from annotator.annotator import Annotator
import argparse

from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--order_file", help="path to order file", default=None)
    A = Annotator()

    args = parser.parse_args()
    order_file = args.order_file
    if order_file is not None:
        if not Path(order_file).exists():
            print("Order file %s not found" % order_file)
            order = None
        else:
            with open(order_file, "r") as f:
                order = [int(l) for l in f.readlines()]
    else:
        order = None

    if order is None:
        while True:
            print("Enter frame number to annotate. Leave blank and hit ENTER to quit.")
            user_input = input("Input number from 0 to 7480: ")
            try:
                frame_num = int(user_input)
            except ValueError:
                print("Exiting!")
                break
            print("Annotating frame %d..." % frame_num)
            A.annotate(frame_num)
    else:
        next_frame = None
        print("Enter first frame number to annotate. Leave blank and hit ENTER to quit.")
        user_input = input("Input number from 0 to 7480: ")
        try:
            frame_num = int(user_input)
            next_frame = order.index(frame_num)
            exit = False
        except ValueError:
            exit = True
        while not exit:
            frame_num = order[next_frame]
            print("Annotating frame %d..." % frame_num)
            A.annotate(frame_num)
            user_input = input("Hit ENTER to continue, or enter 'q' to quit.")
            if user_input.startswith("q") or user_input.startswith("Q"):
                exit = True
            next_frame += 1
        print("Exiting!")
        fig.close()
