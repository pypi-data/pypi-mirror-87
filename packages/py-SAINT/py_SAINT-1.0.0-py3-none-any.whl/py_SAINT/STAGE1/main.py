import torch
import utility
import data
import data.test
import model.meta_multi
import model
import loss
import os
import sys
from option import args
from trainer import Trainer
os.environ['CUDA_VISIBLE_DEVICES']='3'
print(torch.__version__)
print(sys.version)
print(args)
torch.manual_seed(args.seed)
checkpoint = utility.checkpoint(args)
def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)
if checkpoint.ok:
    loader = data.Data(args)
    print("loader_loadertest---",len(loader.loader_test))
    model = model.Model(args, checkpoint)
    print('number of parameters:', count_parameters(model))    
    loss = loss.Loss(args, checkpoint) if not args.test_only else None
    t = Trainer(args, loader, model, loss, checkpoint)
    while not t.terminate():
        print(1)
        t.train()
        print(2)
        t.test()
        print(3)
    checkpoint.done()

