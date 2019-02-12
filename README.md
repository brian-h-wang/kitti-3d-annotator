#KITTI 3D Ground Truth Annotator

# How to use

Install requirements with pip

```
pip install -r requirements.txt
```

Download the KITTI object detection dataset, or if you already have it downloaded, modify the paths in `config.py` to point to the locations of the directories for Velodyne data, ground truth labels, calibration, and saved segmentation annotation outputs.

Default folder structure looks like this:

```
PROJECT_ROOT/
  - kitti/
    - data_object/
      - training/
        - calib/
        - image_2/
        - label_2/
        - velodyne/
        - gt_segmentation/  <- The annotator will create this directory
```

To start the annotator, just run

```
python main.py
```

Enter the frame number to annotate, and the point cloud viewer will appear. Instructions will appear in the Python terminal window - keep the terminal in view while the point cloud viewer is open. 
