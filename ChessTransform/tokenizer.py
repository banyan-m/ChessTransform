import json 
import os
import regex



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
                if doc_count % 1000 == 0:
                    print(f"--> processed {doc_count} documents")

        print(f"--> processed {doc_count} documents in total")
        print(f"--> found {len(all_ids)} total bytes")
        print(f"Learning(num_merges={num_merges})...")

        for _ in range(num_merges):

            pair_counts = {}



            
                

        
