import torch
from basemodel import PoolFormer
import torch.nn as nn
import basemodel


# different decoders
# vanilla decoders
class vanilla_decoder(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.Linear1 = nn.Linear(768,1000)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        return self.relu(self.Linear1(x.mean([-2,-1])))

    
# deconv decoder 
class deconv_decoder(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.deconv1 = nn.ConvTranspose2d(768, 384, 4, stride=2, padding=1)
        self.bn1 = nn.BatchNorm2d(384)
        self.deconv2 = nn.ConvTranspose2d(384, 192, 4, stride=2, padding=1)
        self.bn2 = nn.BatchNorm2d(192)
        self.deconv3 = nn.ConvTranspose2d(192, 96, 4, stride=2, padding=1)
        self.bn3 = nn.BatchNorm2d(96)
        self.relu = nn.ReLU()
        self.conv = nn.Conv2d(96,17, 1)
        
    def forward(self, x):
        x = self.deconv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.deconv2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.deconv3(x)
        x = self.bn3(x)
        x = self.relu(x)
        x = self.conv(x)
        return x
        
    
class Backbone(PoolFormer):
    def __init__(self, **kwargs):
        layers = [8, 8, 24, 8]
        embed_dims = [96, 192, 384, 768]
        mlp_ratios = [4, 4, 4, 4]
        downsamples = [True, True, True, True]
        super().__init__(
            layers, embed_dims=embed_dims, 
            mlp_ratios=mlp_ratios, downsamples=downsamples, 
            layer_scale_init_value=1e-6, 
            **kwargs)   
  
    def forward(self, x):
        # input embedding
        x = self.forward_embeddings(x)
        # through backbone
        x = self.forward_tokens(x)
        x = self.norm(x)
        return x
    

class PoolPoses(nn.Module):
    def __init__(self):
        super().__init__()
        model = Backbone()
        backbone = basemodel.poolformer_m48(pretrained=True)
        model.load_state_dict(backbone.state_dict())
        self.backbone = model
        # self.decoder = vanilla_decoder()
        self.decoder = deconv_decoder()
        
    def forward(self, x):
        return self.decoder(self.backbone(x))
        