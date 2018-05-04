import climiko.channel.serial_channel
import queue
import serial
import serial.urlhandler.protocol_loop as protocol_loop
import logging

logging.basicConfig(level=logging.DEBUG)


def test_constructor():
    fake_serial = serial.serial_for_url('loop://?logging=debug', do_not_open=True)  # type: protocol_loop.Serial

    uut = climiko.channel.serial_channel.SerialChannel(fake_serial, True)
    with uut.connect() as session:
        session.write(b'demo')

    fake_serial_queue = fake_serial.queue.queue  # type: queue.deque
    closed = fake_serial_queue.pop()
    data = b''.join(list(fake_serial_queue))




test_constructor()