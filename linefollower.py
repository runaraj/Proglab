from behavior import Behavior
import random

class LineFollow(Behavior):

    def __init__(self,priority, sensob):
        super(LineFollow, self).__init__(priority=priority, sensobs=sensob)
        self.left = False
        self.right = False
        self.count = 0
        self.time = 0 #teller timesteps for aktivering/deaktivering
        self.turn = False

    def give_recommendation(self):
        self.motor_recommendations.clear()
        print(self.get_sensob_data())
        sensorArray = self.get_sensob_data()[0][0]

        lineLeft = (sensorArray[0] + sensorArray[1])/2
        line_center = (sensorArray[2] + sensorArray[3])/2
        lineRight = (sensorArray[4] + sensorArray[5])/2
        diff = abs(lineLeft - lineRight)>0.25
        avg = sum(sensorArray)/6
        self.turn = True

        motoRec = ("F", 0.2)
        if self.count == 4:
            print("LineFollower sent request")
            self.bbcon.get_halt_request()

        elif diff:
            if lineLeft<lineRight:
                if lineRight-line_center>0.25:
                    self.motor_recommendations.append(motoRec)
                    self.motor_recommendations.append(("L", 90))
                elif sensorArray[1]-sensorArray[0]>0.25:
                    self.motor_recommendations.append(("L", 30))
                else:
                    self.motor_recommendations.append(("L", 15))
            if lineRight<lineLeft:
                if lineLeft-line_center>0.25:
                    self.motor_recommendations.append(motoRec)
                    self.motor_recommendations.append(("R", 90))
                elif sensorArray[4]-sensorArray[5]>0.25:
                    self.motor_recommendations.append(("R", 30))
                else:
                    self.motor_recommendations.append(("R", 15))
        elif avg<0.45:
            dir = random.randint(0,1)
            if dir:
                self.motor_recommendations.append(motoRec)
                self.motor_recommendations.append(("L", 90))
            else:
                self.motor_recommendations.append(motoRec)
                self.motor_recommendations.append(("R", 90))
        else:
            motoRec = ("F", 0.3)
            self.turn = False
        self.motor_recommendations.append(motoRec)
        # print(self.motor_recommendations)

    def consider_activation(self):
        self.time += 1
        if self.time == 3:
            sensorArray = self.get_sensob_data()[0][0]
            minste = min(sensorArray)
            maxte = max(sensorArray)
            avg = sum(sensorArray)/6
            if maxte-minste >0.22 or avg<0.4:
                self.activate()
            self.time = 0

    def consider_deactivation(self):
        #print(self.get_sensob_data()[0])
        sensorArray = self.get_sensob_data()[0][0]
        #print(sensorArray)
        #minste = min(sensorArray)
        #maxte = max(sensorArray)
        avg = sum(sensorArray)/6
        if avg>0.71:
            self.deactivate()


    def determine_match_degree(self):
        if self.turn:
            self.match_degree = 0.8
        else:
            self.match_degree = 0.3

    def check_bbcon_data(self):
        self.left = self.bbcon.left
        self.right = self.bbcon.right