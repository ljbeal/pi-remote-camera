import time

try:
    # import RPi.GPIO as GPIO
    import pigpio
except ImportError:
    print('could not import gpio library')


class Movement:

    def __init__(self,
                 loop: bool = True):

        self.x = Servo(0, loop)
        self.y = Servo(0, loop)


class Servo:

    _full_travel_time = 0.75  # approx time taken to travel 180°

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

        try:
            print('attempting connection to gpio pins')
            print('if this takes too long, make sure to start the daemon ')
            print('with sudo systemctl start pigpiod')
            self._pi = pigpio.pi()
            self._pi.set_mode(6, pigpio.OUTPUT)
            self._pi.set_PWM_frequency(pin, 50)
        except NameError:
            self._pi = None

        self.angle = init_val

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

        try:
            dtheta = abs(new - self._value)
        except TypeError:
            dtheta = 180

        self._value = new
        self._move_to_angle(self._value, dtheta)

    def _move_to_angle(self, angle, travel=180):

        pmin = 500
        pmax = 2500

        divisor = 180 / (pmax - pmin)

        pw = int(angle / divisor + pmin)

        sleep_time = Servo._full_travel_time * travel / 180

        if self._verbose:
            print(f'moving to angle {angle}, pulsewidth of {pw}. '
                  f'Sleeping for {sleep_time}s before disabling pwm')

        self._pi.set_servo_pulsewidth(self._pin, pw)
        time.sleep(sleep_time)
        self._pi.set_servo_pulsewidth(self._pin, 0)

    def scan(self, n: int = 10):
        for i in range(n + 1):
            angle = i * self._limit/n

            print(f'setting angle to {angle}')
            self.angle = angle
            time.sleep(1)
