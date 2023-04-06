import io
from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class Camera:

    def __init__(self, rotation: int = 180):
        try:
            self._camera = Picamera2()
            vid_config = self._camera.create_video_configuration()
            self._camera.configure(vid_config)
            encoder = JpegEncoder(num_threads=2)

            self._camera.rotation = rotation

            self._output = StreamingOutput()
            self._camera.start_recording(encoder, FileOutput(self._output))
        except Exception as E:
            print('could not init camera')
            raise E

    def gen(self):
        """Video streaming generator function."""
        if self._camera is None:
            while True:
                yield b'--frame\r\n'

        yield b'--frame\r\n'
        while True:
            frame = self._output.frame
            yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'

    def stop_recording(self):
        self._camera.stop_recording()
