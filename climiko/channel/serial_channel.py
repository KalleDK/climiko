import serial
import typing
from .base_channel import BaseChannel


class SerialChannel(BaseChannel):
    def __init__(self, device: serial.Serial, verbose: bool=False):
        super().__init__(verbose)
        self.device = device

    @classmethod
    def from_dict(cls, url: str, settings: typing.Dict=None, verbose: bool=False):
        settings = dict(settings) if settings else dict()
        settings['do_not_open'] = True
        settings['url'] = url

        return cls(serial.serial_for_url(**settings), verbose)

    @property
    def _name(self):
        return self.device.name

    def _connect(self):
        self.device.open()

    def _disconnect(self):
        self.device.close()

    def _write(self, data: bytes):
        self.device.write(data)
        self.device.flush()

    def _read(self) -> bytes:
        return self.device.read_all()

    def _is_alive(self) -> bool:
        return self.device.is_open

    def _send_break(self):
        self.device.send_break()

    def _clear_input_buffer(self):
        self.device.reset_input_buffer()
