class BBCON:
    #Instance variables
    behaviors = [] # a list of all the behavior objects used by the bbcon
    active_behaviors = [] #a list of all behaviors that are currently active
    sensobs = [] #a list of all sensory objects used by the bbcon
    motobs = [] #a list of all motor objects used by the bbcon
    arbitrator = None #the arbitrator object that will resolve actuator requests produced by the behaviors.

    def add_behavior(self):#append a newly-created behavior onto the behaviors list.
        pass

    def add_sensob(self):#append a newly-created sensob onto the sensobs list.
        pass

    def activate_behavior(self):#add an existing behavior onto the active-behaviors list.
        pass

    def deactivate_behavior(self):#remove an existing behavior from the active behaviors list.
        pass

    def run_one_timestep(self):
        #Should perform at least the following actions each calls:
        #Update all sensobs, behaviors. Invoke arbitrator.choose_action
        #Update motobs, wait, reset sensobs
        pass