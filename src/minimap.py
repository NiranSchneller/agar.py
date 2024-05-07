
import pygame

from src.networking.helpers.utils import get_max_font_size
from src.constants import PlayerConstants, EdibleConstants
from src.networking.information.player_information import PlayerInformation
from src.player import Player
from typing import List

MINIMAP_SIZE = (200, 200)
MINIMAP_POSE = (0, 0)  # (X,Y)
MINIMAP_BORDER_SIZE = 5


class Minimap():

    @staticmethod
    def update_minimap(other_player_information: List[PlayerInformation],
                       world_information_dimensions, edibles, player: Player, window: pygame.Surface):

        other_player_information.append(PlayerInformation(
            player.x, player.y, player.radius, player.name, "MyPlayer"))

        for edible in edibles:
            edible_clone = PlayerInformation(
                edible.platform_x, edible.platform_y, edible.radius, "iAmEdible", "Edible")
            other_player_information.append(edible_clone)

        # Border rectangle
        pygame.draw.rect(window, (0, 0, 0), pygame.Rect(
            MINIMAP_POSE[0], MINIMAP_POSE[1], MINIMAP_SIZE[0] +
            MINIMAP_BORDER_SIZE,
            MINIMAP_SIZE[1] + MINIMAP_BORDER_SIZE))

        pygame.draw.rect(window, (173, 216, 190), pygame.Rect(
            MINIMAP_POSE[0], MINIMAP_POSE[1],
            MINIMAP_SIZE[0], MINIMAP_SIZE[1]))

        world_width = world_information_dimensions[0]
        world_height = world_information_dimensions[1]
        for player_information in other_player_information[::-1]:
            x_scale_ratio = MINIMAP_SIZE[0] / int(world_width)
            y_scale_ratio = MINIMAP_SIZE[1] / int(world_height)

            absolute_player_minimap_x = player_information.x * x_scale_ratio
            absolute_player_minimap_y = player_information.y * y_scale_ratio

            player_minimap_x = MINIMAP_POSE[0] + absolute_player_minimap_x
            player_minimap_y = MINIMAP_POSE[1] + absolute_player_minimap_y
            player_minimap_radius = player_information.radius * y_scale_ratio

            color = PlayerConstants.PLAYER_COLOR
            if player_information.name == "iAmEdible":
                color = EdibleConstants.EDIBLE_COLOR

            pygame.draw.circle(window, color,
                               (player_minimap_x, player_minimap_y), max(player_minimap_radius, MINIMAP_POSE[0]))
            # The appended player information has "" as its
            if player_information.id == "MyPlayer":
                font_size = get_max_font_size(
                    "You", player_minimap_radius)
                font = pygame.font.SysFont("Arial", font_size)
                name_surface = font.render("You", True, (255, 255, 255))
                name_rect = name_surface.get_rect()
                name_rect.center = (
                    player_minimap_x, player_minimap_y)  # type: ignore
                window.blit(name_surface, name_rect)
