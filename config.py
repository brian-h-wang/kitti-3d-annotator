from pathlib import Path

OBJ_PATH = Path("kitti") / "data_object" / "training"
VELO_PATH = OBJ_PATH / "velodyne"
LABELS_PATH = OBJ_PATH / "label_2"
CALIB_PATH = OBJ_PATH / "calib"
SAVE_PATH = OBJ_PATH / "gt_segmentation"