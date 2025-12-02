import os 
import time
import argparse
import torch 
from ChessTransform.tokenizer import BPETokenizer
from ChessTransform.common import get_base_dir
from ChessTransform.datasets import parquetchess_dataset

parser = argparse.ArgumentParser(
    description="Train a tokenizer for the ChessTransform dataset"
)
parser.add_argument("--max_chars", type=int, default=10_000_000_000, help="Maximum number of characters to use for training (default 10b)")
parser.add_argument("--doc_cap", type=int, default=10_000, help="Maximum char per document (deafult 10k)")
parser.add_argument("--vocab_size", type=int, default=65536, help="Vocab size (default 65536)")
f"Max chars: {args.max_chars}, Doc cap: {args.doc_cap}, Vocab size: {args.vocab_size}"
print(f"Max chars: {args.max_chars}, Doc cap: {args.doc_cap}, Vocab size: {args.vocab_size}")

def text_iterator():
    nchars = 0
    for batch in parquetchess_iter_batched(split="train"):
        for doc in batch:
            doc_text = doc
            if len(doc_text) > args.doc_cap:
                doc_text = doc_text[:args.doc_cap]
            nchars += len(doc_text)
            yield doc_text
            if nchars >= args.max_chars:
                return
text_iter = text_iterator()



