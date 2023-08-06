import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
def make_model(args, parent=False):
    return UNet(in_channels=1,out_channels=3,depth=5,residual=False)

class UNet(nn.Module):
    def __init__(self, in_channels=1, out_channels=1, depth=3, wf=6, padding=True,
                 batch_norm=False, up_mode='upconv', residual=False, use_coord=False, polar=False):
        super(UNet, self).__init__()
        assert up_mode in ('upconv', 'upsample')
        self.padding = padding
        self.depth = depth
        self.residual = residual

        prev_channels = in_channels
        self.down_path = nn.ModuleList()
        for i in range(depth):
            if i == 0 and use_coord:
                self.down_path.append(UNetConvBlock(prev_channels, 2 ** (wf + i), padding, batch_norm, coord=True, polar=polar))
            else:
                self.down_path.append(UNetConvBlock(prev_channels, 2**(wf+i), padding, batch_norm))
            prev_channels = 2**(wf+i)

        self.up_path = nn.ModuleList()
        for i in reversed(range(depth - 1)):
            self.up_path.append(UNetUpBlock(prev_channels, 2**(wf+i), up_mode,
                                            padding, batch_norm))
            prev_channels = 2**(wf+i)

        self.last = nn.Conv2d(prev_channels, out_channels, kernel_size=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        input = x
        blocks = []
        for i, down in enumerate(self.down_path):
            x = down(x)
            if i != len(self.down_path)-1:
                blocks.append(x)
                x = F.avg_pool2d(x, 2)

        for i, up in enumerate(self.up_path):
            x = up(x, blocks[-i-1])

        if self.residual:
            out = input[:, 1:4, :, :] + self.last(x)
        else:
            out = self.last(x)

        return self.sigmoid(out)

class UNetConvBlock(nn.Module):
    def __init__(self, in_size, out_size, padding, batch_norm, coord=False, polar=False):
        super(UNetConvBlock, self).__init__()
        block = []

        if coord:
            block.append(CoordConv(in_size, out_size, with_r=polar, kernel_size=3, padding=int(padding)))
        else:
            block.append(nn.Conv2d(in_size, out_size, kernel_size=3,
                                   padding=int(padding)))
        block.append(nn.ReLU())
        if batch_norm:
            block.append(nn.BatchNorm2d(out_size))
        else:
            block.append(nn.InstanceNorm2d(out_size))

        if coord:
            block.append(CoordConv(out_size, out_size, with_r=polar, kernel_size=3, padding=int(padding)))
        else:
            block.append(nn.Conv2d(out_size, out_size, kernel_size=3,
                                   padding=int(padding)))
        block.append(nn.ReLU())
        if batch_norm:
            block.append(nn.BatchNorm2d(out_size))
        else:
            block.append(nn.InstanceNorm2d(out_size))

        self.block = nn.Sequential(*block)

    def forward(self, x):
        out = self.block(x)
        return out


class UNetUpBlock(nn.Module):
    def __init__(self, in_size, out_size, up_mode, padding, batch_norm):
        super(UNetUpBlock, self).__init__()
        if up_mode == 'upconv':
            self.up = nn.ConvTranspose2d(in_size, out_size, kernel_size=2,
                                         stride=2)
        elif up_mode == 'upsample':
            self.up = nn.Sequential(nn.Upsample(mode='bilinear', scale_factor=2),
                                    nn.Conv2d(in_size, out_size, kernel_size=1))

        self.conv_block = UNetConvBlock(in_size, out_size, padding, batch_norm)

    def center_crop(self, layer, target_size):
        _, _, layer_height, layer_width = layer.size()
        diff_y = (layer_height - target_size[0]) // 2
        diff_x = (layer_width - target_size[1]) // 2
        return layer[:, :, diff_y:(diff_y + target_size[0]), diff_x:(diff_x + target_size[1])]

    def forward(self, x, bridge):
        up = self.up(x)
        crop1 = self.center_crop(bridge, up.shape[2:])
        out = torch.cat([up, crop1], 1)
        out = self.conv_block(out)

        return out
