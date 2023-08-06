# Residual Dense Network for Image Super-Resolution
# https://arxiv.org/abs/1802.08797

from model import common

import torch
import torch.nn as nn


def make_model(args, parent=False):
    return RDN(args)


class RDB_Conv(nn.Module):
    def __init__(self, inChannels, growRate, kSize=3):
        super(RDB_Conv, self).__init__()
        Cin = inChannels
        G = growRate
        self.conv = nn.Sequential(*[
            nn.BatchNorm3d(),
            nn.ReLU(),
            nn.Conv3d(Cin, G, kSize, padding=(kSize - 1) // 2, stride=1)
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
        self.LFF = nn.Conv3d(G0 + C * G, G0, 1, padding=0, stride=1)

    def forward(self, x):
        return self.LFF(self.convs(x)) + x


class RDN(nn.Module):
    def __init__(self, args):
        super(RDN, self).__init__()
        r = args.scale[0]
        G0 = 32
        kSize = args.RDNkSize

        # number of RDB blocks D, conv layers within the blocks C, out channels G within the last layer of the blocks,
        # self.D, C, G = {
        #     'A': (20, 6, 32),
        #     'B': (16, 8, 64),
        #     'C': (10, 8, 64),
        # }[args.RDNconfig]

        # Shallow feature extraction net
        self.SFENet1 = nn.Conv3d(args.n_colors, G0, kSize, padding=(kSize - 1) // 2, stride=1)
        # Redidual dense blocks and dense feature fusion
        self.RDBs = nn.ModuleList()
        for i in range(4):
            self.RDBs.append(
                RDB(growRate0=G0, growRate=G0/2, nConvLayers=4)
            )

        # Global Feature Fusion
        self.recon = nn.Sequential(*[
            nn.Conv3d(5*G0, 1, 1, padding=0, stride=1)
        ])


    def forward(self, x):
        x = self.SFENet1(x)

        RDBs_out = [x]
        for i in range(self.D):
            x = self.RDBs[i](x)
            RDBs_out.append(x)

        x = self.recon(torch.cat(RDBs_out, 1))
        return x
