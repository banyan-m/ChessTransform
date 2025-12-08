import os 
import pyarrow.parquet as pq

from ChessTransform.common import get_base_dir

base_dir = get_base_dir()
DATA_DIR = os.path.join(base_dir, "chess_data")
os.makedirs(DATA_DIR, exist_ok=True)

def list_parquet_files(data_dir=None):

    data_dir = DATA_DIR if data_dir is None else data_dir
    parquet_files = [f for f in os.listdir(data_dir) if f.endswith(".parquet")]
    parquet_paths = [os.path.join(data_dir, f) for f in parquet_files]

    return parquet_paths

def parquets_iter_batched(split, start=0, step=1, with_results=False):
    
    assert split in ["train", "val"], "split must be either train or val"
    parquet_paths = list_parquet_files()
    parquet_paths = parquet_paths[:-1] if split == "train" else parquet_paths[-1:]

    for file_path in parquet_paths:
        pf = pq.ParquetFile(file_path)
        for rg_idx in range(start, pf.num_row_groups, step):
            rg = pf.read_row_group(rg_idx)

    



