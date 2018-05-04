from climiko.channel.telnet_channel import TelnetChannel

t = TelnetChannel.from_dict('localhost', {'port': 51234})

with t.connect() as session:
    t.write(b'flaf')
    t.is_alive()
    t.write(b'flaf')
    print(t.read())
