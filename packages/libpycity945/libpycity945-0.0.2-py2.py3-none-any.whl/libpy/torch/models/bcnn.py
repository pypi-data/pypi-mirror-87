#!/usr/bin/env python3

import torch
import torchvision
import torch.optim as optim
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F

def ConvBNReLU(in_channels,out_channels,kernel_size):
    return nn.Sequential(
        nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, stride=1,padding=kernel_size//2),
        nn.BatchNorm2d(out_channels),
        nn.ReLU6(inplace=True)
    )

class InceptionV1Module(nn.Module):
    def __init__(self, in_channels,out_channels1, out_channels2reduce,out_channels2, out_channels3reduce, out_channels3, out_channels4):
        super(InceptionV1Module, self).__init__()

        self.branch1_conv = ConvBNReLU(in_channels=in_channels,out_channels=out_channels1,kernel_size=1)

        self.branch2_conv1 = ConvBNReLU(in_channels=in_channels,out_channels=out_channels2reduce,kernel_size=1)
        self.branch2_conv2 = ConvBNReLU(in_channels=out_channels2reduce,out_channels=out_channels2,kernel_size=3)

        self.branch3_conv1 = ConvBNReLU(in_channels=in_channels, out_channels=out_channels3reduce, kernel_size=1)
        self.branch3_conv2 = ConvBNReLU(in_channels=out_channels3reduce, out_channels=out_channels3, kernel_size=5)

        self.branch4_pool = nn.MaxPool2d(kernel_size=3,stride=1,padding=1)
        self.branch4_conv1 = ConvBNReLU(in_channels=in_channels, out_channels=out_channels4, kernel_size=1)

    def forward(self,x):
        out1 = self.branch1_conv(x)
        out2 = self.branch2_conv2(self.branch2_conv1(x))
        out3 = self.branch3_conv2(self.branch3_conv1(x))
        out4 = self.branch4_conv1(self.branch4_pool(x))
        out = torch.cat([out1, out2, out3, out4], dim=1)
        return out

class BCNN(nn.Module):
    def __init__(self,in_channels=3, num_classes=2):
        super(BCNN, self).__init__()
        self.block1 = nn.Sequential(
            nn.Conv2d(in_channels=3,out_channels=64,kernel_size=7,stride=3,padding=3),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(kernel_size=3,stride=3, padding=1),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=1, stride=1),
            nn.BatchNorm2d(64),
        )
        self.block2 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=192, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(192),
            nn.MaxPool2d(kernel_size=3, stride=3, padding=1),
        )

        self.block3 = nn.Sequential(
            InceptionV1Module(in_channels=192,out_channels1=64, out_channels2reduce=96, out_channels2=128, out_channels3reduce = 16, out_channels3=32, out_channels4=32),
            InceptionV1Module(in_channels=256, out_channels1=128, out_channels2reduce=128, out_channels2=192,out_channels3reduce=32, out_channels3=96, out_channels4=64),
            nn.MaxPool2d(kernel_size=3, stride=3, padding=1),
        )

        self.block4 = nn.Sequential(
            InceptionV1Module(in_channels=480, out_channels1=192, out_channels2reduce=96, out_channels2=208,out_channels3reduce=16, out_channels3=48, out_channels4=64),
            InceptionV1Module(in_channels=512, out_channels1=160, out_channels2reduce=112, out_channels2=224,
                              out_channels3reduce=24, out_channels3=64, out_channels4=64),
            InceptionV1Module(in_channels=512, out_channels1=128, out_channels2reduce=128, out_channels2=256,
                              out_channels3reduce=24, out_channels3=64, out_channels4=64),
            InceptionV1Module(in_channels=512, out_channels1=112, out_channels2reduce=144, out_channels2=288,
                              out_channels3reduce=32, out_channels3=64, out_channels4=64),
            InceptionV1Module(in_channels=528, out_channels1=256, out_channels2reduce=160, out_channels2=320,
                              out_channels3reduce=32, out_channels3=128, out_channels4=128),
            nn.MaxPool2d(kernel_size=3, stride=3, padding=1),
        )

        self.block5 = nn.Sequential(
            InceptionV1Module(in_channels=832, out_channels1=256, out_channels2reduce=160, out_channels2=320,out_channels3reduce=32, out_channels3=128, out_channels4=128),
            InceptionV1Module(in_channels=832, out_channels1=384, out_channels2reduce=192, out_channels2=384,out_channels3reduce=48, out_channels3=128, out_channels4=128),
        )

        self.classifiers = nn.Sequential(
            nn.Linear(1024 ** 2, num_classes),
        )

    def forward(self, x):
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)
        x = self.block4(x)
        x = self.block5(x)

        batch_size = x.size(0)
        x = x.view(batch_size, 1024, 13 * 13)

        x = (torch.bmm(x, torch.transpose(x, 1, 2)) / 13 ** 2).view(batch_size, -1)

        x = torch.nn.functional.normalize(torch.sign(x) * torch.sqrt(torch.abs(x) + 1e-10))

        # feature = feature.view(feature.size(0), -1)
        x = self.classifiers(x)
        return x

if __name__ =='__main__':
    # model = torchvision.models.vgg16()
    model = BCNN()

    inputs = torch.randn(1,3,3024,3024)
    outputs = model(inputs)
    print(outputs.shape)


