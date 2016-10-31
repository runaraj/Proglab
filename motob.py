from motors import Motors


class Motob:

    def __init__(self):
        motors = [] #list of motors whose settings will be determined
        value = None #a holder of the most recent MR sent to the motob
        #value = (direction, degree) e.g (L, 30)=> turn 30 degrees to the left


    def update(mr): #recv. a new MR, load it into value slot, and operate
        self.value = mr
        self.operationalize()

    def operationalize(): #convert a MR into 1 or more motor settings, and send them to corresponding motor
        pass
