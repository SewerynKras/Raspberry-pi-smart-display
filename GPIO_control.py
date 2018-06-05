import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


class Device(object):
    """Creates a device object used to control GPIO devices

    Arguments:
        pin {int} -- Pin that the device is connected to (using BCM mode)
        type {string} -- 'input' or 'output'

    Keyword Arguments:
        n_open {bool} -- if True calling turn_on will write
                low(1) to the pin (default: {Flase})
        initial_state {int} -- what should be writen to
                the pin immediately (default: {0})
    """

    def __init__(self, pin, itype, n_open=False, initial_state=0):
        self.pin = pin
        self.initial_state = initial_state
        self.state = initial_state
        self.type = itype

        if n_open is True:
            self.on = 0
        else:
            self.on = 1
        if itype == "input":
            GPIO.setup(self.pin, GPIO.IN)
        else:
            GPIO.setup(self.pin, GPIO.OUT, initial=self.initial_state)

    def turn_on(self):
        GPIO.output(self.pin, self.on)
        self.state = self.on

    def turn_off(self):
        GPIO.output(self.pin, not self.on)
        self.state = not self.on

    def get_state(self):
        if self.type == "input":
            return bool(GPIO.input(self.pin))
        else:
            return self.state


def clean():
    GPIO.cleanup()
