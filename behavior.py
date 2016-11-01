


class Behavior:


    def __init__(self, priority, sensobs):
        self.bbcon = None
        self.bbcon_index = None
        self.sensobs = []
        self.motor_recommendations = []
        self.active_flag = False
        self.halt_request = None
        self.priority = priority
        self.match_degree = 0
        self.weight = 0
        self.value = 0
        self.add_sensobs(sensobs)

    def set_bbcon(self, bbcon):
        self.bbcon = bbcon
        self.bbcon_index = bbcon.behaviors.index(self)

    # OBS! SENSOBS MÅ ADDES/REMOVES SOM LISTE
    def add_sensobs(self, sensobs):
        for sensob in sensobs:
            self.sensobs.append(sensob)

    def remove_sensobs(self, sensobs):
        for sensob in sensobs:
            self.sensobs.remove(sensob)

    def activate(self):
        self.active_flag = True
        self.bbcon.activate_behavior(self.bbcon_index)

    def deactivate(self):
        self.active_flag = False
        self.bbcon.deactivate_behavior(self)

    def consider_deactivation(self):
        pass

    def consider_activation(self):
        pass

    def update(self):
        if self.active_flag:
            self.consider_deactivation()
        else:
            self.consider_activation()
        if self.active_flag: #funke?
            self.sense_and_act()
            self.calculate_weight()


    def get_sensob_data(self):
        pass

    def check_bbcon_data(self):
        pass

    def give_recommendation(self):
        pass

    def send_halt_request(self):
        pass

    def determine_match_degree(self):
        pass


    def sense_and_act(self):
        self.get_sensob_data()
        self.check_bbcon_data()
        self.give_recommendation()
        self.send_halt_request()
        self.determine_match_degree()

    def calculate_weight(self):
        self.weight = self.priority*self.match_degree
        return self.weight



class CollisionAvoidance(Behavior): #do I need memory?
    #I have 1 sensob that has sensors=[ultrasonic, IRProximity]

    def __init__(self, priority, sensobs):
        super(CollisionAvoidance, self).__init__(priority=priority)
        self.frontDistance = None
        self.right = False
        self.left = False


    def get_sensob_data(self):
        self.sensobs[0].update()
        values = self.sensobs[0].get_values()
        self.frontDistance = values[0]
        self.right = values[1][0]
        self.left = values[1][1]


    def frontCollisionImminent(self): #checks for frontalContact
        if self.frontDistance < 2:
            return True
        return False

    def give_recommendation(self):
        #no crashes in sight => low match degree
        #side crashes in sight mid-tier degree
        #front crash in sight => high-tier degree




        return ("F", 0)



    def determine_match_degree(self):
        if self.frontCollisionImminent():
            self.match_degree = 0.9

class FollowLine(Behavior):
    pass
class TracObject(Behavior):
    pass
