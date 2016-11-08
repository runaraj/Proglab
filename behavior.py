import sensob


class Behavior:
    #HUSK BEHAVIORS SKAL IKKE OPPDATERE SENSOB/SENSORER BARE HENTE VERDIENE
    #BBCON OPPDATERER SENSORENE I STARTEN AV HVERT TIMESTEP

    def __init__(self, priority, sensobs):
        self.bbcon = None
        self.bbcon_index = None
        self.sensobs = []
        self.motor_recommendations = []
        self.active_flag = True
        self.halt_request = None
        self.priority = priority #brukes til å beregne weight [er statisk]
        self.match_degree = 0 #tall mellom [0,1], brukes til å beregne weight, sier noe om hvor viktig MRen er
        self.weight = 0 #brukes av arbitrator til aa velge handling
        #self.value = 0 ???
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
        self.check_bbcon_data()
        self.give_recommendation()
        self.send_halt_request()
        self.determine_match_degree()

    def calculate_weight(self):
        self.weight = self.priority*self.match_degree
        return self.weight



class CollisionAvoidance(Behavior): #do I need memory?
    #I have 1 sensob that has sensors=[ultrasonic, IRProximity]
    #dersom sidesensorer oppdager noe, sett flagg for at andre behaviors ikke kan svinge den veien?

    def __init__(self, priority, sensobs):
        super(CollisionAvoidance, self).__init__(priority=priority, sensobs=sensobs)
        self.frontDistance = 0
        self.right = False
        self.left = False
        self.direction = True

        self.count_time = 0


    def __str__(self):
        front = "FrontDistance: ", self.frontDistance
        right = "Right: ", self.right
        left = "Left: ", self.left
        return front + "\n" + right + "\n" + left

    def get_sensob_data(self):

        values = self.sensobs[0].get_values()
        print(values)
        self.frontDistance = values[0]
        self.right = values[1][0]
        self.left = values[1][1]


    def frontCollisionImminent(self): #checks for frontalContact !!HVOR STOR TRENGER DENNE VERDIEN VAERE?!!
        if self.frontDistance < 5:
            return True
        return False

    def give_recommendation(self): #RIGHT ELLER LEFT SETTE FLAGG SLIK AT ANDRE BEHAVIORS IKKE KAN SVINGE DEN VEIEN
        #no crashes in sight => low match degree
        #side crashes in sight mid-tier degree
        #front crash in sight => high-tier degree
        direction = self.direction #dersom fare for frontkollisjon men ingen sidesensor fare=>True=prover aa unngaa til venstre, False=>hoyre
        if self.frontCollisionImminent():
            if self.left or direction:
                recomm = ("R", 30)
            elif self.right or not direction:
                recomm = ("L", 30)
            else:
                pass #kan bruke direction her istedenfor
        else:
            if self.left:
                recomm = ("F", 0)
            elif self.right:
                recomm = ("F", 0)
            else:
                recomm = ("F", 0) #dersom det ikke er fare for kollisjon
        self.direction = (not direction)
        self.motor_recommendations.clear()
        self.motor_recommendations.append(recomm)



    def determine_match_degree(self):
        if self.frontCollisionImminent():
            self.match_degree = 0.9

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

    def give_recommendation(self):
        sensorArray = self.get_sensob_data()[0][0]
        print("sensor Array:", sensorArray)


        #nå brukes ikke de to midterse sensorene
        lineLeft = (sensorArray[0] + sensorArray[1])/2
        lineRight = (sensorArray[4] + sensorArray[5])/2
        lineDiff = abs(lineLeft-lineRight)

        print("Left:", lineLeft, "LineDiff:", lineDiff, "Right:", lineRight)


        #grensene her kan endres
        if 0.03 < lineDiff and lineLeft < lineRight:
            motoRec = ("L", 15)
        elif 0.03 < lineDiff and lineRight < lineLeft:
            motoRec = ("R", 15)
        else:
            motoRec = ("F", 0)
        self.motor_recommendations.clear()
        self.motor_recommendations.append(motoRec)
        print(self.motor_recommendations)

    def determine_match_degree(self):
        if self.motor_recommendations[0][0] == "R" or self.motor_recommendations[0][0] == "L":
            self.match_degree = 0.9
        else:
            self.match_degree = 0.4



class TrackObject(Behavior):
    #1 sensob = [ultrasonic, camera]
    #dersom ikke aktiv: Camera skal ikke ta bilder
    #bruker ultrasonic i consider activation => dersom et objekt er foran => aktiver og sjekk Camera
    #I consider_deavtivation: dersom Camera ikke ser noe av interesse=> deaktiver

    def __init__(self, priority, sensobs):
        super(TrackObject, self).__init__(priority=priority, sensobs=sensobs)
        self.frontDistance = 0
        self.image = None


    def consider_activation(self):
        pass


    def checkFront(self):
        pass

