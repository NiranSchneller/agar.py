from src.edible import Edible
from ast import literal_eval as make_tuple
from src.networking.information.player_information import PlayerInformation
LOG_PROTOCOL = True

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
        edibles = []  # return list of edibles
        for edible in edible_list_unparsed:
            if edible != '':
                params = edible.split(',')
                edible_x = int(params[0])
                edible_y = int(params[1])
                color = make_tuple(params[2].replace(':', ','))
                radius = int(params[3])
                edibles.append(Edible(edible_x, edible_y, color, radius))

        return world_size, edibles

    """
        Updates the server of any changes in the playing field, including edibles being eaten
        
        message -  ~name,x,y,radius~...~
        ... - Send edible information if it was eaten, so server can remove it from the playing field
    """

    @staticmethod
    def generate_client_status_update(player_x, player_y, player_radius, name, edibles: [Edible] = None):
        message = '~'
        message += f'{name},{player_x},{player_y},{player_radius}~'



        if edibles is not None:
            for edible in edibles:
                tup = str(edible.color).replace(',', ':')
                message += f'{edible.platform_x},{edible.platform_y},{tup},{edible.radius}~'

        return message

    """
        A message has been recieved from a client in the format of the message sent in - generate_client_status_update
        edible format (reminder) - x,y,color,radius
    """

    @staticmethod
    def parse_client_status_update(message: str):
        if LOG_PROTOCOL:
            print(f"Client sent message: {message}")
        message_list = message.split('~')

        # location of player in world coordinates
        player_information = message_list[1].split(',')
        player_name = player_information[0]
        player_location = player_information[1], player_information[2]
        player_radius  = player_information[3]


        eaten_edibles = []
        # update the server if any edibles were eaten
        if message_list[2] != '':
            # + 1 because we need to account for starting delimeter
            edibles_list_unparsed = message[message[1::].find('~') + 1 + 1:].split('~')
            for edible in edibles_list_unparsed:
                if edible != '':
                    params = edible.split(',')
                    edible_x = int(params[0])
                    edible_y = int(params[1])
                    color = make_tuple(params[2].replace(':', ','))
                    radius = int(params[3])
                    eaten_edibles.append(Edible(edible_x, edible_y, color, radius))

        return PlayerInformation(player_name, player_location[0], player_location[1], player_radius), eaten_edibles



    """
        Message sent to client to update him of everything he needs to know (changes in world, player positions)
        
        special seperator for this type of message - ~!"# -> signifies transition between data 
        message -> [size]~5,5,(2,2,2),6~...~!"#6,5,4...~23,45,(..),5~!"....~
    """
    @staticmethod
    def generate_server_status_update(edibles_created: [Edible], player_locations, edibles_removed: [Edible]):

        message = f'~'

        for edible in edibles_created:
            tup = str(edible.color).replace(',', ':')
            message += f'{edible.platform_x},{edible.platform_y},{tup},{edible.radius}~'

        # TODO: player_locations and edibles_removed
        return message + '!"#' # TEMPORARY


    @staticmethod
    def parse_server_status_update(message: str):
        # TODO: transition between data
        edibles_created_unparsed = message.split('!"#')[0]
        # now we have: ~5,5,(2,2,2),6~...~
        edibles_created_list = edibles_created_unparsed.split('~')

        edibles_created = []
        for edible_created in edibles_created_list:
            if edible_created != '':
                params = edible_created.split(',')
                edible_x = int(params[0])
                edible_y = int(params[1])
                color = make_tuple(params[2].replace(':', ','))
                radius = int(params[3])
                edibles_created.append(Edible(edible_x, edible_y, color, radius))
        return edibles_created










