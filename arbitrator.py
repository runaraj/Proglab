

import random

class Arbitrator:


    def __init__(self, bbcon):
        self.bbcon = bbcon
        self.active_list = []
        self.weight_list = []


    def choose_action(self):
        self.update_active_list()
        self.update_weight_list()


    def update_active_list(self):
        self.active_list.clear()
        for behavior in self.bbcon.active_behaviors:
            if behavior.active_flag:
                self.active_list.append(behavior)

    def update_weight_list(self):
        self.weight_list.clear()
        #self.weight_list.append(0)
        for behavior in self.active_list:
            
