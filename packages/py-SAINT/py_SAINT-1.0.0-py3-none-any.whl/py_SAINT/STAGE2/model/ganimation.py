import torch.nn as nn
import numpy as np
import torch

def make_model(args, parent=False):
    return Generator()

class Generator(nn.Module):
    """Generator. Encoder-Decoder Architecture."""
    @property
    def name(self):
        return self._name

    def __init__(self, conv_dim=64, c_dim=5, repeat_num=6):
        super(Generator, self).__init__()
        self._name = 'generator_wgan'

        # Down-Sampling
        downlayers1 = []
        downlayers1.append(nn.Conv2d(1, conv_dim, kernel_size=7, stride=1, padding=3, bias=False))
        downlayers1.append(nn.InstanceNorm2d(conv_dim, affine=True))
        
        self.dn1 = nn.Sequential(*downlayers1)

        curr_dim = conv_dim
        downlayers2 = []
        downlayers2.append(nn.ReLU(inplace=True))
        downlayers2.append(nn.Conv2d(curr_dim, curr_dim*2, kernel_size=4, stride=2, padding=1, bias=False))
        downlayers2.append(nn.InstanceNorm2d(curr_dim*2, affine=True))
        self.dn2 = nn.Sequential(*downlayers2)   

        curr_dim = curr_dim * 2
        downlayers3 = []
        downlayers3.append(nn.ReLU(inplace=True))
        downlayers3.append(nn.Conv2d(curr_dim, curr_dim*2, kernel_size=4, stride=2, padding=1, bias=False))
        downlayers3.append(nn.InstanceNorm2d(curr_dim*2, affine=True))
        self.dn3 = nn.Sequential(*downlayers3)  

        curr_dim = curr_dim * 2

        midlayer = []
        midlayer.append(nn.ReLU(inplace=True))
        # Bottleneck
        for i in range(repeat_num):
            midlayer.append(ResidualBlock(dim_in=curr_dim, dim_out=curr_dim))

        # Up-Sampling

        self.mid = nn.Sequential(*midlayer)

        uplayers2 = []
        # print('curr_dim_input', curr_dim*2)
        uplayers2.append(nn.ConvTranspose2d(curr_dim*2, curr_dim//2, kernel_size=4, stride=2, padding=1, bias=False))
        uplayers2.append(nn.InstanceNorm2d(curr_dim//2, affine=True))
        uplayers2.append(nn.ReLU(inplace=True))
        curr_dim = curr_dim // 2

        self.up2 = nn.Sequential(*uplayers2)

        uplayers1 = []
        uplayers1.append(nn.ConvTranspose2d(curr_dim*2, curr_dim//2, kernel_size=4, stride=2, padding=1, bias=False))
        uplayers1.append(nn.InstanceNorm2d(curr_dim//2, affine=True))
        uplayers1.append(nn.ReLU(inplace=True))
        ##128 channels
        curr_dim = curr_dim // 2

        self.up1 = nn.Sequential(*uplayers1)

        layers = []
        layers.append(nn.Conv2d(curr_dim*2, 1, kernel_size=7, stride=1, padding=3, bias=False))
        layers.append(nn.Tanh())
        self.img_reg = nn.Sequential(*layers)

        layers = []
        layers.append(nn.Conv2d(curr_dim*2, 1, kernel_size=7, stride=1, padding=3, bias=False))
        layers.append(nn.Sigmoid())
        self.attetion_reg = nn.Sequential(*layers)

    def forward(self, x):
        # replicate spatially and concatenate domain information
        # x = torch.cat([x, c], dim=1)

        val1 = self.dn1(x)
        val2 = self.dn2(val1)
        val3 = self.dn3(val2)
        val4 = self.mid(val3)
        # print('val3,val4', val3.shape, val4.shape)
        val5 = self.up2(torch.cat((val3,val4),dim=1))
        # print('val2,val5', val2.shape, val5.shape)
        val6 = self.up1(torch.cat((val2,val5),dim=1))

        attn = self.attetion_reg(torch.cat((val1,val6),dim=1))
        return attn * x, attn

    # def _do_if_necessary_saturate_mask(self, m, saturate=False):
    #     return torch.clamp(0.55*torch.tanh(3*(m-0.5))+0.5, 0, 1) if saturate else m

    # def init_weights(self):
    #     self.apply(self._weights_init_fn)

    # def _weights_init_fn(self, m):
    #     classname = m.__class__.__name__
    #     if classname.find('Conv') != -1:
    #         m.weight.data.normal_(0.0, 0.02)
    #         if hasattr(m.bias, 'data'):
    #             m.bias.data.fill_(0)
    #     elif classname.find('BatchNorm2d') != -1:
    #         m.weight.data.normal_(1.0, 0.02)
    #         m.bias.data.fill_(0)

class ResidualBlock(nn.Module):
    """Residual Block."""
    def __init__(self, dim_in, dim_out):
        super(ResidualBlock, self).__init__()
        self.main = nn.Sequential(
            nn.Conv2d(dim_in, dim_out, kernel_size=3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(dim_out, affine=True),
            nn.ReLU(inplace=True),
            nn.Conv2d(dim_out, dim_out, kernel_size=3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(dim_out, affine=True))

    def forward(self, x):
        return x + self.main(x)