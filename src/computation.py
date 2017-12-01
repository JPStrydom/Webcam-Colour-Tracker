import numpy as np
import cv2

import config

camera_width = config.camera_width
camera_height = config.camera_height
h_range = config.h_range
sv_range = config.sv_range


def calculate_color_threshold(img_brg):
    img_hsv = cv2.cvtColor(img_brg, cv2.COLOR_BGR2HSV)

    scan_area = img_hsv[
                    round(camera_height / 2) - 10: round(camera_height / 2) + 10,
                    round(camera_width / 2) - 10: round(camera_width / 2) + 10
                ]
    avg_hsv_color = np.mean(np.mean(scan_area, axis=0), axis=0)

    lower_threshold = np.array(
        [
            avg_hsv_color[0] - h_range,
            avg_hsv_color[1] - sv_range,
            avg_hsv_color[2] - sv_range
        ],
        dtype=int
    )
    upper_threshold = np.array(
        [
            avg_hsv_color[0] + h_range,
            avg_hsv_color[1] + sv_range,
            avg_hsv_color[2] + sv_range
        ],
        dtype=int
    )

    avg_brg_color = tuple(cv2.cvtColor(np.uint8([[avg_hsv_color]]), cv2.COLOR_HSV2BGR)[0, 0])

    return lower_threshold, upper_threshold, avg_brg_color


def detect(img_brg, lower_threshold, upper_threshold):
    img_hsv = cv2.cvtColor(img_brg, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(img_hsv, lower_threshold, upper_threshold)

    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

    max_cnt = []
    max_cnt_area = 0
    for h, cnt in enumerate(contours):
        area = int(np.ceil(cv2.contourArea(cnt)))
        if area > max_cnt_area:
            max_cnt = cnt
            max_cnt_area = area

    if len(max_cnt) > 0:
        m = cv2.moments(max_cnt)
        cx = int(m["m10"] / m["m00"])
        cy = int(m["m01"] / m["m00"])
    else:
        return tuple([0, 0])

    return tuple([cx, cy])