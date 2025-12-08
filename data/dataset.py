import os 
import pyarrow.parquet as pq

from ChessTransform.common import get_base_dir

base_dir = get_base_dir()
BASE_DIR = os.path.join(base_dir, "chess_data")