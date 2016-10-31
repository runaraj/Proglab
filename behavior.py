


class Behavior:


    def __init__(self, priority):
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

    def set_bbcon(self, bbcon):
        self.bbcon = bbcon
        self.bbcon_index = bbcon.behaviors.index(self)


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
        if self.active_flag:
            self.value = self.sense_and_act()
        return self.value

    def sense_and_act(self):
        pass

    def calculate_weight(self):
        self.weight = self.priority*self.match_degree
        return self.weight



class CollisionAvoidance(Behavior):

    def __init__(self, priority, sensobs):
        super(CollisionAvoidance, self).__init__(priority=priority)
        self.add_sensobs(sensobs)
        self.frontDistance = None

    def sense_and_act(self):
        self.frontDistance = self.sensobs[0].get_value()
        return self.frontDistance




    
class FollowLine(Behavior):

class TracObject(Behavior):

