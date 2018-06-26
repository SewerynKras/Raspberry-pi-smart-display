import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


class Device(object):

    def __init__(self, pin, state):
        """Creates a device object used to control GPIO devices

        Arguments:
            pin {int} -- Pin that the device is connected to (using BCM mode)
            state {string} -- 'input' or 'output'
        """
        self.pin = pin
        self.state = state

        if state == "input":
            GPIO.setup(self.pin, GPIO.IN)
        elif state == "output":
            GPIO.setup(self.pin, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.pin, 1)

    def turn_off(self):
        GPIO.output(self.pin, 0)

    def get_state(self):
        return bool(GPIO.input(self.pin))


def clean():
    GPIO.cleanup()
