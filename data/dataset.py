import os 
import pyarrow.parquet as pq

from ChessTransform.common import get_base_dir

base_dir = get_base_dir()
DATA_DIR = os.path.join(base_dir, "chess_data")
os.makedirs(DATA_DIR, exist_ok=True)

def list_parquet_files(data_dir=None):
    data_dir = DATA_DIR if data_dir is None else data_dir

