import pptk
import numpy as np
from pathlib import Path
import annotator.kitti_utils as kitti_utils

# Default KITTI file paths
OBJ_PATH = Path("kitti") / "data_object" / "training"
VELO_PATH = OBJ_PATH / "velodyne"
LABELS_PATH = OBJ_PATH / "label_2"
CALIB_PATH = OBJ_PATH / "calib"
SAVE_PATH = OBJ_PATH / "gt_segmentation"


class Annotator(object):

    def __init__(self, points_path=VELO_PATH, labels_path=LABELS_PATH,
                 calib_path=CALIB_PATH, save_path = SAVE_PATH):
        self.viewer = None
        self.proj = None
        self.points = None
        self.bbox_labels = None
        self.points_path = points_path
        self.labels_path = labels_path
        self.calib_path = calib_path
        self.save_path = save_path
        if not self.save_path.is_dir():
            self.save_path.mkdir(parents=True)


    def load_data(self, frame_num):
        """
        Load in KITTI data and initialize a viewer
        Parameters
        ----------
        frame_num

        Returns
        -------

        """
        # Check valid frame number
        assert 0 <= frame_num <= 7480, "Frame number must be between 0 and 7480"
        self.frame_num = frame_num

        pc = kitti_utils.load_kitti_lidar_data(self.points_path / ("%06d.bin" % frame_num),
                                               load_reflectance=False)
        labels = kitti_utils.load_kitti_labels(self.labels_path / ("%06d.txt" % frame_num))
        self.proj = kitti_utils.KittiProjection.load_file(self.calib_path / ("%06d.txt" % frame_num))
        self.points = pc
        self.bbox_labels = labels
        self.viewer = pptk.viewer(pc)
        self.viewer.set(floor_level=kitti_utils.KITTI_GROUND_LEVEL)
        self.viewer.set(point_size=0.01)
        self.viewer.set(lookat=[0,0,0])


    def annotate(self, frame_num):
        self.load_data(frame_num)

        # Get initial point labels from KITTI bounding boxes
        # Label points which fall inside one of the bounding boxes
        # initial_annotations = [kitti_utils.check_points_in_box(self.points,
        #                                                        self.proj.inverse_transform(label.box_corners()))
        #                        for label in self.bboxlabels]

        self.print_instructions()

        # All points start colored white. Points that have been labeled will turn red
        point_colors = np.array([[0.95,0.95,0.95] for i in range(self.points.shape[0])])

        # Label -1 means background
        instance_labels = np.zeros(self.points.shape[0], dtype=int)
        for (i,object_label) in enumerate(self.bbox_labels):
            self.viewer.attributes(point_colors)
            # Calculate initial point labels from bounding box
            print("Annotating object %d with class '%s'" % (i, object_label.object_type))
            initial_labels = kitti_utils.check_points_in_box(self.points,
                                                             self.proj.inverse_transform(object_label.box_corners()))
            initial_indices = np.where(initial_labels)
            self.viewer.set(selected=initial_indices)
            print("Fix point labels in viewer window. Press ENTER when done.")
            self.viewer.wait()
            annotation = self.viewer.get("selected")
            n_annotated = len(annotation)
            print("Annotated %d points." % n_annotated)
            print("")
            if n_annotated > 0:
                instance_labels[annotation] = i+1
                point_colors[annotation] = np.array([0.85, 0.2, 0.2])

        # Get class labels from instance labels
        class_labels = [self.bbox_labels[i-1].object_type if i > 0 else 'BG' for i in instance_labels]

        # Write labels
        save_file_path = self.save_path / ("%06d.txt" % self.frame_num)
        print("Saving annotation to '%s'" % str(save_file_path))
        if save_file_path.is_file():
            print("Warning: Overwriting existing annotation")
        lines = ["%d %s" % (i, l) for (i,l) in zip(instance_labels, class_labels)]
        with open(save_file_path, "w") as save_file:
            save_file.write('\n'.join(lines))
        self.close()


    def print_instructions(self):
        print("----------------------")
        print("ANNOTATOR INSTRUCTIONS")
        print("----------------------")
        print("Rotate the view by dragging with LMB held down.")
        print("Pan the view around by holding shift and dragging LMB.")
        print("Zoom in/out with mouse wheel.")
        print("")
        print("Select points by holding CMD and dragging a box around points with LMB.")
        print("De-select points by holding CMD+SHIFT and dragging a box with LMB.")
        print("You can also click on individual points while holding CMD or CMD+SHIFT.")
        print("Press ENTER when done to save annotation, and go to next object.")
        print("*Be very careful* not to press RMB. This will de-select all points!")
        print("")
        print("Press C to reset the viewpoint to the mean of the currently selected points,")
        print("  it can be useful to do this when you start annotating a new object.")
        print("You can skip any objects with class 'DontCare'")
        print("")



    def close(self):
        self.viewer.close()
        self.viewer = None


