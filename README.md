# Webcam-Colour-Tracker

## Introduction

This is a simple Python application that tracks any user defined colour through a web-camera in real-time. Users can also chose to draw the colours they track onto a blank canvas.

## Links

- The project's GitHub repository can be found [here](https://github.com/JPStrydom/Webcam-Colour-Tracker)
- A guide to getting started with OpenCV in Python can be found [here](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_tutorials.html)

## Setup

If you'd like to run this project yourself, you can follow the following steps:

1) Clone the repository, or simply download the source code [here](https://github.com/JPStrydom/Webcam-Colour-Tracker/archive/master.zip)
2) Download and install the latest version of Python 3 for you OS [here](https://www.python.org/downloads/)
3) Add the following to your environmental `path` variable:
    - Windows:
        - `C:\Users\(username)\AppData\Local\Programs\Python\Python36-32`
        - `C:\Users\(username)\AppData\Local\Programs\Python\Python36-32\Scripts`
    - Linux:
        - ``
        - ``
4) Run the command `pip install numpy` in the same directory as the source code to install the numpy package
5) Run the command `pip install opencv_python` in the same directory as the source code to install the OpenCV package
6) Run the `play.py` file to start the program

The controls for the application are as follows:
- **`q`** - Quit and close the application (You can only use one instance of the application per web-camera, else it will crash)
- **`d`** - Sample and track the average colour inside the target area (indicated by the white circle on the web-camera output) / Stop tracking the current colour
- **`m`** - Draw the last tracked colour on a the canvas (if no canvas is open, it'll open one for you)
- **`c`** - Clear the canvas