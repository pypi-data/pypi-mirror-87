import random

try:
    import RPi.GPIO as GPIO

    GPIO.setwarnings(False)
except Exception:

    class GPIO:
        OUT = 0
        IN = 0
        HIGH = True
        LOW = False
        BCM = 0

        @staticmethod
        def setup(*args, **kwargs):
            pass

        @staticmethod
        def output(pin, high_or_low):
            pass

        @staticmethod
        def input(pin):
            return random.randint(0, 100)

        @staticmethod
        def setmode(mode):
            pass

        @staticmethod
        def cleanup():
            pass
