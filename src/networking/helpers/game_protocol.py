from src.edible import Edible
from ast import literal_eval as make_tuple


class Protocol:
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
            tup = str(edible.color).replace(',', ':')
            message += f'{edible.platform_x},{edible.platform_y},{tup},{edible.radius}~'
        return message

    """
        Parses the message: server_initiate_world
        
        :returns -> tuple (x,y), tuple (edibles)
    """

    @staticmethod
    def parse_server_initiate_world(message: str):
        message_list = message.split('~')
        # message[1] = width,height
        world_size = (message_list[1].split(',')[0], message_list[1].split(',')[1])

        edible_message_unparsed = message[message[1::].find('~') + 1:]
        # now we have the edibles, parsing...
        edible_list_unparsed = edible_message_unparsed.split('~')
        print(edible_list_unparsed)
        edibles = []  # return list of edibles
        for edible in edible_list_unparsed:
            if edible != '':
                params = edible.split(',')
                edible_x = int(params[0])
                edible_y = int(params[1])
                color = make_tuple(params[2].replace(':',','))
                radius = int(params[3])
                edibles.append(Edible(edible_x, edible_y, color, radius))

        return world_size, edibles
