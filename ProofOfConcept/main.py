import argparse
from imports import *
from dataloader.dataloaders import *
# from model.models import *
from utils.utils import *

parser = argparse.ArgumentParser('arguments for training')
parser.add_argument('--data_dir', type=str, default='../data', help='path to dataset directory')
parser.add_argument('--annotation_dir', type=str, default='../data', help='path to dataset directory')
parser.add_argument('--save_dir', type=str, default='../saved_logs', help='path to experiment directory')
parser.add_argument("--dataset", type=str, default='EgoMocap ', choices=['EgoMocap', 'MSCoco', 'MPII'])
parser.add_argument('--img_dim', type=int, default=224)
parser.add_argument("--model", type=str, default='MetaPool', choices=['PoolPose', 'ViT'])
parser.add_argument("--nopretrain", action='store_true')
parser.add_argument('--batch_size', type=int, default=128, help='batch_size')
parser.add_argument('--num_workers', type=int, default=4, help='num of workers to use')
parser.add_argument('--epochs', type=int, default=210, help='number of training epochs')
parser.add_argument("--gpu", action='store_true')
parser.add_argument("--multigpu", action='store_true')
parser.add_argument('--loss_type', default='MSE', type=str, choices=['MSE'], help='Imbalance loss type')
parser.add_argument('--scheduler', default='ADAMW', type=str, choices=['ADAMW'], help='Type of Optimizer')
parser.add_argument('--lr_init', type=float, default=1e-3, help='learning rate')
parser.add_argument('--lr_decay', type=float, default=0.1, help='learning rate decay')
parser.add_argument('--warmup', action='store_true', help='Warmup for the first 5 epochs')
# parser.add_argument('--lr_decay_epochs', type=float, nargs='+', default = [116, 232], help='learning rate decay epochs')
parser.add_argument('--weight_decay', type=float, default=5e-4, help='weight decay')
parser.add_argument('--momentum', type=float, default=0.9, help='momentum')
parser.add_argument("--args_rand", type=int, default=1)
parser.add_argument("--debug", action="store_true")
args = parser.parse_args()


def main():

    torch.set_default_dtype(torch.float32)
    device = torch.device("cuda" if (torch.cuda.is_available() and args.gpu) else "cpu")

    trainloader, valloader, testloader = dataloader_const(args, device)

    optimizer, lr_scheduler, = optimizer_const(args, device)

    # model = model_cont(args, device)
    model = None

    logger = None

    train_val_eval(args, model, trainloader, valloader, testloader, device, optimizer, lr_scheduler, logger)

if __name__ == '__main__':
    main()