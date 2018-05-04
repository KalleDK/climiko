import queue
import serial
import serial.urlhandler.protocol_loop as protocol_loop
from unittest import TestCase
from climiko.channel.serial_channel import SerialChannel


def get_queue_result(serial_queue: queue.Queue):
    buffer = serial_queue.queue  # type: queue.deque
    closed = buffer.pop()
    data = b''.join(list(buffer))
    return closed, data


class TestSerialSettings(TestCase):
    def test_constructor(self):
        fake_serial = serial.serial_for_url('loop://', do_not_open=True)  # type: protocol_loop.Serial

        input_data = b'demo'

        uut = SerialChannel(fake_serial, False)
        with uut.connect() as session:
            session.write(input_data)

        closed, data = get_queue_result(fake_serial.queue)

        self.assertIsNone(closed, 'Serial was not closed')
        self.assertEqual(data, input_data, 'Data was not written')
