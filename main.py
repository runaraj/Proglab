from behavior import CollisionAvoidance
from behavior import FollowLine
from behavior import TrackObject
from sensob import Sensob
from bbcon import BBCON
from imager2 import Imager

import time

# from basic_robot import *
from motors import Motors
from irproximity_sensor import IRProximitySensor
from ultrasonic import Ultrasonic
from zumo_button import ZumoButton
from motob import Motob
from reflectance_sensors import ReflectanceSensors
from arbitrator import Arbitrator
from camera import Camera


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

def test45():
    ZumoButton().wait_for_press()
    sensor = IRProximitySensor()
    count = 0
    while count < 10:
        sensor.update()
        print(sensor.get_value())
        count += 1
        time.sleep(2.5)

def test4():
    sensor = ReflectanceSensors()
    ZumoButton().wait_for_press()
    m = Motors()
    motob = Motob(m)

    sensob = Sensob()
    sensob.set_sensors([sensor])
    print(sensor.get_value())
    behavior = FollowLine(1, [sensob])
    #print("Behavior sensob:", behavior.sensobs)
    count = 0
    while True:
        sensob.update()
        behavior.update()
        print("MR:", behavior.motor_recommendations)
        motob.update(behavior.motor_recommendations[0])
        count += 1
        #time.sleep(3)
        if count == 15:
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
def runTimesteps(bbcon, timesteps):
    timestepNo = 0
    ZumoButton().wait_for_press()
    while timestepNo < timesteps:
        bbcon.run_one_timestep()
        timesteps += 1


def systemTest():

    motor = Motors()
    ultra = Ultrasonic()
    proxim = IRProximitySensor()


    motob = Motob(motor)
    arbitrator =Arbitrator(motob=motob)

    sensob = Sensob()
    sensob.set_sensors([ultra, proxim])



    bbcon = BBCON(arbitrator=arbitrator, motob=motob)
    b = CollisionAvoidance(priority=1, sensobs=[sensob])
    bbcon.add_behavior(b)

    bbcon.activate_behavior(0)
    bbcon.add_sensob(sensob)

    while True:
        runTimesteps(bbcon,15)






def sensorTest():
    ZumoButton().wait_for_press()
    sensor = Ultrasonic()
    count = 0
    while count < 5:
        sensor.update()
        print(sensor.get_value())
        count += 1

def camTest():
    ZumoButton().wait_for_press()
    sensor = Camera(img_width=128, img_height=96, img_rot=0) #endre disse?
    sensor2 = Camera(img_width=256, img_height=192, img_rot=0)
    sensor3 = Camera(img_width=512, img_height=384, img_rot=0)
    sensor4 = Camera(img_width=1024, img_height=768, img_rot=0)


    sensor.update()
    sensor2.update()
    sensor3.update()
    sensor4.update()
    pic = sensor.get_value()
    pic2 = sensor2.get_value()
    pic3 = sensor3.get_value()
    pic4 = sensor4.get_value()
    b = Imager()
    b.image = pic
    b.dump_image("test", type="JPEG") #dump as jpeg/jpg/gif?
    b.image = pic2
    b.dump_image("test2", type="JPEG")
    b.image = pic3
    b.dump_image("test3", type="JPEG")
    b.image = pic4
    b.dump_image("test4", type="JPEG")


def trackTest():
    ZumoButton().wait_for_press()
    motor = Motors()
    ultra = Ultrasonic()
    camera = Camera()

    motob = Motob(motor)
    arbitrator = Arbitrator(motob=motob)

    sensob = Sensob()
    sensob.set_sensors([ultra, camera])

    bbcon = BBCON(arbitrator=arbitrator, motob=motob)
    b = TrackObject(priority=1, sensobs=[sensob])
    bbcon.add_behavior(b)

    bbcon.activate_behavior(0)
    bbcon.add_sensob(sensob)

    timesteps = 0
    while timesteps < 15:

        bbcon.run_one_timestep()
        timesteps += 1
