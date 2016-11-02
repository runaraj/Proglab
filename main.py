from behavior import CollisionAvoidance
from sensob import sensob

#from basic_robot import *
from motors import Motors
from ultrasonic import Ultrasonic
from zumo_button import ZumoButton
from motob import Motob



def test():
    ZumoButton().wait_for_press()
    ultra = Ultrasonic()
    m = Motors()
    ultra.update()
    tall = ultra.get_value()
    print("tall: ", tall)
    while tall < 5.0:
        m.backward(0.2, 1)
        print(tall)
        ultra.update()
        tall = ultra.get_value()
    print(tall)

def test2():
    motob = Motob(Motors())
    wait = input("Press any key to run L:10")
    motob.update(('L', 10))



def dancer():
    ZumoButton().wait_for_press()
    m = Motors()
    m.forward(.2,3)
    m.backward(.2,3)
    m.right(.5,3)
    m.left(.5,3)
    m.backward(.3,2.5)
    m.set_value([.5,.1],10)
    m.set_value([-.5,-.1],10)
