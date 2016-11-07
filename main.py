from behavior import CollisionAvoidance
from sensob import Sensob

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

def test3():
    ZumoButton().wait_for_press()
    m = Motors()
    m.set_value((1,0), dur=2)



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


def test4():
    ZumoButton().wait_for_press()
    m = Motors()
    motob = Motob(m)
    sensor = Ultrasonic()
    sensob = Sensob()
    sensob.set_sensors([sensor])

    behavior = CollisionAvoidance(priority=1, sensobs=[sensob])
    print("Behavior sensob:", behavior.sensobs)
    count = 0
    while True:
        behavior.update()
        motob.update(behavior.motor_recommendations[0])
        count +=1
        if count==6:
            break

