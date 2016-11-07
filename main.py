from behavior import CollisionAvoidance
from sensob import sensob

# from basic_robot import *
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
    ZumoButton().wait_for_press()
    motob = Motob(Motors())
    deg = input("Skriv antall grader: ")
    dir = input("Skriv retning L/R: ")
    motob.update((dir, int(deg)))


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
    M = Motob(m)
    s = Ultrasonic()
    S = sensob()
    S.set_sensors([s])
    b = CollisionAvoidance(1, S)
    while True:
        b.update()
        M.update(b.motor_recommendations[0])