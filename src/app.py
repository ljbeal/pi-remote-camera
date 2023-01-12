#!/usr/bin/env python
from flask import Flask, render_template, Response

import io
import picamera
from threading import Condition

import gimbal

app = Flask(__name__)


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        # frame = camera.get_frame()
        with output.condition:
            output.condition.wait()
            frame = output.frame
            yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/move-u')
def move_u():
    print('u')
    gimbal.gimbal.move(x=0, y=gimbal.UP*5)
    return 'u'


@app.route('/move-d')
def move_d():
    print('d')
    gimbal.gimbal.move(x=0, y=-gimbal.UP*5)
    return 'd'


@app.route('/move-l')
def move_l():
    print('l')
    gimbal.gimbal.move(x=-gimbal.RIGHT*5, y=0)
    return 'l'


@app.route('/move-r')
def move_r():
    print('r')
    gimbal.gimbal.move(x=gimbal.RIGHT*5, y=0)
    return 'r'


@app.route('/move-dl')
def move_dl():
    print('dl')
    gimbal.gimbal.move(x=-gimbal.RIGHT*5, y=-gimbal.UP*5)
    return 'dl'


@app.route('/move-dr')
def move_dr():
    print('dr')
    gimbal.gimbal.move(x=gimbal.RIGHT*5, y=-gimbal.UP*5)
    return 'dr'


@app.route('/move-ul')
def move_ul():
    print('ul')
    gimbal.gimbal.move(x=-gimbal.RIGHT*5, y=gimbal.UP*5)
    return 'ul'


@app.route('/move-ur')
def move_ur():
    print('ur')
    gimbal.gimbal.move(x=gimbal.RIGHT*5, y=gimbal.UP*5)
    return 'ur'


@app.route('/move-c')
def move_c():
    print('c')
    gimbal.gimbal.x = 90
    gimbal.gimbal.y = 90
    return 'c'


if __name__ == '__main__':
    with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
        output = StreamingOutput()
        camera.rotation = 180
        camera.start_recording(output, format='mjpeg')

        try:
            app.run(host='0.0.0.0', threaded=True)
        finally:
            camera.stop_recording()
