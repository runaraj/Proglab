import time
from camera import Camera

class BBCON:
    #Instance variables
    behaviors = [] # a list of all the behavior objects used by the bbcon
    active_behaviors = [] #a list of all behaviors that are currently active
    sensobs = [] #a list of all sensory objects used by the bbcon
    motobs = [] #a list of all motor objects used by the bbcon
    arbitrator = None #the arbitrator object that will resolve actuator requests produced by the behaviors.
    right = False
    left = False #disse settes av collisionAvoidance, men brukes av alle slik at en annen behavior ikke kan svinge inn i en vegg
    camera = False
    halt = False

    def get_halt_request(self):
        self.halt = True


    def activate_camera(self):
        self.camera = True
    def deactivate_camera(self):
        self.camera = False

    def __init__(self, arbitrator, motob):
        self.arbitrator = arbitrator
        self.motobs.append(motob)
        self.arbitrator.set_bbcon(bbcon=self)

    def add_behavior(self, behavior):#append a newly-created behavior onto the behaviors list.
        self.behaviors.append(behavior)

    def add_sensob(self, sensob):#append a newly-created sensob onto the sensobs list.
        self.sensobs.append(sensob)

    def activate_behavior(self,behaviorIndex):#add an existing behavior onto the active-behaviors list.
        try:
            self.active_behaviors.append(self.behaviors[behaviorIndex])
        except IndexError:
            print("No such behavior")
            pass

    def wait(self,seconds):
        time.sleep(seconds)

    def deactivate_behavior(self, behavior):#remove an existing behavior from the active behaviors list.
        try:
            self.active_behaviors.remove(behavior)
        except IndexError:
            print("Invalid index")
            pass

    def run_one_timestep(self):
        #Should perform at least the following actions each calls:
        #Update all sensobs, behaviors. Invoke arbitrator.choose_action
        #Update motobs, wait, reset sensobs

        for sens in self.sensobs:
            if isinstance(sens, Camera) and not self.camera:
                continue
            sens.update()

        for behav in self.behaviors:
            behav.update()

        if self.halt:
            exit()
        else:
            self.arbitrator.update_active_list()
            motor_recomm = self.arbitrator.choose_action()
        print(motor_recomm)

        #OBS! Motor programmet "pauser" mens motoren er igang
        #finnes fiks til dette?
        for motob in self.motobs:
            motob.update(motor_recomm)

        waitSeconds = 1
        self.wait(waitSeconds)

        for sens in self.sensobs:
            sens.reset_sensors