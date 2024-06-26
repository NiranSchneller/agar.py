import math


class PlayersEatenInformation:

    def __init__(self):
        self.is_eaten: bool = False
        self.ate_radius: float = 0

    """
        Set radius increase to the radius the player should be after he ate another player.
        
        s_a(r1,r2) = r1**2*pi + r2**2*pi
        A = s_a(r1,r2)
        new_r = sqrt(A/pi)
    """

    def ate_player(self, player_radius: float):
        sum_area = (player_radius ** 2 * math.pi) + \
            (self.ate_radius ** 2 * math.pi)
        self.ate_radius = (sum_area / math.pi) ** 0.5

    """
        Resets
    """

    def get_ate_radius(self) -> float:
        rad = self.ate_radius
        self.ate_radius = 0
        return rad

    def killed(self) -> None:
        self.is_eaten = True

    def get_killed(self) -> bool:
        return self.is_eaten
