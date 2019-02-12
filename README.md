# KITTI 3D Ground Truth Annotator

This is a tool for creating 3D instance segmentation annotations for the KITTI object detection dataset. The code loads in the KITTI bounding box object annotations and gives points initial labels based on whether they fall within a ground truth bounding box. The user then cleans up the annotations using a point cloud viewer GUI.

The [Point Processing Toolkit](https://github.com/heremaps/pptk) is used for visualization and annotation.

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
        - gt_segmentation/  <- The annotator will create this directory. Output segmentations go here.
```

To start the annotator, just run

```
python main.py
```

Enter the frame number to annotate, and the point cloud viewer will appear. Instructions will appear in the Python terminal window - keep the terminal in view while the point cloud viewer is open. 
