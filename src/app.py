#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response

from gimbal import gimbal

try:
    from camera_pi import Camera
except ImportError:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/move-u')
def move_u():
    print('u')
    gimbal.move(x=0, y=5)
    return 'u'


@app.route('/move-d')
def move_d():
    print('d')
    gimbal.move(x=0, y=-5)
    return 'd'


@app.route('/move-l')
def move_l():
    print('l')
    gimbal.move(x=5, y=0)
    return 'l'


@app.route('/move-r')
def move_r():
    print('r')
    gimbal.move(x=-5, y=0)
    return 'r'


@app.route('/move-c')
def move_c():
    print('c')
    gimbal.x = 90
    gimbal.y = 90
    return 'c'


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
