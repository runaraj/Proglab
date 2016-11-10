from behavior import CollisionAvoidance
from behavior import FollowLine
from sensob import Sensob
from bbcon import BBCON

#from basic_robot import *
from motors import Motors
from irproximity_sensor import IRProximitySensor
from ultrasonic import Ultrasonic
from zumo_button import ZumoButton
from motob import Motob
from reflectance_sensors import ReflectanceSensors
from arbitrator import Arbitrator



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
    sensor = ReflectanceSensors()
    ZumoButton().wait_for_press()
    m = Motors()
    motob = Motob(m)

    sensob = Sensob()
    sensob.set_sensors([sensor])

    behavior = FollowLine(1, [sensob])
    #print("Behavior sensob:", behavior.sensobs)
    count = 0
    while True:
        sensob.update()
        behavior.update()
        #print("MR:", behavior.get_sensob_data())
        #motob.update(behavior.motor_recommendations[0])
        count +=1
        if count==20:
            break

def test5():

    ZumoButton().wait_for_press()
    m = Motors()
    motob = Motob(m)
    sensor = Ultrasonic()

    sensob = Sensob()
    sensob.set_sensors([sensor])

    behavior = CollisionAvoidance(1, [sensob])
    print("Behavior sensob:", behavior.sensobs)
    count = 0
    while True:
        sensob.update()
        behavior.update()
        #print("MR:", behavior.get_sensob_data())
        motob.update(behavior.motor_recommendations[0])
        count +=1
        if count==12:
            break

def systemTest():
    ZumoButton().wait_for_press()
    motor = Motors()
    ultra = Ultrasonic()
    proxim = IRProximitySensor()


    motob = Motob(motor)
    sensob = Sensob()
    sensob.set_sensors([ultra, proxim])
    behavior = CollisionAvoidance(priority=1, sensobs=[sensob])

    arb = Arbitrator(motob=motob)

    bbcon = BBCON(arbitrator=arb, motob=motob)
    bbcon.add_behavior(behavior)
    bbcon.activate_behavior(0)
    bbcon.add_sensob(sensob)
    #print(bbcon)
    #print("behavior", behavior)
    #print("sensob", sensob)
    print(sensob.get_values())


    bbcon.run_one_timestep()

    print(sensob.get_values())
    #print("bbcon", bbcon)
    #print("behavior", behavior)
    #print("sensob", sensob)



def sensorTest():
    ZumoButton().wait_for_press()
    sensor = Ultrasonic()
    count = 0
    while count < 5:
        sensor.update()
        print(sensor.get_value())
        count += 1

