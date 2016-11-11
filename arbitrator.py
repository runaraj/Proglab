from collections import defaultdict


class Arbitrator:

    def __init__(self, motob):
        self.bbcon = None
        self.motob = motob
        self.weighted_active = defaultdict(float)

    def set_bbcon(self, bbcon):
        self.bbcon = bbcon

    def choose_action(self):  # returns the MR from the behavior whose recommendation will be chosen
        self.update_active_list()
        max_pri = 0
        max_behavior = None
        for behaviour in self.weighted_active:
            if self.weighted_active[behaviour] > max_pri:
                max_pri = self.weighted_active
                max_behavior = behaviour
            return max_behavior.motor_reccomendations[0]

    def update_active_list(self):
        self.weighted_active.clear()
        for behavior in self.bbcon.active_behaviors:
            if behavior.active_flag:
                self.weighted_active[behavior] = behavior.weight
