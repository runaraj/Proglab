

import random

class Arbitrator:


    def __init__(self, bbcon, motob):
        self.bbcon = bbcon
        self.motob = motob
        self.active_list = []
        self.weight_list = []


    #Runar at twork here
    def choose_action(self): #returns the MR from the behavior whose recommendation will be chosen
        self.update_active_list()
        self.update_weight_list()
        weight_sum = sum(self.weight_list) #make float manual?
        choice = random.uniform(0.0, weight_sum)
        for weight in range(len(self.weight_list)):
            if choice <= self.weight_list[weight]:
                 self.active_list[weight].motor_recommendations




    def update_active_list(self):
        self.active_list.clear()
        for behavior in self.bbcon.active_behaviors:
            if behavior.active_flag:
                self.active_list.append(behavior)

    def update_weight_list(self): #put this in same func as update active lists?
        self.weight_list.clear()
        #self.weight_list.append(0)
        for behavior in self.active_list:
            self.weight_list.append(behavior.weight)
        for i in range(1,len(self.weight_list)):
            self.weight_list[i] = self.weight_list[i-1]+self.weight_list[i]

