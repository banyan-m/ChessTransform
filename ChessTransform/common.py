import os

def get_base_dir():

    if os.environ.get("CHESSTRANSFORM_BASE_DIR"):
        base_dir = os.environ.get("CHESSTRANSFORM_BASE_DIR")

    else:
        home_dir = os.path.expanduser("~")
        cache_dir = os.path.join(home_dir, ".cache")
        base_dir = os.path.join(cache_dir, "ChessTransform")
    
    os.makedirs(base_dir, exist_ok=True)
    return base_dir
   

