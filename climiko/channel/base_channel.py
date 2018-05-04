import logging
import abc


log = logging.getLogger(__name__)


class BaseChannel(abc.ABC):
    def __init__(self, verbose):
        self.verbose = verbose

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @property
    @abc.abstractmethod
    def _name(self) -> str:
        ...

    @abc.abstractmethod
    def _connect(self):
        ...

    @abc.abstractmethod
    def _disconnect(self):
        ...

    @abc.abstractmethod
    def _write(self, data: bytes):
        ...

    @abc.abstractmethod
    def _read(self) -> bytes:
        ...

    @abc.abstractmethod
    def _send_break(self):
        ...

    @abc.abstractmethod
    def _is_alive(self) -> bool:
        ...

    @abc.abstractmethod
    def _clear_input_buffer(self):
        ...

    # Should not be implemented

    def _verbose_print(self, data, raw=False):
        if self.verbose:
            if raw:
                print(data)
            else:
                print('Serial[{}]: {}'.format(self.name, data))

    @property
    def name(self) -> str:
        return self._name

    def connect(self):
        self._verbose_print("connecting")
        self._connect()
        return self

    def disconnect(self):
        self._verbose_print("disconnecting")
        return self._disconnect()

    def write(self, data: bytes):
        """Generic handler that will write to both SSH and telnet channel.

        :param data: data to be written to the channel
        :type data: bytes
        """
        self._verbose_print("writing")
        log.debug("write: {}".format(data))
        return self._write(data)

    def read(self):
        self._verbose_print("reading")
        data = self._read()
        log.debug("read: {}".format(data))
        return data

    def is_alive(self):
        return self._is_alive()

    def send_break(self):
        self._send_break()

    def clear_input_buffer(self):
        return self._clear_input_buffer()
