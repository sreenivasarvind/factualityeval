import argparse
import json

import torch
from torch import nn, optim
from torch.autograd import Variable

import logging
from bert_dataloader import *
from scibert import *
from transformers import *

model = SciBertForRanking()
ckpt = torch.load('model/abstract_scibert_mlm/pytorch_model.bin')
model.load_state_dict(ckpt)
