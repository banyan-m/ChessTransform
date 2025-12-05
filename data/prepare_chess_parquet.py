import os 
import argparse

import pyarrow as pa
import pyarrow.parquet as pq


def iter_pgn_games(path):
    
    """ Yields one PGN game at a time from a single file"""

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        game_lines = []
        for raw_line in f:
            line = raw_line.rstrip("\n")

            if line.strip() == "" and game_lines:
                yield game_lines
                game_lines = []
            
            else:
                if line.strip() == "" and not game_lines:
                    continue
                game_lines.append(line)

        if game_lines:
            yield game_lines


def iter_all_games(in_dir):

    for filename in sorted(os.listdir(in_dir)):
        if not filename.endswith(".pgn"):
            continue
        path = os.path.join(in_dir, filename)

        for game_lines in iter_pgn_games(path):
            yield game_lines


def parse_game(game_lines):
    headers = [l for l in game_lines if l.startswith("[")]
    result = None
    for h in headers:
        if h.startswith("[Result"):
            parts = h.split('"')
            if len(parts) >= 2:
                result = parts[1]
                break
    if result not in ["1-0", "0-1", "1/2-1/2"]:
        return None

    moves_lines = [
        l for l in game_lines
        if not l.startswith("[") and l.strip()
    ]

    if not moves_lines:
        return None

    moves_str = " ".join(" ".join(moves_lines).split())

    text = f"[RESULT: {result}] {moves_str}"
    return text, result

def process_pgn_dir(in_dir, out_dir, max_games_per_shard=1000000):

    os.makedirs(out_dir, exist_ok=True)
    shard_idx = 0
    texts, results = [], []

    def flush_shard():
        nonlocal shard_idx, texts, results
        if not texts:
            return
        table = pa.Table.from_pydict({"text": texts, "result": results})
        out_path = os.path.join(out_dir, f"shard_{shard_idx:05d}.parquet")
        pq.write_table(table, out_path)
        print(f"--> wrote {len(texts)} games to {out_path}")
        shard_idx += 1
        texts, results = [], []

    total_games = 0
    for game_lines in iter_all_games(in_dir):
        parsed = parse_game(game_lines)
        
        if parsed is None:
            continue
        text, result = parsed
        texts.append(text)
        results.append(result)
        total_games += 1

        if len(texts) >= max_games_per_shard:
            flush_shard()

    
    flush_shard()
    print(f"--> processed {total_games} games in total")
    print(f"--> wrote {shard_idx} shards to {out_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        