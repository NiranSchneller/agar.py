
"""
    Represents an interpolator, used for smooth scaling

    takes in x, y as starting points, and has dynamic target points.

"""
class Interpolator:

    def __init__(self, increaser, x):
        self.increaser = increaser
        self.current_increaser = increaser
        self.x = x

        self.is_lerping = False

        self.target_x = x

    def init_lerp(self, x, target_x):
        self.x = x
        self.target_x = target_x
        self.is_lerping = True
        self.current_increaser = self.increaser


    def lerp(self):
        if self.is_lerping:
            res_x = self.x + (self.target_x - self.x) * self.current_increaser
            self.current_increaser = min(self.increaser + self.current_increaser, 1)
            if self.current_increaser == 1:
                self.is_lerping = False
            return res_x
        else:
            return self.target_x

