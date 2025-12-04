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


