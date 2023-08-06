class NetworkError(Exception):
    def __init__(self, error: str):
        super().__init__(error)


class TCPServerOccupiedError(NetworkError):
    def __init__(self, server_name):
        super().__init__(
            f"{server_name} has been occupied Note:TCP Server Currently \
Only Support A Single Client")


class CommParserError(NetworkError):
    pass


class CommResourceError(NetworkError):
    pass


class CommNotConnectError(NetworkError):
    pass


class InvaildPlugin(CommResourceError):
    def __init__(self, module: str, plugin: str):
        super().__init__(f"Can not find plugin({module}.{plugin}).")


class InvaildModule(CommResourceError):
    def __init__(self, module: str):
        super().__init__(f"Can not find module({module}).")


class InvaildMethod(CommParserError):
    def __init__(self, method: str):
        super().__init__(f"Can not parser method({method}).")


class InvaildJsonMsg(CommParserError):
    def __init__(self, e: Exception):
        super().__init__(f"Message can not convert to json object: {e}.")


class RpcIdInvaild(CommParserError):
    def __init__(self):
        super().__init__("rpc id is not int type.")


class RpcVersionInvaild(CommParserError):
    def __init__(self):
        super().__init__("rpc version is not 2.0.")


class RpcMethodMiss(CommParserError):
    def __init__(self):
        super().__init__("method is missing.")
