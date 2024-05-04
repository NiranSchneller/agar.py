from typing import List, Tuple, Union
from src.edible import Edible
from ast import literal_eval as make_tuple
from src.networking.information.player_information import PlayerInformation
LOG_PROTOCOL = False
EATEN = "EATEN"


class Protocol:

    @staticmethod
    def server_initiate_world(level_size: Tuple[int, int], edibles: List[Edible]) -> str:
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
        message = ''
        message += f'~{level_size[0]},{level_size[1]}~'
        for edible in edibles:
            tup = str(edible.color).replace(',', ':')
            message += f'{edible.platform_x},{edible.platform_y},{tup},{edible.radius}~'
        return message

    """
        Parses the message: server_initiate_world
    """

    @staticmethod
    def parse_server_initiate_world(message: str) -> Tuple[Tuple[str, str], List[Edible]]:
        message_list = message.split('~')
        # message[1] = width,height
        world_size = (message_list[1].split(',')[0],
                      message_list[1].split(',')[1])

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
    def generate_client_status_update(player_x: int, player_y: int, player_radius: float, name: str, id: str,
                                      edibles: Union[List[Edible], None] = None) -> str:
        message: str = '~'
        message += f'{id},{name},{player_x},{player_y},{player_radius}~'

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
    def parse_client_status_update(message: str) -> Tuple[PlayerInformation, List[Edible]]:
        if LOG_PROTOCOL:
            print(f"Client sent message: {message}")
        message_list = message.split('~')

        # location of player in world coordinates
        player_information = message_list[1].split(',')
        player_uuid = player_information[0]
        player_name = player_information[1]
        player_location = float(player_information[2]), float(
            player_information[3])
        player_radius = float(player_information[4])

        eaten_edibles = []
        # update the server if any edibles were eaten
        if message_list[2] != '':
            # + 1 because we need to account for starting delimeter
            edibles_list_unparsed = message[message[1::].find(
                '~') + 1 + 1:].split('~')
            for edible in edibles_list_unparsed:
                if edible != '':
                    params = edible.split(',')
                    edible_x = int(params[0])
                    edible_y = int(params[1])
                    color = make_tuple(params[2].replace(':', ','))
                    radius = int(params[3])
                    eaten_edibles.append(
                        Edible(edible_x, edible_y, color, radius))
        return PlayerInformation(player_location[0], player_location[1], player_radius, player_name, player_uuid), eaten_edibles

    """
        Message sent to client to update him of everything he needs to know (changes in world, player positions)
        
        special seperator for this type of message - ~!"# -> signifies transition between data 
        message -> [size]~5,5,(2,2,2),6~...~!"#6,5,4...~23,45,(..),5~!"....~
    """
    @staticmethod
    def generate_server_status_update(edibles_created: List[Edible],
                                      other_player_information: List[PlayerInformation],
                                      edibles_removed: List[Edible],
                                      eaten_rad_increase: float, is_eaten: bool) -> str:
        if is_eaten:
            return EATEN

        message = f'~'

        for edible in edibles_created:
            tup = str(edible.color).replace(',', ':')
            message += f'{edible.platform_x},{edible.platform_y},{tup},{edible.radius}~'
        # added edibles created
        message += '!"#'
        for player_information in other_player_information:
            message += f'{player_information.name},{player_information.x},{player_information.y},{player_information.radius}~'
        message += '!"#'

        for edible_removed in edibles_removed:
            tup = str(edible_removed.color).replace(',', ':')
            message += f'{edible_removed.platform_x},{edible_removed.platform_y},{tup},{edible_removed.radius}~'

        return message + '!"#' + str(eaten_rad_increase)

    @staticmethod
    def parse_server_status_update(message: str) -> Union[str, Tuple[List[Edible], List[PlayerInformation],
                                                                     List[Edible], float]]:
        if message.strip() == "EATEN":
            return "EATEN"

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
                edibles_created.append(
                    Edible(edible_x, edible_y, color, radius))

        player_information_unparsed = message.split('!"#')[1]
        player_information_list = player_information_unparsed.split('~')
        player_information_parsed: List[PlayerInformation] = []

        for information in player_information_list:
            if information != '':
                information_params = information.split(',')
                player_name = information_params[0]
                player_x, player_y = int(float(information_params[1])), int(
                    float(information_params[2]))
                player_radius = int(float(information_params[3]))
                player_information_parsed.append(PlayerInformation(
                    player_x, player_y, player_radius, player_name))

        edibles_removed_list = message.split('!"#')[2].split('~')
        edibles_removed: List[Edible] = []

        for edible_removed in edibles_removed_list:
            if edible_removed != '':
                params = edible_removed.split(',')
                edible_x = int(params[0])
                edible_y = int(params[1])
                color = make_tuple(params[2].replace(':', ','))
                radius = int(params[3])
                edibles_removed.append(
                    Edible(edible_x, edible_y, color, radius))

        radius_inc = (message.split('!"#')[3])
        radius_inc = float(radius_inc)
        return edibles_created, player_information_parsed, edibles_removed, radius_inc
