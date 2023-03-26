import pygame


class PlayerCameraConstants:
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    GRID_LINE_COLOR = 180, 180, 180
    BACKGROUND_COLOR = 173, 216, 230
    WINDOW_GRID_SPACING = 50  # pixels


class PlayerConstants:
    PLAYER_VELOCITY = 7.5  # pixels per 1/ FPS seconds
    PLAYER_COLOR = (0, 200, 200)
    PLAYER_OUTLINE_COLOR = 115, 147, 179
    PLAYER_STARTING_OUTLINE_THICKNESS = 1
    PLAYER_LOCATION_CAMERA = (PlayerCameraConstants.SCREEN_WIDTH / 2, PlayerCameraConstants.SCREEN_HEIGHT / 2)
    PLAYER_STARTING_RADIUS = 100
    DISTANCE_THRESHOLD = PLAYER_VELOCITY

class EdibleConstants:
    EDIBLE_RADIUS = 20
    EDIBLE_COLOR = (0,0,0)
    AMOUNT_OF_EDIBLES = 4000


class PlatformConstants:
    PLATFORM_HEIGHT = 20000
    PLATFORM_WIDTH = 20000

class GameSettings:
    GAME_NAME = "Agar.py"
    FPS = 60
