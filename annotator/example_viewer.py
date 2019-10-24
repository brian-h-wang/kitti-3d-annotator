import numpy as np
from colorsys import hsv_to_rgb
from annotator.annotator import Annotator


class ExampleViewer(Annotator):

    def view(self, frame_num):
        self.load_data(frame_num)
        load_file_path = self.save_path / ("%06d.txt" % self.frame_num)
        with open(load_file_path, "r") as readfile:
            lines = readfile.readlines()
        instance_labels = np.array([int(line.split(" ")[0]) for line in lines])

        # Define random hue color for each instance
        n_instances = np.max(instance_labels)+1
        hues = np.linspace(0,1.0, n_instances)
        np.random.shuffle(hues)
        colors = np.array([hsv_to_rgb(h, 0.7, 0.85)
                          for h in hues])

        colors[0,:] = [0.4,0.4,0.4]

        initial_labels = self.get_initial_labels()
        self.viewer.set(show_axis=False, show_grid=False)
        self.viewer.set(point_size=0.015)
        self.viewer.set(bg_color_bottom=[0.1,0.1,0.1,1.0])

        self.viewer.attributes(colors[initial_labels], colors[instance_labels])
        self.viewer.wait()
        self.viewer.close()

