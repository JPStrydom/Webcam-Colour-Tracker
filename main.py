import numpy as np
import cv2

camera_width = 1280
camera_height = 720

cap = cv2.VideoCapture(0)
cap.set(3, camera_width)
cap.set(4, camera_height)

detect_bool = False

h_range = 5
sv_range = 100


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


def draw_color_line(img_brg, draw_point_array, draw_color, is_canvas=False):
    draw_color_line_help(img_brg, draw_point_array, (0, 0, 0), is_canvas)
    draw_color_line_help(img_brg, draw_point_array, draw_color, is_canvas)


def draw_color_line_help(img_brg, draw_point_array, draw_color, is_canvas=False):
    padding = 0
    if draw_color == (0, 0, 0):
        padding = 10

    taper_rate = 2
    if is_canvas:
        taper_rate = (50 / len(draw_point_array))

    for index, point in enumerate(draw_point_array):
        if validate_point(index, point, draw_point_array, is_canvas):
            cv2.line(
                img_brg,
                tuple(point),
                tuple(draw_point_array[index + 1]),
                (int(draw_color[0]), int(draw_color[1]), int(draw_color[2])),
                round(50 - index * taper_rate + padding)
            )


def validate_point(index, point, draw_point_array, is_canvas):
    return (index <= 25 or is_canvas) and\
           point[0] != 0 and\
           point[1] != 0 and\
           draw_point_array[index + 1, 0] != 0 and\
           draw_point_array[index + 1, 1] != 0


def draw_target_circle(img_brg):
    cv2.circle(img_brg, (round(camera_width / 2), round(camera_height / 2)), 25, (0, 0, 0), 10)
    cv2.circle(img_brg, (round(camera_width / 2), round(camera_height / 2)), 25, (255, 255, 255), 6)
    cv2.circle(img_brg, (round(camera_width / 2), round(camera_height / 2)), 25, (0, 0, 0), 2)


while True:
    ret, frame = cap.read()
    img = np.copy(frame)

    if detect_bool:
        detected_point = detect(img, lower, upper)
        point_array = np.vstack((detected_point, point_array))
        draw_color_line(img, point_array, color)
    else:
        draw_target_circle(img)

    cv2.imshow("Image", img)

    k = cv2.waitKey(1)
    if k == ord("q"):
        break
    elif k == ord("d"):
        detect_bool = not detect_bool
        if detect_bool:
            point_array = np.zeros([1, 2], dtype=tuple)
            lower, upper, color = calculate_color_threshold(img)
    elif k == ord('m'):
        if 'img_draw' not in globals():
            img_draw = np.copy(frame)
            img_draw[:, :] = [255, 255, 255]
        if 'point_array' in globals():
            draw_color_line(img_draw, point_array, color, is_canvas=True)

        cv2.imshow("Draw", img_draw)
    elif k == ord('c'):
        img_draw = np.copy(frame)
        img_draw[:, :] = [255, 255, 255]

        cv2.imshow("Draw", img_draw)

cap.release()
cv2.destroyAllWindows()
