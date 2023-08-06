#!/usr/bin/env python3
# coding=utf-8

import torch
import torch.nn as nn
import torch.nn.functional as F

# 双层卷积 默认参数stride=1，bias=True
class DoubleConv2d(nn.Module):
    def __init__(self, in_channels, out_channels, mid_channels=None):
        super().__init__()
        if not mid_channels:
            mid_channels = out_channels
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, mid_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(mid_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(mid_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )

    def forward(self,x):
        return self.double_conv(x)

# 下采样卷积层 最大池化下采样
class Down(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.maxpool_conv = nn.Sequential(
            nn.MaxPool2d(kernel_size=2), # 默认值stride=kernel_size
            DoubleConv2d(in_channels, out_channels)
        )

    def forward(self, x):
        return self.maxpool_conv(x)


# 上采样卷积层 可采用双线性插值或逆卷积
class Up(nn.Module):
    def __init__(self, in_channels, out_channels, bilinear=True):
        super().__init__()
        if bilinear:
            self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
            self.conv = DoubleConv2d(in_channels, out_channels, in_channels // 2)
        else:
            self.up = nn.ConvTranspose2d(in_channels , in_channels // 2, kernel_size=2, stride=2)
            self.conv = DoubleConv2d(in_channels, out_channels)

    def forward(self, x1, x2):
        x1 = self.up(x1)
        # input is CHW
        diffY = x2.size()[2] - x1.size()[2]
        diffX = x2.size()[3] - x1.size()[3]

        x1 = F.pad(x1, [diffX // 2, diffX - diffX // 2,
                        diffY // 2, diffY - diffY // 2])
        # if you have padding issues, see
        # https://github.com/HaiyongJiang/U-Net-Pytorch-Unstructured-Buggy/commit/0e854509c2cea854e247a9c615f175f76fbb2e3a
        # https://github.com/xiaopeng-liao/Pytorch-UNet/commit/8ebac70e633bac59fc22bb5195e513d5832fb3bd
        x = torch.cat([x2, x1], dim=1)
        return self.conv(x)


"""
U-Net 网络，改自FCN，只有卷积层无全连接层
"""
class UNet(nn.Module):
    def __init__(self, in_ch=3, out_ch=1, bilinear=True):
        super(UNet, self).__init__()
        
        self.in_conv = DoubleConv2d(in_channels=in_ch, out_channels=64)
        self.down1 = Down(in_channels=64, out_channels=128)
        self.down2 = Down(in_channels=128, out_channels=256)
        self.down3 = Down(in_channels=256, out_channels=512)
        factor = 2 if bilinear else 1
        self.down4 = Down(in_channels=512, out_channels=1024//factor)

        self.up1 = Up(in_channels=1024, out_channels=512//factor, bilinear=bilinear)
        self.up2 = Up(in_channels=512, out_channels=256//factor, bilinear=bilinear)
        self.up3 = Up(in_channels=256, out_channels=128//factor, bilinear=bilinear)
        self.up4 = Up(in_channels=128, out_channels=64, bilinear=bilinear)
        self.out_conv = nn.Conv2d(in_channels=64, out_channels=out_ch, kernel_size=1)

    def forward(self,x):
        x1 = self.in_conv(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        out = self.out_conv(x)
        return out


if __name__ == '__main__':
    model = UNet(in_ch=3, out_ch=1)

    inputs = torch.randn(1, 3, 572, 572)
    outputs = model(inputs)
    print(outputs.shape)


