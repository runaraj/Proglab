import time

class BBCON:
    #Instance variables
    behaviors = [] # a list of all the behavior objects used by the bbcon
    active_behaviors = [] #a list of all behaviors that are currently active
    sensobs = [] #a list of all sensory objects used by the bbcon
    motobs = [] #a list of all motor objects used by the bbcon
    arbitrator = None #the arbitrator object that will resolve actuator requests produced by the behaviors.

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

    def deactivate_behavior(self, behaviorIndex):#remove an existing behavior from the active behaviors list.
        try:
            self.active_behaviors.remove(behaviorIndex)
        except IndexError:
            print("Invalid index")
            pass

    def run_one_timestep(self):
        #Should perform at least the following actions each calls:
        #Update all sensobs, behaviors. Invoke arbitrator.choose_action
        #Update motobs, wait, reset sensobs
        for sens in self.sensobs:
            sens.update

        #TODO behaviors

        self.arbitrator.choose_action

        for motor in self.motobs:
            #motor.update

        waitSeconds = 1
        self.wait(waitSeconds)

        for sens in self.sensobs:
            sens.reset_sensors