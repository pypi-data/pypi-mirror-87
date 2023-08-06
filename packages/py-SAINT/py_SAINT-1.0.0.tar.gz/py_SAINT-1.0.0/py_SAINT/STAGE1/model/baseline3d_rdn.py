# Residual Dense Network for Image Super-Resolution
# https://arxiv.org/abs/1802.08797

from model import common

import torch
import torch.nn as nn


def make_model(args, parent=False):
    return RDN3D(args)


def pixel_shuffle_3d(input, upscale_factor):
    batch_size, channels, in_height, in_width, in_depth = input.size()
    channels //= upscale_factor
    
    out_height = in_height * upscale_factor

    input_view = input.contiguous().view(
    batch_size, channels, upscale_factor, in_height, in_width, in_depth)

    shuffle_out = input_view.permute(0, 1, 3, 2, 4, 5).contiguous()
    return shuffle_out.view(batch_size, channels, out_height, in_width, in_depth)


class PixelShuffle3d(nn.Module):
    def __init__(self, upscale_factor):
        super(PixelShuffle3d, self).__init__()
        self.upscale_factor = upscale_factor

    def forward(self, input):
        return pixel_shuffle_3d(input, self.upscale_factor)

    def extra_repr(self):
        return 'upscale_factor={}'.format(self.upscale_factor)


class RDB_Conv(nn.Module):
    def __init__(self, inChannels, growRate, kSize=3):
        super(RDB_Conv, self).__init__()
        Cin = inChannels
        G  = growRate
        self.conv = nn.Sequential(*[
            nn.Conv3d(Cin, G, kSize, padding=(kSize-1)//2, stride=1),
            nn.ReLU()
        ])

    def forward(self, x):
        out = self.conv(x)
        return torch.cat((x, out), 1)

class RDB(nn.Module):
    def __init__(self, growRate0, growRate, nConvLayers, kSize=3):
        super(RDB, self).__init__()
        G0 = growRate0
        G  = growRate
        C  = nConvLayers
        
        convs = []
        for c in range(C):
            convs.append(RDB_Conv(G0 + c*G, G))
        self.convs = nn.Sequential(*convs)
        
        # Local Feature Fusion
        self.LFF = nn.Conv3d(G0 + C*G, G0, 1, padding=0, stride=1)

    def forward(self, x):
        return self.LFF(self.convs(x)) + x

class RDN3D(nn.Module):
    def __init__(self, args):
        super(RDN3D, self).__init__()
        r = args.scale[0]
        G0 = args.G0
        kSize = args.RDNkSize

        # number of RDB blocks D, conv layers within the blocks C, out channels G within the last layer of the blocks,
        self.D, C, G = {
            'A': (20, 6, 32),
            'B': (16, 8, 64),
            'C': (2, 8, 32),
            'D': (6, 8, 16)
        }[args.RDNconfig]

        # Shallow feature extraction net
        self.SFENet1 = nn.Conv3d(args.n_colors, G0, kSize, padding=(kSize-1)//2, stride=1)
        self.SFENet2 = nn.Conv3d(G0, G0, kSize, padding=(kSize-1)//2, stride=1)

        # Redidual dense blocks and dense feature fusion
        self.RDBs = nn.ModuleList()
        for i in range(self.D):
            self.RDBs.append(
                RDB(growRate0 = G0, growRate = G, nConvLayers = C)
            )

        # Global Feature Fusion
        self.GFF = nn.Sequential(*[
            nn.Conv3d(self.D * G0, G0, 1, padding=0, stride=1),
            nn.Conv3d(G0, G0, kSize, padding=(kSize-1)//2, stride=1)
        ])

        # Up-sampling net
        self.UPNet = nn.Sequential(*[
            nn.Conv3d(G0, G * 2, kSize, padding=(kSize-1)//2, stride=1),
            PixelShuffle3d(2),
            nn.Conv3d(G, G * 2, kSize, padding=(kSize-1)//2, stride=1),
            PixelShuffle3d(2),
            nn.Conv3d(G, 1, kSize, padding=(kSize-1)//2, stride=1)
        ])
        


    def forward(self, x, first_layer, loc):

        if loc == 'first':
            f__1 = self.SFENet1(x)
            x  = self.SFENet2(f__1)
            return x, f__1

        if 'second' in loc:
            RDB_num = int(loc[-1])
            return self.RDBs[RDB_num](x)

        # RDBs_out = []
        # for i in range(self.D):
        #     x = self.RDBs[i](x)
        #     RDBs_out.append(x)
        if 'third' in loc:
            x = self.GFF(x)
            x += first_layer
            return x
        if 'fourth' in loc:
            return self.UPNet(x)
