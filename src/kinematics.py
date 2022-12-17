import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    print('could not import RPi.GPIO')


class Movement:

    def __init__(self,
                 loop: bool = True):

        self.x = Servo(0, loop)
        self.y = Servo(0, loop)


class Servo:

    def __init__(self,
                 pin: int,
                 init_val: float = 90.0,
                 limit: float = 180.0,
                 loop: bool = True,
                 verbose: bool = False):

        self._value = None
        self._limit = limit
        self._loop = loop
        self._verbose = verbose

        self._pin = pin
        self.angle = init_val

        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(pin, GPIO.OUT)
            self._pwm = GPIO.PWM(pin, 50)
            self._pwm.start(0)
        except NameError:
            self._pwm = None

    def __add__(self, other):
        self.angle = self.angle + other
        return self

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        self.angle = self.angle - other
        return self

    def __isub__(self, other):
        return self.__sub__(other)

    def __float__(self):
        return self.angle

    def __repr__(self):
        return str(self.angle)

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, new):
        self._verbose = new

    @property
    def angle(self):
        return float(self._value)

    @angle.setter
    def angle(self, new):
        if new > self._limit:
            if self._loop:
                new = new - self._limit
            else:
                new = self._limit

        self._value = new
        self._set_angle(self._value)

    def sleep(self):
        self._pwm.ChangeDutyCycle(0)

    def _set_angle(self, angle):
        # set angle for range
        dcmin = 2.5
        dcmax = 12.5

        divisor = 180/(dcmax - dcmin)

        dcycle = angle / divisor + dcmin

        try:
            if self.verbose:
                print(f'angle {angle}°, setting duty cycle to {dcycle:.2f}')
            self._pwm.ChangeDutyCycle(dcycle)

        except AttributeError:
            pass

    def scan(self, n: int = 10):
        for i in range(n + 1):
            angle = i * self._limit/n

            print(f'setting angle to {angle}')
            self.angle = angle
            time.sleep(1)
