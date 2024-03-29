file_name = "EgoCap_nth10.hdf5"
import os.path
import urllib.request
import time
if not os.path.exists(file_name):
    print("Downloading dataset, might take a while... its 400 MB")
    urllib.request.urlretrieve("https://www.cs.ubc.ca/~rhodin/20_CPSC_532R_533R/assignments/"+file_name, file_name)
    print("Done downloading")
else:
    print("Dataset already present, nothing to be done")

import torch
from poolposes_base import PoolPoses
model = PoolPoses()
if torch.cuda.is_available():
    model.cuda()

# download dataset from the web (400 MB file from https://www.cs.ubc.ca/~rhodin/20_CPSC_532R_533R/assignments/EgoCap_nth10.hdf5)
file_name = "EgoCap_nth10.hdf5"
import os.path
import urllib.request
import torch
import torchvision
import torchvision.transforms as transforms
import h5py
import os
from poolposes_base import PoolPoses
from IPython import display


# a function to move tensors from the CPU to the GPU
def dict_to_device(orig, device):
    new = {}
    for k,v in orig.items():
        new[k] = v.to(device)
    return new


class EgoCapDataset(torch.utils.data.Dataset):
    def __init__(self, data_folder):
        super(EgoCapDataset).__init__();
        data_file = 'EgoCap_nth10.hdf5'
        print("Loading dataset to memory, can take some seconds")
        with h5py.File(data_file, 'r') as hf:
            self.poses_2d = torch.from_numpy(hf['pose_2d'][...])
            self.poses_3d = torch.from_numpy(hf['pose_3d'][...])
            self.imgs  = torch.from_numpy(hf['img'][...])
        print(".. done loading")

        self.mean, self.std = torch.FloatTensor([0.485, 0.456, 0.406]), torch.FloatTensor([0.229, 0.224, 0.225])
        self.normalize = transforms.Compose([transforms.Resize((224,224)),
                                              transforms.Normalize(self.mean, self.std)])
        self.denormalize = transforms.Compose([transforms.Resize((128,160)),
                                               transforms.Normalize(mean = [ 0., 0., 0. ], std = 1/self.std),
                                               transforms.Normalize(mean = -self.mean, std = [ 1., 1., 1. ])])

    def __len__(self):
        return self.poses_2d.shape[0]
    
    def __getitem__(self, idx):
        sample = {'img': self.normalize(self.imgs[idx].float()/255),
                  'pose_2d': self.poses_2d[idx],
                  'pose_3d': self.poses_3d[idx]}
        return sample
    
# skeleton pose definition
# Labels are 2D (x, y) coordinate vectors, zero-based starting from the top-left pixel. They appear in the following order: 
joint_names = ['head', 'neck', 'left-shoulder', 'left-elbow', 'left-wrist', 'left-finger', 'right-shoulder', 'right-elbow', 'right-wrist', 'right-finger', 'left-hip', 'left-knee', 'left-ankle', 'left-toe', 'right-hip', 'right-knee', 'right-ankle', 'right-toe']
# the skeleton is defined as a set of bones (pairs of skeleton joint indices):
bones_ego_str = [('head', 'neck'), ('neck', 'left-shoulder'), ('left-shoulder', 'left-elbow'), ('left-elbow', 'left-wrist'), ('left-wrist', 'left-finger'), ('neck', 'right-shoulder'), ('right-shoulder', 'right-elbow'), ('right-elbow', 'right-wrist'), ('right-wrist', 'right-finger'), 
                 ('left-shoulder', 'left-hip'), ('left-hip', 'left-knee'), ('left-knee', 'left-ankle'), ('left-ankle', 'left-toe'), ('right-shoulder', 'right-hip'), ('right-hip', 'right-knee'), ('right-knee', 'right-ankle'), ('right-ankle', 'right-toe'), ('right-shoulder', 'left-shoulder'), ('right-hip', 'left-hip')]
bones_ego_idx = [(joint_names.index(b[0]),joint_names.index(b[1])) for b in bones_ego_str]


# plotting utility functions
import matplotlib.pyplot as plt

r"""Plots skeleton pose on a matplotlib axis.

        Args:
            ax (Axis): plt axis to plot
            pose_2d (FloatTensor): tensor of keypoints, of shape K x 2
            bones (list): list of tuples, each tuple defining the keypoint indices to be connected by a bone 
        Returns:
            Module: self
"""
def plot_skeleton(ax, pose_2d, bones=bones_ego_idx, linewidth=2, linestyle='-', label=None):
    cmap = plt.get_cmap('hsv')
    for i, bone in enumerate(bones):
        color = cmap(bone[1] * cmap.N // len(joint_names)) # color according to second joint index
        if i!=0:
            label=None
        ax.plot(pose_2d[bone,0], pose_2d[bone,1], linestyle, color=color, linewidth=linewidth, label=label)

r"""Plots list of skeleton poses and image.

        Args:
            poses (list): list of pose tensors to be plotted
            ax (Axis): plt axis to plot
            bones (list): list of tuples, each tuple defining the keypoint indices to be connected by a bone 
        Returns:
            Module: self
"""
def plotPosesOnImage(poses, img, ax=plt, labels=None):
    img_pil = torchvision.transforms.ToPILImage()(img)
    img_size = torch.FloatTensor(img_pil.size)
    linestyles = ['-', '--', '-.', ':']
    for i, p in enumerate(poses):
        pose_px = p*img_size
        plot_skeleton(ax, pose_px, linestyle=linestyles[i%len(linestyles)], label=labels[i])
    ax.imshow(img_pil)

r"""Converts a multi channel heatmap to an RGB color representation for display.

        Args:
            heatmap (tensor): of size C X H x W
        Returns:
            image (tensor): of size 3 X H x W
"""
def heatmap2image(heatmap):
    C,H,W = heatmap.shape
    cmap = plt.get_cmap('hsv')
    img = torch.zeros(3,H,W).to(heatmap.device)
    for i in range(C):
        color = torch.FloatTensor(cmap(i * cmap.N // C)[:3]).reshape([-1,1,1]).to(heatmap.device)
        img = torch.max(img, color * heatmap[i]) # max in case of overlapping position of joints
    # heatmap and probability maps might have small maximum value. Normalize per channel to make each of them visible
    img_max, indices = torch.max(img,dim=-1,keepdim=True)
    img_max, indices = torch.max(img_max,dim=-2,keepdim=True)
    return img/img_max

# setting up the dataset and train/val splits
path='/content'
ecds = EgoCapDataset(data_folder=path)

val_ratio = 0.2
val_size = int(len(ecds)*val_ratio)
indices_val = list(range(0, val_size))
indices_train = list(range(val_size, len(ecds)))

val_set   = torch.utils.data.Subset(ecds, indices_val)
train_set = torch.utils.data.Subset(ecds, indices_train)

# define the dataset loader (batch size, shuffling, ...)
train_loader = torch.utils.data.DataLoader(train_set, batch_size = 2, num_workers=0, pin_memory=False, shuffle=True, drop_last=True)
val_loader = torch.utils.data.DataLoader(val_set, batch_size = 2, num_workers=0, pin_memory=False, shuffle=False, drop_last=False)

def integral_heatmap_layer(heatmap):
    # # compute coordinate matrix
    # heatmap = dict['heatmap']
    
    n,k,h,w = heatmap.shape
    heatmap = torch.nn.functional.softmax(heatmap.reshape(n*k,-1), dim=1).reshape(
        (n,k,h,w)
    )
    
    x = torch.linspace(0,1,w).to('cuda')
    y = torch.linspace(0,1,h).to("cuda")
    y = y.reshape(-1,1)
    posex = torch.sum(torch.sum(heatmap * x, dim = 3, keepdim=True), dim =2)
    posey = torch.sum(torch.sum(heatmap * y, dim = 3, keepdim=True), dim =2)
    pose = torch.cat([ posex, posey], dim = 2)

    return {'probabilitymap': heatmap, 'pose_2d': pose}

# DIFFERENT HERE
# init model and put everything in cuda
model = PoolPoses()
if torch.cuda.is_available():
    model.cuda()

optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
fig=plt.figure(figsize=(20, 5), dpi= 80, facecolor='w', edgecolor='k')
axes=fig.subplots(1,3)
losses = []
num_epochs = 5
for e in range(num_epochs):
    train_iter = iter(train_loader)
    for i in range(len(train_loader)):
        batch_cpu = next(train_iter)
        batch_gpu = dict_to_device(batch_cpu,'cuda')
        pred_raw = model(batch_gpu['img'])
        pred_integral = integral_heatmap_layer(pred_raw) # note, this function must be differentiable

        # optimize network
        
        loss = torch.nn.functional.mse_loss(pred_integral['pose_2d'], batch_gpu['pose_2d'])
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
      

        # plot progress
        if i%10==0:
            # clear figures for a new update
            for ax in axes:
                ax.cla()
            pred_cpu = dict_to_device(pred_integral, 'cpu')
            # plot the ground truth and the predicted pose on top of the image
            plotPosesOnImage([pred_cpu['pose_2d'][0].detach(), batch_cpu['pose_2d'][0]], ecds.denormalize(batch_cpu['img'][0]), ax=axes[0], labels=['prediction', 'ground truth label'])
            axes[0].set_title('Input image with predicted pose (solid) and GT pose (dashed)')
            axes[0].legend()

            # plot the predicted probability map and the predicted pose on top
            plotPosesOnImage([pred_cpu['pose_2d'][0].detach()], heatmap2image(pred_cpu['probabilitymap'][0]).detach(), ax=axes[1], labels=['prediction'])
            axes[1].set_title('Predicted probability map with predicted pose overlayed')
            axes[1].legend()

            # plot the current training error on a logplot
            axes[2].plot(losses)
            axes[2].set_yscale('log')
            axes[2].set_title('Training error in log scale')
            axes[2].legend()

            # clear output window and diplay updated figure
            display.clear_output(wait=True)
            display.display(plt.gcf())
            print("Epoch {}, iteration {} of {} ({} %), loss={}".format(e, i, len(train_loader), 100*i//len(train_loader), losses[-1]))
            print("Training for the specified amount of epochs would take long.\nStop the process once you verified that your method works.")
plt.close('all')
