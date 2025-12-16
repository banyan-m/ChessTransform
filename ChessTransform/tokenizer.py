import json 
import os
import regex

GPT4_PATTERN = r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""


class BPETokenizer:


    def __init__(self):

        self.merges = []

        self.vocab = {i: bytes([i]) for i in range(256)}

        self.pattern = regex.compile(GPT4_PATTERN)

    def _pretokenize(self, text):
        return self.pattern.findall(text)
    
    @classmethod
    def train_from_iterator(cls, iterator, vocab_size=65536):

        assert vocab_size >= 256 

        tokenizer = cls()

        num_merges = vocab_size - 256

        if num_merges == 0:
            return tokenizer

        print("Reading corpus...")
        all_chunks = []
        doc_count = 0
        total_bytes = 0
       
        for text in iterator:
            chunks = tokenizer._pretokenize(text)

            for chunk in chunks:
                chunk_bytes = list(chunk.encode("utf-8"))
                if chunk_bytes:
                    all_chunks.append(chunk_bytes)
                    total_bytes += len(chunk_bytes)
            doc_count += 1
            if doc_count % 1000 == 0:
                print(f"--> processed {doc_count} documents")

        print(f"--> processed {doc_count} documents in total")
        print(f"--> found {total_bytes} total bytes")
        print(f"Learning(num_merges={num_merges})...")

        #train the tokenizer by learning merges, most frequent pairs are merged first
        for i in range(num_merges):

            pair_counts = {}
            for chunk in all_chunks:
                for j in range(len(chunk) - 1):
                    pair = (chunk[j], chunk[j + 1])
                    pair_counts[pair] = pair_counts.get(pair, 0) + 1
            
            if not pair_counts:
                print("--> no pairs found, stopping training")
                break

            #find the most frequent pair of bytes to merge
            best_pair = max(pair_counts, key=pair_counts.get)
            best_count = pair_counts[best_pair]
            
            new_id = 256 + i
            tokenizer.merges.append(best_pair)
            tokenizer.vocab[new_id] = tokenizer.vocab[best_pair[0]] + tokenizer.vocab[best_pair[1]]

            for idx, chunk in enumerate(all_chunks):
                new_chunk = []
                j = 0
                while j < len(chunk):
                    if j < len(chunk) - 1 and chunk[j] == best_pair[0] and chunk[j + 1] == best_pair[1]:
                        new_chunk.append(new_id)
                        j += 2
                    else:
                        new_chunk.append(chunk[j])
                        j += 1
                all_chunks[idx] = new_chunk
            if (i + 1) % 100 == 0:
                total_tokens = sum(len(c) for c in all_chunks)
                print(f"  merge {i + 1}/{num_merges}: {best_pair} → {new_id} (count: {best_count})")

        print(f"Done! Vocabulary size: {len(tokenizer.vocab)}")
        return tokenizer

    def encode(self, text):
        """Encode text to list of token ids."""
        all_ids = []

        chunks = self._pretokenize(text)
        for chunk in chunks:
            ids = list(chunk.encode("utf-8"))

            for merge_idx, pair in enumerate(self.merges):
                new_id = 256 + merge_idx
                new_ids = []
                j = 0
                while j < len(ids):
                    if j < len(ids) - 1 and ids[j] == pair[0] and ids[j + 1] == pair[1]:
                        new_ids.append(new_id)
                        j += 2
                    else:
                        new_ids.append(ids[j])
                        j += 1
                ids = new_ids
            all_ids.extend(ids)
        return all_ids  

            


            
            
    
            
            


            

            


            
                

        
