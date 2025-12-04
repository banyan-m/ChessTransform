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
            