import torch.nn as nn
import torch.nn.functional as F
import torch

# Residual block
class ResidualBlock(nn.Module):
    def __init__(self, in_features):
        super(ResidualBlock, self).__init__()

        conv_block = [  nn.ReflectionPad2d(1), # N, C, H, W  H, W 上下左右各填充1个像素
                        nn.Conv2d(in_features, in_features, 3),
                        nn.InstanceNorm2d(in_features),
                        nn.ReLU(inplace=True),
                        nn.ReflectionPad2d(1),
                        nn.Conv2d(in_features, in_features, 3),
                        nn.InstanceNorm2d(in_features)  ]

        self.conv_block = nn.Sequential(*conv_block)

    def forward(self, x):
        return x + self.conv_block(x)
"""
# DenseNet
class DenseBlock(nn.Module):
    def __init__(self, in_features):
        super(DenseBlock, self).__init__()

        self.relu = nn.ReLU(inplace = True)
        self.bn = nn.BatchNorm2d(num_features = in_features)
        
        self.conv1 = nn.Conv2d(in_channels = in_features, out_channels = 32, kernel_size = 3, stride = 1, padding = 1)
        self.conv2 = nn.Conv2d(in_channels = 32, out_channels = 32, kernel_size = 3, stride = 1, padding = 1)
        self.conv3 = nn.Conv2d(in_channels = 64, out_channels = 32, kernel_size = 3, stride = 1, padding = 1)
        self.conv4 = nn.Conv2d(in_channels = 96, out_channels = 32, kernel_size = 3, stride = 1, padding = 1)
        self.conv5 = nn.Conv2d(in_channels = 128, out_channels = 32, kernel_size = 3, stride = 1, padding = 1)
    
    def forward(self, x):
        bn = self.bn(x) 
        conv1 = self.relu(self.conv1(bn))
        conv2 = self.relu(self.conv2(conv1))

        # Concatenate in channel dimension
        c2_dense = self.relu(torch.cat([conv1, conv2], 1))
        conv3 = self.relu(self.conv3(c2_dense))
        c3_dense = self.relu(torch.cat([conv1, conv2, conv3], 1))
        conv4 = self.relu(self.conv4(c3_dense))
        c4_dense = self.relu(torch.cat([conv1, conv2, conv3, conv4], 1))
        conv5 = self.relu(self.conv5(c4_dense))
        c5_dense = self.relu(torch.cat([conv1, conv2, conv3, conv4, conv5], 1))
    
        return c5_dense

# DenseNet transition layer
class Transition_Layer(nn.Module): 
  def __init__(self, in_channels, out_channels):
    super(Transition_Layer, self).__init__() 
    
    self.relu = nn.ReLU(inplace = True) 
    self.bn = nn.BatchNorm2d(num_features = out_channels) 
    self.conv = nn.Conv2d(in_channels = in_channels, out_channels = out_channels, kernel_size = 1, bias = False) 
    self.avg_pool = nn.AvgPool2d(kernel_size = 2, stride = 2, padding = 0) 
  
  def forward(self, x): 
    bn = self.bn(self.relu(self.conv(x))) 
    out = self.avg_pool(bn) 
    return out 
"""

# DenseNet
class DenseBlock(nn.Module):
    def __init__(self, in_features):
        super(DenseBlock, self).__init__()

        self.relu = nn.ReLU(inplace = True)
        self.bn = nn.BatchNorm2d(num_features = in_features)
        
        self.conv1 = nn.Conv2d(in_channels = in_features, out_channels = 32, kernel_size = 3, stride = 1, padding = 1)
        self.conv2 = nn.Conv2d(in_channels = 32, out_channels = 32, kernel_size = 3, stride = 1, padding = 1)
        self.conv3 = nn.Conv2d(in_channels = 64, out_channels = 32, kernel_size = 3, stride = 1, padding = 1)
        self.conv4 = nn.Conv2d(in_channels = 96, out_channels = 32, kernel_size = 3, stride = 1, padding = 1)
        self.conv5 = nn.Conv2d(in_channels = 128, out_channels = 32, kernel_size = 3, stride = 1, padding = 1)
    
    def forward(self, x):
        bn = self.bn(x) 
        conv1 = self.relu(self.conv1(bn))
        conv2 = self.relu(self.conv2(conv1))

        # Concatenate in channel dimension
        c2_dense = self.relu(torch.cat([conv1, conv2], 1))
        conv3 = self.relu(self.conv3(c2_dense))
        c3_dense = self.relu(torch.cat([conv1, conv2, conv3], 1))
        conv4 = self.relu(self.conv4(c3_dense))
        c4_dense = self.relu(torch.cat([conv1, conv2, conv3, conv4], 1))
        conv5 = self.relu(self.conv5(c4_dense))
        c5_dense = self.relu(torch.cat([conv1, conv2, conv3, conv4, conv5], 1))
    
        return c5_dense

# DenseNet transition layer
class Transition_Layer(nn.Module): 
  def __init__(self, in_channels, out_channels):
    super(Transition_Layer, self).__init__() 
    
    self.relu = nn.ReLU(inplace = True) 
    self.bn = nn.BatchNorm2d(num_features = out_channels) 
    self.conv = nn.Conv2d(in_channels = in_channels, out_channels = out_channels, kernel_size = 1, bias = False) 
    #self.avg_pool = nn.AvgPool2d(kernel_size = 2, stride = 2, padding = 0) 
  
  def forward(self, x): 
    bn = self.bn(self.relu(self.conv(x))) 
    #out = self.avg_pool(bn) 
    return bn

class Generator(nn.Module):
    def __init__(self, input_nc, output_nc, use_densenet=False, n_residual_blocks=6):
        super(Generator, self).__init__()

        # batchSize, 1, 128, 128

        # Initial convolution block
        model = [   nn.ReflectionPad2d(3),
                    nn.Conv2d(input_nc, 64, 7),
                    nn.InstanceNorm2d(64),
                    nn.ReLU(inplace=True) ]

        # Downsampling
        in_features = 64
        out_features = in_features*2
        for _ in range(2):
            model += [  nn.Conv2d(in_features, out_features, 3, stride=2, padding=1),
                        nn.InstanceNorm2d(out_features),
                        nn.ReLU(inplace=True) ]
            in_features = out_features
            out_features = in_features*2
        # 256
        # Transfer module
        if not use_densenet:
            for _ in range(n_residual_blocks):
                model += [ResidualBlock(in_features)]
        else:
            model += [DenseBlock(in_features)] 
            model += [Transition_Layer(160,256)]# 3 256 16 16  #expect: 256 128 3 3

        # Upsampling
        out_features = in_features//2
        for _ in range(2):
            model += [  nn.ConvTranspose2d(in_features, out_features, 3, stride=2, padding=1, output_padding=1),
                        nn.InstanceNorm2d(out_features),
                        nn.ReLU(inplace=True) ]
            in_features = out_features
            out_features = in_features//2

        # Output layer
        model += [  nn.ReflectionPad2d(3),
                    nn.Conv2d(64, output_nc, 7),
                    nn.Tanh() ]

        self.model = nn.Sequential(*model)

    def forward(self, x):
        return self.model(x)

class Discriminator(nn.Module):
    def __init__(self, input_nc):
        super(Discriminator, self).__init__()

        # A bunch of convolutions one after another
        model = [   nn.Conv2d(input_nc, 64, 4, stride=2, padding=1),
                    nn.LeakyReLU(0.2, inplace=True) ]

        model += [  nn.Conv2d(64, 128, 4, stride=2, padding=1),
                    nn.InstanceNorm2d(128), 
                    nn.LeakyReLU(0.2, inplace=True) ]

        model += [  nn.Conv2d(128, 256, 4, stride=2, padding=1),
                    nn.InstanceNorm2d(256), 
                    nn.LeakyReLU(0.2, inplace=True) ]

        model += [  nn.Conv2d(256, 512, 4, padding=1),
                    nn.InstanceNorm2d(512), 
                    nn.LeakyReLU(0.2, inplace=True) ]

        # FCN classification layer
        model += [nn.Conv2d(512, 1, 4, padding=1)]

        self.model = nn.Sequential(*model)

    def forward(self, x):
        x =  self.model(x)
        # Average pooling and flatten
        return F.avg_pool2d(x, x.size()[2:]).view(x.size()[0], -1)