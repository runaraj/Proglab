from motors import Motors


class Motob:

    def __init__(self, motor, duration=0.5):
        self.motor = motor    # The motor object we control. The motor object controls both wheels
        self.value = None   # a holder of the most recent MR sent to the Motob
        # value = (direction, degree) e.g (L, 30)=> turn 30 degrees to the left
        self.duration = duration

    def update(self, mr):  # Receive a new MR, load it into value slot, and operate
        self.value = mr
        self.operationalize()

    def operationalize(self):  # Convert a MR into 1 or more motor settings, and send them to corresponding motor
        # 15, 30, 90 serves as indicators on how much the robot "turns"

        if self.value[0] == 'L':
            if self.value[1] == 15:
                self.motor.set_value((-0.3, 0.3), self.duration/2)
            if self.value[1] == 30:
                self.motor.set_value((-0.3, 0.3), self.duration)
            if self.value[1] == 90:
                self.motor.set_value((-0.4, 0.4), self.duration * 1.85)

        if self.value[0] == 'R':
            if self.value[1] == 15:
                self.motor.set_value((0.3, -0.3), self.duration/2)
            if self.value[1] == 30:
                self.motor.set_value((0.3, -0.3), self.duration)
            if self.value[1] == 90:
                self.motor.set_value((0.4, -0.4), self.duration * 1.85)

        if self.value[0] == "F":
            if self.value[1] != 0:
                self.motor.forward(dur=self.value[1])
            else:
                self.motor.forward(dur=self.duration)

        if self.value[0] == "B":
            if self.value[1] != 0:
                self.motor.backward(dur=self.value[1])
            else:
                self.motor.backward(dur=self.duration)

        if self.value[0] == "S":
            self.motor.stop()

