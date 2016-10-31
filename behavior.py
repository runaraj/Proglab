


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

    def consider_deavtivation(self):
        pass

    def consider_activation(self):
        pass

    def update(self):
        pass

    def sense_and_act(self):
        pass
