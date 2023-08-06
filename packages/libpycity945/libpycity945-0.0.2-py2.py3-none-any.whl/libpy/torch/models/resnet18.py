#!/usr/bin/env python3
# coding=utf-8

import torch
import torchvision
import torch.nn as nn 

'''
ResNet结构: https://gitee.com/city945/imageHost/raw/master/resnet_struct.png 学习先看resnet_deep.py
1. 含4个stage残差组，每组n个残差块，除第一组是由池化减半尺寸外，其他组的第一块stride=2减半尺寸
2. 每个stage都有个虚拟连接，一般是由第一个残差块输入的下采样 downsample 得来，downsample针对恒等连接
输入: batch_sizex3x224x224
先Conv1做步幅2的卷积 64x112x112 再con2.x先做步幅2的max pool 64x56x56
对stage1:
    input: 64x56x56 output: 64x56x56
    这个stage没有'虚线'链接，即每个残差块的输入输出维度一致，可以将identity直接加到输出
    采用1x1卷积核，stride=1的方式也能构造一个identity，故对stage1而言，layers内部的残差块都是一样的
对其他stage如stage2:
    input: 64x56x56 output: 256x28x28
    第一个残差块承担尺寸减半任务，输入输出维度不一致，有'虚线'链接(非恒等，采用1x1卷积核，stride=2降低尺寸，指定通道数翻倍实现)
stage1: input: 64x56x56-->(stage1第一块)64x56x56
                        -->64x56x56-->64x56x56-->256x56x56
                        -->64x56x56-->64x56x56-->256x56x56
stage2: input: 256x56x56-->(带虚线的残差块)512x28x28   512个256x1x1 stride=2去卷
                        -->128x28x28-->128x28x28-->512x28x28 # !!每个stage的非第一个残差块没传stride，默认1，不改变尺寸
                        -->...
'''

def Conv1(in_channels, out_channels, stride=3): # 3024+6-7  / 3 +1   ==1008
    return nn.Sequential(
        nn.Conv2d(in_channels, out_channels, kernel_size=7, stride=stride, padding=3, bias=False), # 默认带偏置，带不带无所谓
        nn.BatchNorm2d(out_channels),
        nn.ReLU(inplace=True), # 对原变量覆盖

        nn.MaxPool2d(kernel_size=3, stride=3, padding=1) # (H + 2P - FH) / S + 1   1008+2-3 /3 +1
    )
# 残差单元
class Bottleneck(nn.Module): 
    def __init__(self, in_channels, out_channels, stride=1, downsampling=False): 
        super(Bottleneck, self).__init__()
        self.downsampling = downsampling
        
        self.bottleneck = nn.Sequential(
            nn.Conv2d(in_channels, out_channels=out_channels, kernel_size=3, stride=stride, padding=1, bias=False), # (56 + 2 - 3)/2 +1
            nn.BatchNorm2d(num_features=out_channels), # 期望输入的特征数
            nn.ReLU(),

            nn.Conv2d(out_channels, out_channels=out_channels, kernel_size=3, stride=1, padding=1, bias=False), # kernel_size=3则要padding=1维持尺寸
            nn.BatchNorm2d(out_channels),
            nn.ReLU(),
        )

        if self.downsampling: # 下采样针对恒等连接， 对于stage1的第一块不需减半, stride=1，其 downsample也就是1x1的卷积做的恒等,尺寸不变
            self.downsample = nn.Sequential(
                nn.Conv2d(in_channels, out_channels=out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
        self.relu = nn.ReLU() 

    def forward(self, x): 
        identity = x
        out = self.bottleneck(x)

        if self.downsampling:
            identity = self.downsample(x) 

        out += identity
        out = self.relu(out)
        return out
     
class ResNet(nn.Module):
    def __init__(self, blocks, in_channels=3, num_classes=1000):
        super(ResNet, self).__init__()

        self.conv1 = Conv1(in_channels=in_channels, out_channels=64) # 224x224x3 --> 56x56x64
        # 此 out_channels是每个残差块前两层的channel相同, 第三层是 out_channels的倍数
        self.stage1 = self._make_layers(in_channels=64, out_channels=64, num_block=blocks[0], stride=1) # 残差组1由于池化尺寸已减半，stride=1第一个残差块就不减尺寸了
        self.stage2 = self._make_layers(in_channels=64, out_channels=128, num_block=blocks[1], stride=3)# in_channels上一stage的输出通道，out_channels当前stage第一块第一层的输出通道
        self.stage3 = self._make_layers(in_channels=128, out_channels=256, num_block=blocks[2], stride=3)
        self.stage4 = self._make_layers(in_channels=256, out_channels=512, num_block=blocks[3], stride=3)# stride全改成3 3042/243=12

        self.avgpool = nn.AvgPool2d(kernel_size=13, stride=1) 
        self.fc = nn.Linear(512, num_classes) # 浅层resnet 7x7x512经7x7卷积后成1x512 
        

    def forward(self, x):
        x = self.conv1(x)

        x = self.stage1(x)
        x = self.stage2(x)
        x = self.stage3(x)
        x = self.stage4(x)

        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

    def _make_layers(self, in_channels, out_channels, num_block, stride):
        layers = []
        # 每个stage残差组的第一块可能涉及到输入输出尺寸不一，即虚线的链接，单独处理
        layers.append(Bottleneck(in_channels, out_channels, stride, downsampling=True))
        for i in range(1, num_block): # 第一个残差块已将输出翻倍，故第二残差块的输入也翻倍
            layers.append(Bottleneck(out_channels, out_channels)) # 没传stride,其=1，此残差块不改变尺寸，而且输入尺寸是上一个参差块的输出

        return nn.Sequential(*layers)


def ResNet18(in_channels=3, num_classes=2):
    return ResNet([2,2,2,2], in_channels=in_channels, num_classes=num_classes)

def ResNet34(in_channels=3, num_classes=1000):
    return ResNet([3,4,6,3], in_channels=in_channels, num_classes=num_classes)

if __name__ =='__main__':
    # model = torchvision.models.resnet18()
    model = ResNet34()

    inputs = torch.randn(1,3,224,224)
    outputs = model(inputs)
    print(outputs.shape)

