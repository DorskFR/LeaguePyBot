import cv2
from .peripherals import Vision


class Display:
    def __init__(self):
        self.vision = Vision(
            {"top": 850, "left": 1920, "width": 500, "height": 200}, ratio=0.25
        )

    def show_grid(self):
        # loop_time = time()
        while True:
            self.vision.capture_window()
            self.vision.draw_grid(text=True)
            cv2.imshow("screen", self.vision.sct_img)
            # print("FPS {}".format(round(1 / (time() - loop_time), 2)))
            # loop_time = time()

            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                cv2.destroyAllWindows()
                break
