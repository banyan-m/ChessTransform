import os 
import time
import argparse
import torch 
from ChessTransform.tokenizer import BPETokenizer
from ChessTransform.common import get_base_dir
from ChessTransform.datasets import parquetchess_dataset

