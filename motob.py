from motors import Motors


class Motob:

    def __init__(self, motor, duration=1):
        self.motor = motor    # The motor object we control. The motor object controls both wheels
        self.value = None   # a holder of the most recent MR sent to the Motob
        # value = (direction, degree) e.g (L, 30)=> turn 30 degrees to the left
        self.duration = duration

    def update(self, mr):  # Receive a new MR, load it into value slot, and operate
        self.value = mr
        self.operationalize()

    def operationalize(self):  # convert a MR into 1 or more motor settings, and send them to corresponding motor
        if self.value[0] == 'L':
            #  self.motor.set_left_dir(self.value[1]) Don't think this is needed?
            if self.value[1] == 10:
                self.motor.set_value((0.3, 0.4), self.duration / 2)
            if self.value[1] == 15:
                self.motor.set_value((0.3, 0.4), self.duration)
            if self.value[1] == 30:
                self.motor.set_value((0.4, 0.9), self.duration / 2)
            if self.value[1] == 90:
                self.motor.set_value((0.4, 0.9), self.duration)
            self.motor.forward(dur=self.duration / 2)

        if self.value[0] == 'R':
            # self.motor.set_right_dir(self.value[1])
            if self.value[1] == 10:
                self.motor.set_value((0.2, 0.1), self.duration/2)
            if self.value[1] == 15:
                self.motor.set_value((0.2, 0.2), self.duration/2)
            if self.value[1] == 30:
                self.motor.set_value((0.2, 0.1), self.duration/2)
            if self.value[1] == 90:
                self.motor.set_value((0.2, 0.2), self.duration/2)
            self.motor.forward(dur=self.duration / 2)

        if self.value[0] == "F":
            self.motor.forward(dur=self.duration)

        if self.value[0] == "B":
            self.motor.backward(dur=self.duration)

