from annotator.example_viewer import ExampleViewer

from skimage.io import imread, imshow
from pathlib import Path

if __name__ == "__main__":

    # image_path = parser['image_path']
    # if image_path is not None:
    #     if not Path(image_path).exists():
    #         print("Image path %s not found" % image_path)
    #         image_path = None

    print("Enter frame number to view. Leave blank and hit ENTER to quit.")
    user_input = input("Input number from 0 to 7480: ")
    frame_num = int(user_input)
    print("Showing frame %d..." % frame_num)
    viewer = ExampleViewer()
    viewer.view(frame_num)
