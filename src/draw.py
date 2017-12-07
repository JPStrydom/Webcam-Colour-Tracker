import cv2

from . import config

camera_width = config.camera_width
camera_height = config.camera_height


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