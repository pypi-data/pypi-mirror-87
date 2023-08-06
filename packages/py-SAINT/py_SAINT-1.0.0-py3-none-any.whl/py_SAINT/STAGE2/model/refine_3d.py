from model import common

import torch
import torch.nn as nn


def make_model(args, parent=False):
    return FUSE_RDN(args)


class RDB_Conv_Plane(nn.Module):
    def __init__(self, inChannels, growRate, kSize=3):
        super(RDB_Conv_Plane, self).__init__()
        Cin = inChannels
        G = growRate

        self.conv = nn.Sequential(*[
            nn.Conv3d(Cin, G, (3,3,1), padding=(1,1,0), stride=1),
            nn.ReLU()
        ])

    def forward(self, x):
        out = self.conv(x)
        return torch.cat((x, out), 1)

class RDB_Conv_Channel(nn.Module):
    def __init__(self, inChannels, growRate, kSize=3):
        super(RDB_Conv_Channel, self).__init__()
        Cin = inChannels
        G = growRate
        self.conv = nn.Sequential(*[
            nn.Conv3d(Cin, G, (1,1,3), padding=(0,0,1), stride=1),
            nn.ReLU()
        ])

    def forward(self, x):
        out = self.conv(x)
        return torch.cat((x, out), 1)

class RDB(nn.Module):
    def __init__(self, growRate0, growRate, nConvLayers, type, kSize=3):
        super(RDB, self).__init__()
        G0 = growRate0
        G = growRate
        C = nConvLayers

        convs = []
        if type == 'plane':
            for c in range(C):
                convs.append(RDB_Conv_Plane(G0 + c * G, G))
            self.convs = nn.Sequential(*convs)
        else:
            for c in range(C):
                convs.append(RDB_Conv_Channel(G0 + c * G, G))
            self.convs = nn.Sequential(*convs)


        # Local Feature Fusion
        self.LFF = nn.Conv3d(G0 + C * G, G0, 1, padding=0, stride=1)

    def forward(self, x):
        return self.LFF(self.convs(x)) + x


class FUSE_RDN(nn.Module):
    def __init__(self, args):
        super(FUSE_RDN, self).__init__()
        r = args.scale[0]
        G0 = 32
        kSize = args.RDNkSize

        # number of RDB blocks D, conv layers within the blocks C, out channels G within the last layer of the blocks,
        self.D, C, G = {
            'A': (20, 6, 32),
            'B': (16, 8, 64),
            'C': (2, 4, 12),
        }[args.RDNconfig]

        # Shallow feature extraction net
        self.SFENet1 = nn.Conv3d(2, G0, 1, padding=0, stride=1)
        # self.SFENet2 = nn.Conv3d(G0, G0, kSize, padding=(kSize - 1) // 2, stride=1)

        # Redidual dense blocks and dense feature fusion
        self.RDBs = nn.ModuleList()
        for i in range(4):
            self.RDBs.append(
                RDB(growRate0=G0, growRate=G, nConvLayers=C, type='plane')
            )

        for i in range(1):
            self.RDBs.append(
                RDB(growRate0=G0, growRate=G, nConvLayers=C, type='channel')
            )

        # Global Feature Fusion
        self.GFF = nn.Sequential(*[
            nn.Conv3d((5)* G0, G0, 1, padding=0, stride=1),
            nn.Conv3d(G0, G0, 3, padding=1, stride=1)
        ])
        self.UPNet = nn.Sequential(*[
            # nn.Conv3d(G0, G, (3,3,1), padding=(1,1,0), stride=1),
            # nn.PixelShuffle(r),
            nn.Conv3d(G0, 1, 3, padding=1, stride=1)
        ])

    def forward(self, x):
        # print(x.size())
        f__1 = self.SFENet1(x)
        # x  = self.SFENet2(f__1)

        RDBs_out = []
        out = self.RDBs[0](f__1)
        RDBs_out.append(out)
        out = self.RDBs[1](out)
        RDBs_out.append(out)
        out = self.RDBs[2](out)
        RDBs_out.append(out)
        out = self.RDBs[3](out)
        RDBs_out.append(out)
        out = self.RDBs[4](out)
        RDBs_out.append(out)

        out = self.GFF(torch.cat(RDBs_out,1))
        out += f__1
        return self.UPNet(out)+x.mean(1).view(x.size(0), -1, x.size(2),x.size(3),x.size(4))
