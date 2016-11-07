from motors import Motors


class Motob:

    def __init__(self, motor):
        self.motor = motor    # The motor object we control. The motor object controls both wheels
        self.value = None   # a holder of the most recent MR sent to the Motob
        # value = (direction, degree) e.g (L, 30)=> turn 30 degrees to the left

    def update(self, mr):  # Receive a new MR, load it into value slot, and operate
        self.value = mr
        self.operationalize()

    def operationalize(self):  # convert a MR into 1 or more motor settings, and send them to corresponding motor
        if self.value[0] == 'L':
            self.motor.set_left_dir(self.value[1])
            #-- TEST --#
            if self.value[1] == 10:
                self.motor.set_value((0.1, 0.2), 10)
            if self.value[1] == 15:
                self.motor.set_value((0.2, 0.2), 10)
            if self.value[1] == 30:
                self.motor.set_value((0.1, 0.2), 10)
            if self.value[1] == 90:
                self.motor.set_value((0.2, 0.2), 10)
            #----------#
        if self.value[0] == 'R':
            #-- TEST --#
            self.motor.set_right_dir(self.value[1])
            if self.value[1] == 10:
                self.motor.set_value((0.2, 0.1), 10)
            if self.value[1] == 15:
                self.motor.set_value((0.2, 0.2), 10)
            if self.value[1] == 30:
                self.motor.set_value((0.2, 0.1), 10)
            if self.value[1] == 90:
                self.motor.set_value((0.2, 0.2), 10)
            # ----------#

        # TODO Set appropriate speeds for various angles
        # Set left/right speed (dc)
        # Set right/left dir (is_forward) # Either the actual value or forward/backward
