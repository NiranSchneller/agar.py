
from src.edible import Edible

class Protocol:
    def __init__(self):
        pass


    """
        This method constructs a message that is to be sent to the client, requires information about the players
        and the edibles.
        
        world_size - tuple of two (x,y)
        edibles: list of edible object
        
        
        Generates a protocol message that looks like:
        ~world_size_x,world_size_y~edible_x,edible_y,edible_color,edible_radius~
        
        for example:
        ~20000,20000~200,300,(2,3,4),5~......~
        .... signifies - for each edible
    """
    @staticmethod
    def server_initiate_world(level_size, edibles: [Edible]):
        message = ''
        message += f'~{level_size[0]},{level_size[1]}~'
        for edible in edibles:
            message += f'{edible.platform_x},{edible.platform_y},{edible.color},{edible.radius}~'
        return message
