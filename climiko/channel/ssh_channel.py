import paramiko
import typing
from .base_channel import BaseChannel


class SSHWrapper(paramiko.SSHClient):
    def __init__(self, hostname, port=None, username=None, password=None, pkey=None, key_filename=None, timeout=None,
                 allow_agent=None, look_for_keys=None, compress=None, sock=None, gss_auth=None, gss_kex=None,
                 gss_deleg_creds=None, gss_host=None, banner_timeout=None, auth_timeout=None, gss_trust_dns=None,
                 host_key_files=None, missing_host_key_policy=None):
        super().__init__()
        self.__host_key_files = host_key_files or list()
        self.__missing_host_key_policy = missing_host_key_policy or paramiko.RejectPolicy
        self.__hostname = hostname
        self.__port = port or paramiko.config.SSH_PORT
        self.__username = username
        self.__password = password
        self.__pkey = pkey
        self.__key_filename = key_filename
        self.__timeout = timeout
        self.__allow_agent = allow_agent
        self.__look_for_keys = look_for_keys
        self.__compress = compress
        self.__sock = sock
        self.__gss_auth = gss_auth
        self.__gss_kex = gss_kex
        self.__gss_deleg_creds = gss_deleg_creds
        self.__gss_host = gss_host
        self.__banner_timeout = banner_timeout
        self.__auth_timeout = auth_timeout
        self.__gss_trust_dns = gss_trust_dns




class SSHChannel(BaseChannel):
    def __init__(self, device: paramiko.SSHClient, verbose: bool=False):
        super().__init__(verbose)
        self.device = device

    @classmethod
    def from_dict(cls, host: str, settings: typing.Dict=None, verbose: bool=False):
        settings = dict(settings) if settings else dict()
        settings['host'] = host

        return cls(paramiko.SSHClient(), verbose)

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
