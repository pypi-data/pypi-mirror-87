#!/usr/bin/env python3
# coding:utf8

import torch
import torch.nn as nn
import torchvision 

"""
AlexNet
输入: batch_sizex3x224x224
C1: (224-11)/4+1=54 --> 54x54x96
    (54-3)/2+1=26   --> 26x26x96
C2: (26-5+4)/1+1=26 --> 26x26x256
    (26-3)/2+1=12   --> 12x12x256
C3: (12-3+2)/1+1=12 --> 12x12x384
C4,C5:--> 12x12x384   --> 12x12x256
(12-3)/2+1=5    --> 5x5x256

F1: 5x5x256-->1x1x4096
F2: 1x1x4096-->1x1x4096
F3: 1x1x4096-->1x1xnum_classes
历史原因，当时显存不够60M，放在2块显卡上一款48通道，不能单看一款的实现
"""

class AlexNet(nn.Module):
    def __init__(self, in_channels=3, num_classes=1000):
        super(AlexNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(in_channels=in_channels, out_channels=96, kernel_size=11, stride=4),
            nn.MaxPool2d(kernel_size=3, stride=2), 
            nn.ReLU(),

            nn.Conv2d(in_channels=96, out_channels=256, kernel_size=5, padding=2, stride=1),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.ReLU(),

            nn.Conv2d(in_channels=256, out_channels=384, kernel_size=3, padding=1, stride=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=384, out_channels=384, kernel_size=3, padding=1, stride=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=384, out_channels=256, kernel_size=3, padding=1, stride=1),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.ReLU()
        )

        self.classifier = nn.Sequential(
            nn.Linear(5*5*256,4096), 
            nn.ReLU(),

            nn.Dropout(), # 可以设置dropout比率
            nn.Linear(4096, 4096),
            nn.ReLU(),

            nn.Dropout(),
            nn.Linear(4096, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.shape[0], -1)
        x = self.classifier(x)
        return x

if __name__ =='__main__':
    model = torchvision.models.AlexNet()
    # model = AlexNet()

    inputs = torch.randn(8,3,224,224)
    outputs = model(inputs)
    print(outputs.shape)

