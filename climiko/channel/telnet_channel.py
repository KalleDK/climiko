import telnetlib
import typing
import socket
from .base_channel import BaseChannel


# noinspection PyProtectedMember
DEFAULT_TIMEOUT = socket._GLOBAL_DEFAULT_TIMEOUT


class TelnetWrapper(telnetlib.Telnet):
    def __init__(self, host=None, port=0, timeout=DEFAULT_TIMEOUT):
        self.__host = host
        self.__port = port
        self.__timeout = timeout
        super().__init__()

    def connect(self):
        self.open(self.__host, self.__port, self.__timeout)

    def send_command(self, data):
        self.sock.sendall(telnetlib.IAC + data)


class TelnetChannel(BaseChannel):
    def __init__(self, device: TelnetWrapper, verbose: bool=False):
        super().__init__(verbose)
        self.device = device

    @classmethod
    def from_dict(cls, host: str, settings: typing.Dict=None, verbose: bool=False):
        settings = dict(settings) if settings else dict()
        settings['host'] = host

        return cls(TelnetWrapper(**settings), verbose)

    @property
    def _name(self):
        return 'telnet://{}:{}'.format(self.device.host, self.device.port)

    def _connect(self):
        self.device.connect()

    def _disconnect(self):
        self.device.close()

    def _write(self, data: bytes):
        self.device.write(data)

    def _read(self) -> bytes:
        return self.device.read_very_eager()

    def _is_alive(self) -> bool:
        try:
            self.device.send_command(telnetlib.NOP)
        except AttributeError:
            return False

        return True

    def _send_break(self):
        self.device.send_command(telnetlib.BRK)

    def _clear_input_buffer(self):
        self.read()
