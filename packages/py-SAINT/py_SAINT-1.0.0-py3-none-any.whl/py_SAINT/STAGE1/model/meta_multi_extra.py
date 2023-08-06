import torch
import torch.nn as nn


def make_model(args, parent=False):
    return MSR_RDN(args)

## this generates the index mask for reorganizing the outputs
def get_org_mask(dim):
    factor = dim[1]+1
    output_shape = dim[3]*factor
    ind = torch.LongTensor(list(range(0,output_shape)))
    perm = ind[::dim[3]]
    for i in range(dim[3]-1):
        perm = torch.cat((perm, ind[i+1:][::dim[3]]))
    return perm

class RDB_Conv(nn.Module):
    def __init__(self, inChannels, growRate, kSize=3):
        super(RDB_Conv, self).__init__()
        Cin = inChannels
        G = growRate
        self.conv = nn.Sequential(*[
            nn.Conv2d(Cin, G, kSize, padding=(kSize - 1) // 2, stride=1),
            nn.ReLU()
        ])

    def forward(self, x):
        out = self.conv(x)
        return torch.cat((x, out), 1)


class RDB(nn.Module):
    def __init__(self, growRate0, growRate, nConvLayers, kSize=3):
        super(RDB, self).__init__()
        G0 = growRate0
        G = growRate
        C = nConvLayers

        convs = []
        for c in range(C):
            convs.append(RDB_Conv(G0 + c * G, G))
        self.convs = nn.Sequential(*convs)

        # Local Feature Fusion
        self.LFF = nn.Conv2d(G0 + C * G, G0, 1, padding=0, stride=1)

    def forward(self, x):
        return self.LFF(self.convs(x)) + x

class GenWeights(nn.Module):
    def __init__(self,inpC=64, kernel_size=3, outC=32):
        super(GenWeights,self).__init__()
        self.kernel_size=kernel_size
        self.outC = outC
        self.inpC = inpC
        self.meta_block=nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=(3 - 1) // 2, stride=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 64, 3, padding=(3 - 1) // 2, stride=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, 3, padding=(3 - 1) // 2, stride=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, 3, padding=(3 - 1) // 2, stride=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, 3, padding=(3 - 1) // 2, stride=1)
        )
    def forward(self,x):
        output = self.meta_block(x)
        return output


class MSR_RDN(nn.Module):
    def __init__(self, args):
        super(MSR_RDN, self).__init__()
        G0 = args.G0
        kSize = args.RDNkSize

        # number of RDB blocks D, conv layers within the blocks C, out channels G within the last layer of the blocks,
        self.D, C, G = {
            'A': (20, 6, 32),
            'B': (16, 8, 64),
            'C': (6, 8, 32),
        }[args.RDNconfig]

        # Shallow feature extraction net
        self.SFENet1 = nn.Conv2d(3, G0, kSize, padding=(kSize - 1) // 2, stride=1)
        self.SFENet2 = nn.Conv2d(G0, G0, kSize, padding=(kSize - 1) // 2, stride=1)

        # Redidual dense blocks and dense feature fusion
        self.RDBs = nn.ModuleList()
        for i in range(self.D):
            self.RDBs.append(
                RDB(growRate0=G0, growRate=G, nConvLayers=C)
            )

        # Global Feature Fusion
        self.GFF = nn.Sequential(*[
            nn.Conv2d(self.D * G0, G0, 1, padding=0, stride=1),
            nn.Conv2d(G0, G0, kSize, padding=(kSize - 1) // 2, stride=1)
        ])
        self.GW = GenWeights()
        self.last_layer = nn.Conv2d(4, 4, kSize, padding=(kSize - 1) // 2, stride=1)
        # self.Final = nn.Sequential(*[
        #     nn.Conv2d(32, 1, kSize, padding=(kSize - 1) // 2, stride=1),
        #     nn.ReLU(inplace=True)
        #                            ])
        # self.mapping = get_org_mask([1,3,512,32])

    def forward(self, inp_x, dist, num):
        f__1 = self.SFENet1(inp_x)
        x = self.SFENet2(f__1)
        RDBs_out = []
        for i in range(self.D):
            x = self.RDBs[i](x)
            RDBs_out.append(x)
        x = self.GFF(torch.cat(RDBs_out, 1))
        x += f__1
        # weights = []
        # inp_feature = nn.functional.unfold(x, 3, padding=1)


        for i in range(int(dist.size(1))):
            if i == 0:
                weights = self.GW(dist[:,[i],:,:]).view(x.size(0),1,64,3,3)
            else:
                weights = torch.cat((weights, self.GW(dist[:,[i],:,:]).view(x.size(0),1,64,3,3)), 1)
        inp = nn.functional.unfold(x, 3, padding=1)
        # print("input shape: ", x.size(),weights.size(),inp.size())
        output = inp.transpose(1, 2).matmul(weights.view(weights.size(0), weights.size(1), -1).transpose(1,2)).transpose(1, 2)
        output = output.view(-1, dist.size(1), x.size(2),x.size(3))


        return self.last_layer(output)
