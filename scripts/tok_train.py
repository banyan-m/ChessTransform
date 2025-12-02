from typing import Any


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

t0 = time.time()
tokenizer = RustBPETokenizer.train_from_iterator(text_iter, vocab_size=args.vocab_size)
t1 = time.time()
train_time = t1 - t0
print(f"Tokenizer trained in {train_time} seconds")
print(f"Vocab size: {len(tokenizer.get_vocab())}")
print(f"Vocab: {tokenizer.get_vocab()}")

base_dir = get_base_dir()
tokenizer_dir = os.path.join(base_dir, "tokenizer")
tokenizer.save(tokenizer_dir)

#inline sanity check of different cases
test_text = """Hello world, this is a test.
Numbers: 1234567890
Contractions: don't, can't, won't, etc.
Punctuation: !, ?, ., etc.
Special characters: @, #, $, %, etc.
Unicode: 𝑎, 𝑏, 𝑐, etc.
"""
encode = tokenizer.encode(test_text)
decoded= tokenizer.decode(encode)




#We need to cache a mapping from token id to that token's size in bytes, this will help us determine bits per byte.

vocab_size = tokenizer.get_vocab_size()
special_set = set(tokenizer.get_special_tokens())
token_strings = [tokenizer.decode([token_id]) for token_id in range(vocab_size)]
token_bytes = []

for token_id in range(vocab_size):
    token_string = token_strings[token_id]
    if token_string in special_set:
        token_bytes.append(0)

    else:
        id_bytes = len(token_string.encode("utf-8"))
        token_bytes.append(id_bytes)

token_bytes = torch.tensor(token_bytes, dtype=torch.int32, device="cpu")
token_bytes_path = os.path.join(tokenizer_dir, "token_bytes.pt")

with open(token_bytes_path, "wb") as f:
    torch.save(token_bytes, f)
print(f"Token bytes saved to {token_bytes_path}")


