from src.kinematics import Servo

a = Servo(19)
b = Servo(18)

a.scan()
b.scan()

a.angle = 90
b.angle = 90
