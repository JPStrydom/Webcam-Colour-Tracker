import cv2
import numpy as np

from src import computation
from src import config
from src import draw

camera_width = config.camera_width
camera_height = config.camera_height
h_range = config.h_range
sv_range = config.sv_range

cap = cv2.VideoCapture(0)
cap.set(3, camera_width)
cap.set(4, camera_height)

detect_bool = False


while True:
    ret, frame = cap.read()
    img = np.copy(frame)

    if detect_bool:
        detected_point = computation.detect(img, lower, upper)
        point_array = np.vstack((detected_point, point_array))
        draw.draw_color_line(img, point_array, color)
    else:
        draw.draw_target_circle(img)

    cv2.imshow("Image", img)

    k = cv2.waitKey(1)
    if k == ord("q"):
        break
    elif k == ord("d"):
        detect_bool = not detect_bool
        if detect_bool:
            point_array = np.zeros([1, 2], dtype=tuple)
            lower, upper, color = computation.calculate_color_threshold(img)
    elif k == ord('m'):
        if 'img_draw' not in globals():
            img_draw = np.copy(frame)
            img_draw[:, :] = [255, 255, 255]
        if 'point_array' in globals():
            draw.draw_color_line(img_draw, point_array, color, is_canvas=True)

        cv2.imshow("Draw", img_draw)
    elif k == ord('c'):
        img_draw = np.copy(frame)
        img_draw[:, :] = [255, 255, 255]

        cv2.imshow("Draw", img_draw)

cap.release()
cv2.destroyAllWindows()
