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

        num_merges = vocab_size - 256

        if num_merges == 0:
            return tokenizer

            print ("reading corpus...")
            all_ids = []
            doc_count = 0
            for text in iterator:
                text_bytes = text.encode("utf-8")
                all_ids.extend(list(text_bytes))
                doc_count += 1

                

        
