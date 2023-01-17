#!/usr/bin/env python
from flask import Flask, render_template, Response

from gimbal import gimbal, UP, RIGHT
from camera import Camera

app = Flask(__name__)
cam = Camera(180)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(cam.gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/move-u')
def move_u():
    print('u')
    gimbal.move(x=0, y=UP*5)
    return 'u'


@app.route('/move-d')
def move_d():
    print('d')
    gimbal.move(x=0, y=-UP*5)
    return 'd'


@app.route('/move-l')
def move_l():
    print('l')
    gimbal.move(x=-RIGHT*5, y=0)
    return 'l'


@app.route('/move-r')
def move_r():
    print('r')
    gimbal.move(x=RIGHT*5, y=0)
    return 'r'


@app.route('/move-dl')
def move_dl():
    print('dl')
    gimbal.move(x=-RIGHT*5, y=-UP*5)
    return 'dl'


@app.route('/move-dr')
def move_dr():
    print('dr')
    gimbal.move(x=RIGHT*5, y=-UP*5)
    return 'dr'


@app.route('/move-ul')
def move_ul():
    print('ul')
    gimbal.move(x=-RIGHT*5, y=UP*5)
    return 'ul'


@app.route('/move-ur')
def move_ur():
    print('ur')
    gimbal.move(x=RIGHT*5, y=UP*5)
    return 'ur'


@app.route('/move-c')
def move_c():
    print('c')
    gimbal.x = 90
    gimbal.y = 90
    return 'c'


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
