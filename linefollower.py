from behavior import Behavior

class FollowLine(Behavior):

    def __init__(self,priority, sensob):
        super(FollowLine, self).__init__(priority=priority, sensobs=sensob)
        self.left = False
        self.right = False
        self.count = 0
        self.time = 0 #teller timesteps for aktivering/deaktivering

    def give_recommendation(self):
        self.motor_recommendations.clear()
        sensorArray = self.get_sensob_data()[0]

        lineLeft = (sensorArray[0] + sensorArray[1])/2
        line_center = (sensorArray[2] + sensorArray[3])/2
        lineRight = (sensorArray[4] + sensorArray[5])/2

        motoRec = ("F", 0.001)
        if self.count == 4:
            print("LineFollower sent request")
            self.bbcon.get_halt_request()

        elif line_center < lineLeft and line_center < lineRight:
            motoRec = ("F", 0)
            self.count = 0
            diff = lineLeft-lineRight
            if diff>0.25:
                self.motor_recommendations.append(motoRec)
                self.motor_recommendations.append(("R", 90))
            elif diff<-0.25:
                self.motor_recommendations.append(motoRec)
                self.motor_recommendations.append(("L", 90))
        elif lineLeft < line_center and lineLeft < lineRight:
            motoRec = ("L", 30)
            self.count += 1
        else:
            motoRec = ("R", 30)
            self.count += 1
        self.motor_recommendations.append(motoRec)
        # print(self.motor_recommendations)

    def consider_activation(self):
        self.time += 1
        if self.time == 4:
            sensorArray = self.get_sensob_data()[0][0]
            minste = min(sensorArray)
            maxte = max(sensorArray)
            if maxte-minste >0.22:
                self.activate()
            self.time = 0

    def consider_deactivation(self):
        print(self.get_sensob_data()[0])
        sensorArray = self.get_sensob_data()[0][0]
        print(sensorArray)
        minste = min(sensorArray)
        maxte = max(sensorArray)
        if maxte-minste<0.07:
            self.deactivate()


    def determine_match_degree(self):
        self.match_degree = 0.3

    def check_bbcon_data(self):
        self.left = self.bbcon.left
        self.right = self.bbcon.right