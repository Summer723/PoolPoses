import torch
from basemodel import PoolFormer

class PoolPoses(PoolFormer):
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
        if self.fork_feat:
            # otuput features of four stages for dense prediction
            return x
        x = self.norm(x)
        # cls_out = self.head(x.mean([-2, -1]))
        # for image classification
        return x