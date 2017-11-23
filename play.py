import numpy as np
import cv2

camera_width = 1280
camera_height = 720

cap = cv2.VideoCapture(0)

cap.set(3, camera_width)
cap.set(4, camera_height)

detect_bool = False

play_array = np.zeros([1, 2], dtype=tuple)
img_draw = []

tolerance = 0.15


def calculate_color_threshold(img_rgb):
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)

    scan_area = img_hsv[round(camera_height / 2) - 10: round(camera_height / 2) + 10,
                        round(camera_width / 2) - 10: round(camera_width / 2) + 10]
    avg_hsv_color = np.mean(np.mean(scan_area, axis=0), axis=0)

    lower_threshold = np.array(avg_hsv_color * (1 - tolerance), dtype=int)
    upper_threshold = np.array(avg_hsv_color * (1 + tolerance), dtype=int)

    avg_rgb_color = tuple(cv2.cvtColor(np.uint8([[avg_hsv_color]]), cv2.COLOR_HSV2BGR)[0, 0])

    return lower_threshold, upper_threshold, avg_rgb_color


def detect(img_rgb, lower_threshold, upper_threshold):
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)

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


while True:
    ret, frame = cap.read()
    img = np.copy(frame)

    if detect_bool:
        d = detect(img, lower, upper)
        play_array = np.vstack((d, play_array))
        for i, p in enumerate(play_array):
            if i <= 25 and p[0] != 0 and p[1] != 0 and play_array[i + 1, 0] != 0 and play_array[i + 1, 1] != 0:
                cv2.line(img, tuple(p), tuple(play_array[i + 1]),
                         (0, 0, 0), 50 - i * 2 + 10)
        for i, p in enumerate(play_array):
            if i <= 25 and p[0] != 0 and p[1] != 0 and play_array[i + 1, 0] != 0 and play_array[i + 1, 1] != 0:
                cv2.line(img, tuple(p), tuple(play_array[i + 1]),
                         (int(color[0]), int(color[1]), int(color[2])), 50 - i * 2)
    else:
        cv2.circle(img, (round(camera_width / 2), round(camera_height / 2)), 25, (0, 0, 0), 10)
        cv2.circle(img, (round(camera_width / 2), round(camera_height / 2)), 25, (255, 255, 255), 6)
        cv2.circle(img, (round(camera_width / 2), round(camera_height / 2)), 25, (0, 0, 0), 2)

    cv2.imshow("Image", img)

    k = cv2.waitKey(1)
    if k == ord("q"):
        break
    elif k == ord("d"):
        detect_bool = not detect_bool
        if detect_bool:
            play_array = np.zeros([1, 2], dtype=tuple)
            lower, upper, color = calculate_color_threshold(img)
    elif k == ord('m'):
        if len(img_draw) < 1:
            img_draw = np.copy(frame)
            img_draw[:, :] = [255, 255, 255]
        for i, p in enumerate(play_array):
            if p[0] != 0 and p[1] != 0 and play_array[i + 1, 0] != 0 and play_array[i + 1, 1] != 0:
                cv2.line(img_draw, tuple(p), tuple(play_array[i + 1]),
                         (0, 0, 0), round(50 - i * (50 / len(play_array)) + 10))
        for i, p in enumerate(play_array):
            if p[0] != 0 and p[1] != 0 and play_array[i + 1, 0] != 0 and play_array[i + 1, 1] != 0:
                cv2.line(img_draw, tuple(p), tuple(play_array[i + 1]),
                         (int(color[0]), int(color[1]), int(color[2])), round(50 - i * (50 / len(play_array))))

        cv2.imshow("Draw", img_draw)
    elif k == ord('c'):
        img_draw = np.copy(frame)
        img_draw[:, :] = [255, 255, 255]

        cv2.imshow("Draw", img_draw)

cap.release()
cv2.destroyAllWindows()
