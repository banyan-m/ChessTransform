import json 
import os



class BPETokenizer:


    def __init__(self):

        self.merges = []

        self.vocab = {i: bytes([i]) for i in range(256)}

    @classmethod
    def train_from_iterator(cls, iterator, vocab_size=65536):

        assert vocab_size >= 256 

        tokenizer = cls()
