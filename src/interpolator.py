
"""
    Represents an interpolator, used for smooth scaling

    takes in x, y as starting points, and has dynamic target points.

"""
class Interpolator:

    def __init__(self, increaser, x, y):
        self.increaser = increaser
        self.current_increaser = increaser
        self.x = x
        self.y = y

        self.is_lerping = False

        self.target_x = x
        self.target_y = y

    def init_lerp(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.is_lerping = True
        self.current_increaser = self.increaser


    def lerp(self):
        if self.is_lerping:
            res_x = self.x + (self.target_x - self.x) * self.current_increaser
            res_y = self.y + (self.target_y - self.y) * self.current_increaser
            self.current_increaser = min(self.increaser + self.current_increaser, 1)
            if self.current_increaser == 1:
                self.is_lerping = False
            return res_x, res_y
        else:
            return self.target_x, self.target_y



