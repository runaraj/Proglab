


class Behavior:


    def __init__(self, bbcon):
        self.bbcon = bbcon
        self.sensobs = []
        self.motor_recommendations = []
        self.active_flag = False
        self.halt_request = None
        self.priority = 0
        self.match_degree = 0
        self.weight = 0

    def set_priority(self, value):
        self.priority = value

    def consider_deactivation(self):
        pass

    def consider_activation(self):
        pass

    def update(self):
        if active_flag:
            self.consider_deactivation()
        else:
            self.consider_activation()
        if active_flag:
            self.sense_and_act()


    def sense_and_act(self):
        pass

    def calculate_weight(self):
        self.weight = self.priority*self.match_degree
        return self.weight



class CollisionAvoidanceBehavior(Behavior):

    
