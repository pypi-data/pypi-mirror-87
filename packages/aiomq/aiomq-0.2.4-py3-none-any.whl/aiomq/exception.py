class AioMQError(RuntimeError):
    pass


class AioMQReceiveFormatError(AioMQError):
    pass


class AioMQCloseWebsocket(AioMQError):
    pass
