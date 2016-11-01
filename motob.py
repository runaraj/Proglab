from motors import Motors


class Motob:

    def __init__(self):
        self.motors = []    # list of motors whose settings will be determined
        self.value = None   # a holder of the most recent MR sent to the motob
        # value = (direction, degree) e.g (L, 30)=> turn 30 degrees to the left

    def add_motor(self, motor):
        self.motors.append(motor)

    def update(self, mr): # recv. a new MR, load it into value slot, and operate
        self.value = mr
        self.operationalize()

    def operationalize(self): # convert a MR into 1 or more motor settings, and send them to corresponding motor
        if self.value[0] == 'L':
            for motor in self.motors:
                motor.set_left_dir(self.value[1])
        if self.value[1] == 'R':
            for motor in self.motors:
                motor.set_right_dir(self.value[1])

        # Set left/right speed (dc)
        # Set right/left dir (is_forward) # Either the actual value or forward/backward
