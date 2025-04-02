from time import sleep

import gpiozero

RELAY_PIN = 16

def toggle_pump_relay():
    relay = gpiozero.OutputDevice(RELAY_PIN)
    relay.toggle()
    print(f'Relay status is: {relay.value}')


if __name__ == '__main__':
    print('Starting the test script!')
    while True:
        sleep(2)
        toggle_pump_relay()
