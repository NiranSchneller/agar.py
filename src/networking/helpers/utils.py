import socket
import struct
from typing import Tuple, Union
import pygame
DELIMETER = "~"
SIZE_HEADER_FORMAT = "00000000~"  # n digits for data size + one delimiter
size_header_size = len(SIZE_HEADER_FORMAT)
TCP_DEBUG = False

POSSIBLE_FONT_SIZES = range(10, 40)


def get_max_font_size(text, width):
    for size in reversed(POSSIBLE_FONT_SIZES):
        font = pygame.font.SysFont(None, size)  # type: ignore
        if font.size(text)[0] <= width:
            return size
    return POSSIBLE_FONT_SIZES[0]


def recv_by_size(sock, return_type="string") -> str:
    """
    Receives data from a socket by first reading the size of the data and then receiving the data itself.

    This function is designed to receive data from a socket, where the size of the data is sent first
    as a header before the actual data. It reads the size header, then receives the data based on the
    size specified in the header.

    Parameters:
    - sock (socket.socket): The socket object used for communication.
    - return_type (str): The type of data to return. Default is "string".

    Returns:
    str or bytes: The received data, either as a string or bytes object, depending on the return_type.
    """
    str_size = b""
    data_len = 0
    while len(str_size) < size_header_size:
        _d = sock.recv(size_header_size - len(str_size))
        if len(_d) == 0:
            str_size = b""
            break
        str_size += _d
    data = b""
    str_size = str_size.decode()
    if str_size != "":
        data_len = int(str_size[:size_header_size - 1])
        while len(data) < data_len:
            _d = sock.recv(data_len - len(data))
            if len(_d) == 0:
                data = b""
                break
            data += _d

    if TCP_DEBUG and len(str_size) > 0:
        data_to_print = data[:100]
        if type(data_to_print) == bytes:
            try:
                data_to_print = data_to_print.decode()
            except (UnicodeDecodeError, AttributeError):
                pass
        print(f"\nReceive({str_size})>>>{data_to_print}")

    if data_len != len(data):
        data = b""  # Partial data is like no data !
    if return_type == "string":
        return data.decode()
    return data  # type: ignore


def send_with_size(sock, data):
    """
    Sends data over a socket after prepending it with the size of the data.

    This function sends data over a socket after adding a header that specifies the size of the data.
    The data is then sent over the socket.

    Parameters:
    - sock (socket.socket): The socket object used for communication.
    - data (str or bytes): The data to be sent.

    Returns:
    None

    """
    len_data = len(data)
    len_data = str(len(data)).zfill(size_header_size - 1) + "~"
    len_data = len_data.encode()
    if type(data) != bytes:
        data = data.encode()
    data = len_data + data
    sock.send(data)

    if TCP_DEBUG and len(len_data) > 0:
        data = data[:100]
        if type(data) == bytes:
            try:
                data = data.decode()
            except (UnicodeDecodeError, AttributeError):
                pass
        print(f"\nSent({len_data})>>>{data}")
