from typing import Tuple


LOG_DH = False


class DHProtocol():
    @staticmethod
    def server_send_pg(p: int, g: int) -> str:
        return f"{p}~{g}"

    @staticmethod
    def client_recieve_pg(message: str) -> Tuple[int, int]:
        p, g = message.split("~")
        if LOG_DH:
            print(f"p:{p}, g:{g}")
        return int(p), int(g)

    @staticmethod
    def server_send_A(a: int) -> str:
        return f"{a}~"

    @staticmethod
    def client_recieve_A(message: str) -> int:
        a = message.split("~")[0]
        if LOG_DH:
            print(f"alice_a:{a}")
        return int(a)

    @staticmethod
    def client_send_B(b: int) -> str:
        return f"{b}~"

    @staticmethod
    def server_recieve_B(message: str) -> int:
        b = message.split("~")[0]
        if LOG_DH:
            print(f"bob_b:{b}")
        return int(b)
