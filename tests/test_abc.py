import unittest
import climiko.channel.base_channel


class TestBaseChannel(unittest.TestCase):

    def test_constructor(self):
        with self.assertRaises(TypeError):
            climiko.channel.base_channel.BaseChannel()


if __name__ == '__main__':
    unittest.main()
