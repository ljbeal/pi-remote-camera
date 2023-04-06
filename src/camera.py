import io
from threading import Condition
import picamera2


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


class Camera:

    def __init__(self, rotation: int = 180):
        try:
            self._camera = picamera2.PiCamera2()
            vid_config = self._camera.create_video_configuration()
            self._camera.configure(vid_config)
            encoder = H264Encoder(bitrate=10000000)

            self._camera.rotation = rotation

            self._output = StreamingOutput()
            self._camera.start_recording(encoder, self._output)
        except:
            pass

    def gen(self):
        """Video streaming generator function."""
        if self._camera is None:
            while True:
                yield b'--frame\r\n'

        yield b'--frame\r\n'
        while True:
            with self._output.condition:
                self._output.condition.wait()
                frame = self._output.frame
                yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'

    def stop_recording(self):
        self._camera.stop_recording()
