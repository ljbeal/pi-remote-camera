from .kinematics import Servo


RIGHT = -1
UP = -1


class control:

    def __init__(self, azpin, elpin):
        self._az = Servo(azpin)
        self._el = Servo(elpin)

        self._el.angle = 90
        self._az.angle = 90

    def move(self, x, y):
        self.x = self.x + x
        self.y = self.y + y

    @property
    def x(self):
        return self._az.angle

    @x.setter
    def x(self, newx):
        self._az.angle = newx

        print(f'x is now {self.x}')

    @property
    def y(self):
        return self._el.angle

    @y.setter
    def y(self, newy):
        self._el.angle = newy

        print(f'y is now {self.y}')


gimbal = control(19, 18)
