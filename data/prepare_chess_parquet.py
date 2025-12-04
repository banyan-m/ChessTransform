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