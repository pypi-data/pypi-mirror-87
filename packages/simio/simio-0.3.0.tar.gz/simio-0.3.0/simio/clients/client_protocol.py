from typing_extensions import Protocol


class ClientProtocol(Protocol):
    """
        Client protocol for type hints
    """

    def __init__(self, *args, **kwargs):  # pylint: disable=super-init-not-called
        ...
