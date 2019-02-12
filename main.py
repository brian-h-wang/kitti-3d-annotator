from annotator.annotator import Annotator

if __name__ == "__main__":
    A = Annotator()
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
