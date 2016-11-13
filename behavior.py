import sensob
import finnFarge

class Behavior:
    #HUSK BEHAVIORS SKAL IKKE OPPDATERE SENSOB/SENSORER BARE HENTE VERDIENE
    #BBCON OPPDATERER SENSORENE I STARTEN AV HVERT TIMESTEP

    def __init__(self, priority, sensobs):
        self.bbcon = None
        self.bbcon_index = None
        self.sensobs = []
        self.motor_recommendations = []
        self.active_flag = False
        self.halt_request = None
        self.priority = priority #brukes til å beregne weight [er statisk]
        self.match_degree = 0 #tall mellom [0,1], brukes til å beregne weight, sier noe om hvor viktig MRen er
        self.weight = 0 #brukes av arbitrator til aa velge handling
        self.add_sensobs(sensobs)

    def set_bbcon(self, bbcon):
        self.bbcon = bbcon #setter peker til bbcon
        self.bbcon_index = bbcon.behaviors.index(self) #brukes til aktivering/deaktivering

    # OBS! SENSOBS MÅ ADDES/REMOVES SOM LISTE
    def add_sensobs(self, sensobs):
        for sensob in sensobs:
            self.sensobs.append(sensob)

    def remove_sensobs(self, sensobs):
        for sensob in sensobs:
            self.sensobs.remove(sensob)

    def activate(self):
        self.active_flag = True
        print(self, "activated")
        self.bbcon.activate_behavior(self.bbcon_index)

    def deactivate(self):
        self.active_flag = False
        print(self, "deactivated")
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
            self.sense_and_act()
            self.calculate_weight()


    def get_sensob_data(self):
        sensobData = []
        for sensob in self.sensobs:
            sensobData.append(sensob.get_values())
        return sensobData

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
        #self.check_bbcon_data()
        self.give_recommendation()
        self.send_halt_request()
        self.determine_match_degree()

    def calculate_weight(self):
        self.weight = self.priority*self.match_degree
        return self.weight


class CollisionAvoidance(Behavior):  # do I need memory?
    # I have 1 sensob that has sensors = [ultrasonic, IRProximity]
    # dersom sidesensorer oppdager noe, sett flagg for at andre behaviors ikke kan svinge den veien?

    def __init__(self, priority, sensobs):
        super(CollisionAvoidance, self).__init__(priority=priority, sensobs=sensobs)
        self.frontDistance = 0
        self.right = False
        self.left = False
        self.direction = True

        self.count_time = 0

    def set_bbcon_sideflags(self):
        self.bbcon.left = self.left
        self.bbcon.right = self.right

    def get_sensob_data(self):
        values = self.sensobs[0].get_values()
        print(values)
        self.frontDistance = values[0]
        self.right = values[1][1]
        self.left = values[1][0]
        self.set_bbcon_sideflags()

    def frontCollisionImminent(self): #checks for frontalContact !!HVOR STOR TRENGER DENNE VERDIEN VAERE?!!
        if self.frontDistance < 6:
            return True
        return False

    def give_recommendation(self):  # RIGHT ELLER LEFT SETTE FLAGG SLIK AT ANDRE BEHAVIORS IKKE KAN SVINGE DEN VEIEN
        # no crashes in sight => low match degree
        # side crashes in sight mid-tier degree
        # front crash in sight => high-tier degree
        motoRec = ('F', 0)
        self.motor_recommendations.clear()
        direction = self.direction # dersom fare for frontkollisjon men ingen sidesensor fare=>True=prover aa unngaa til venstre, False=>hoyre
        if self.frontCollisionImminent():
            if self.frontDistance < 4.5:
                if self.left and self.right:
                    self.motor_recommendations.append(("B", 1.5))
                    if direction:
                        self.motor_recommendations.append(("R", 90))
                    else:
                        self.motor_recommendations.append(("L", 90))
                elif self.right:
                    motoRec = ("L", 90)
                elif self.left or direction:
                    motoRec = ('R', 90)
                else:
                    motoRec = ("L", 90)
            elif self.right:
                motoRec = ("L", 90)
            elif self.left or direction:
                motoRec = ("R", 90)
            else:
                motoRec = ("L", 90)

        self.direction = (not direction)

        self.motor_recommendations.append(motoRec)

    def determine_match_degree(self):
        if self.frontCollisionImminent():
            self.match_degree = 0.9
        else:
            self.match_degree = 0.25

    def consider_deactivation(self):
        if self.frontDistance > 40 and not self.left and not self.right:
            self.count_time += 1
        else:
            self.count_time = 0
        if self.count_time == 10:
            self.count_time = 0
            self.deactivate()

    def consider_activation(self):
        self.count_time += 1
        if self.count_time == 3:
            self.get_sensob_data()
            if self.frontDistance<30 or self.right or self.left:
                self.activate()
            self.count_time = 0


class FollowLine(Behavior):

    def __init__(self,priority, sensob):
        super(FollowLine, self).__init__(priority=priority, sensobs=sensob)
        self.left = False
        self.right = False
        self.count = 0
        self.time = 0 #teller timesteps for aktivering/deaktivering

    def give_recommendation(self):
        sensorArray = self.get_sensob_data()[0]

        ## TESTING ##
        print("sensor Array:", sensorArray)

        # nå brukes ikke de to midterse sensorene
        lineLeft = (sensorArray[0] + sensorArray[1])/2
        line_center = (sensorArray[2] + sensorArray[3])/2
        lineRight = (sensorArray[4] + sensorArray[5])/2
        lineDiff = abs(lineLeft-lineRight)

        # print("Left:", lineLeft, "LineDiff:", lineDiff, "Right:", lineRight)
        motoRec = ("F", 0.001)
        if self.count == 4:
            print("LineFollower sent request")
            self.bbcon.get_halt_request()
        elif line_center < lineLeft and line_center < lineRight:
            motoRec = ("F", 0)
            self.count = 0
        elif lineLeft < line_center and lineLeft < lineRight:
            motoRec = ("L", 30)
            self.count += 1
        else:
            motoRec = ("R", 30)
            self.count += 1
        self.motor_recommendations.clear()
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


class TrackObject(Behavior):
    #1 sensob = [ultrasonic, camera]
    #dersom ikke aktiv: Camera skal ikke ta bilder
    #bruker ultrasonic i consider activation => dersom et objekt er foran => aktiver og sjekk Camera
    #I consider_deavtivation: dersom Camera ikke ser noe av interesse=> deaktiver

    def __init__(self, priority, sensobs):
        super(TrackObject, self).__init__(priority=priority, sensobs=sensobs)
        self.frontDistance = 0
        self.halt_request = False
        self.image = None
        self.left = False
        self.right = False
        self.leftColor = 0
        self.rightColor = 0
        self.count = 0
        self.time = 0

        self.objectInSight = False


    def consider_activation(self):
        self.time += 1
        if self.time == 2:
            self.checkFront()
            if self.frontDistance < 15:
                self.get_sensob_data()
                self.leftColor, self.rightColor = self.get_colors()
                if self.leftColor+self.rightColor > 3000:
                    self.activate()
            self.time = 0

    def consider_deactivation(self):
        #self.checkFront() TRENGS DENNE?
        pixelcount = 64 * 96
        totalpixels = pixelcount * 2
        greenCount = self.leftColor+self.rightColor
        if self.frontDistance > 20 and (totalpixels-greenCount>pixelcount*1.5):
            self.deactivate()

    def activate(self):
        super(TrackObject, self).activate()
        self.bbcon.activate_camera()
    def deactivate(self):
        super(TrackObject, self).deactivate()
        self.bbcon.deactivate_camera()
        self.objectInSight = False

    def check_bbcon_data(self):
        self.left = self.bbcon.left
        self.right = self.bbcon.right

    def checkFront(self):
        value = self.sensobs[0].get_values()[0]
        self.frontDistance = value


    def get_sensob_data(self):
        self.image = self.sensobs[0].get_values()[1]
        self.image.save("cam.JPEG", format="JPEG")

    def give_recommendation(self):
        self.checkFront()
        self.leftColor, self.rightColor = self.get_colors() #antall grønne piksler i l/r bilde
        diff = abs(self.leftColor-self.rightColor)
        mr = ("F", 0)

        self.motor_recommendations.clear()
        print("FrontDist: ", self.frontDistance)
        print("LC: ", self.leftColor)
        print("RC: ", self.rightColor)
        if self.frontDistance<5 and ((self.leftColor+self.rightColor > 6000) or self.objectInSight):
            self.halt_request = True
        elif diff < 750 or self.count == 3:
            self.count = 0
        elif self.frontDistance>15: #KANSKJE?
            self.count += 1
            if self.count == 2:
                mr = ("F", 0)
            self.count = 0
        else:
            if self.leftColor > self.rightColor:
                if not self.left:
                    self.motor_recommendations.append(("L",15))
            else:
                if not self.right:
                    self.motor_recommendations.append(("R",15))
            mr = ("F", 0.25)
            #self.count += 1
        if diff < 750:
            self.objectInSight = True

        if self.halt_request:
            print("Sending req")
            self.bbcon.get_halt_request()
        else:
            self.motor_recommendations.append(mr)


    def determine_match_degree(self):
        self.match_degree = 1

    def get_colors(self):
        left = finnFarge.left("cam.JPEG")
        right = finnFarge.right("cam.JPEG")
        left = left.resize(64,96)
        right = right.resize(64,96)

        #ENDRE WTA TIL KUN Å TELLE TRENGER IKKE BILDE => DONE
        l = left.map_color_wta22(thresh=0.45)
        r = right.map_color_wta22(thresh=0.45)
        return l, r
