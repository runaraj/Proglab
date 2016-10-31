from behavior import CollisionAvoidance
import motob
from sensob import Sensob
import arbitrator
import bbcon
import basic_robot
from motors import Motors



if __name__ == '__main__':

    ultraSonic = basic_robot.ultrasonic.Ultrasonic()
    m = Motors()
    FrontDistance = Sensob()
    FrontDistance.set_sensors(ultraSonic)

    FrontCollision = CollisionAvoidance(1, FrontDistance)

    while FrontCollision.update() < 4.0:
        m.backward(0.2, 3)

    




