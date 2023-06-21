import sounddevice as sd

devices = sd.query_devices()
for device in devices:
    if device['max_input_channels'] > 0:
        print('Device name:', device['name'])
        print('Maximum input channels:', device['max_input_channels'])
        print()

devices = sd.query_devices()
for device in devices:
    if device['max_input_channels'] > 0:
        print('Device name:', device['name'])
        print('Default samplerate:', device['default_samplerate'])
        print()