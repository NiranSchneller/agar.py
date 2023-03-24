import pygame

class PlayerConstants:
    PLAYER_VELOCITY = 7.5  # pixels per 1/ FPS seconds
    PLAYER_COLOR = (0, 200, 200)
    PLAYER_STARTING_RADIUS = 100
    DISTANCE_THRESHOLD = PLAYER_VELOCITY


class PlayerCameraConstants:
    PLAYER_CAMERA_WIDTH = 1920
    PLAYER_CAMERA_HEIGHT = 1080
    GRID_LINE_COLOR = 180, 180, 180
    BACKGROUND_COLOR = 173, 216, 230
    WINDOW_GRID_SPACING = 50  # pixels

class PlatformConstants:
    PLATFORM_HEIGHT = 20000
    PLATFORM_WIDTH = 20000

class GameSettings:
    GAME_NAME = "Agar.py"
    FPS = 60
