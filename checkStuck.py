

class CheckStuck():

    def __init__(self):
        self.prev_mrs = []
        self.stuck = False



    def check_prev(self):
        for mr in self.prev_mrs:
            if mr[0] == "F" or mr[0] == "B":
                return False
        return True

    def check_stuck(self, mr):
        self.prev_mrs.append(mr)
        if len(self.prev_mrs) == 5:
            self.stuck = self.check_prev()
        self.prev_mrs.clear()
        return self.stuck

