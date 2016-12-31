import RPi.GPIO as GPIO
import time

class Button:
    def __init__(self, button_pin=12):
        self.button_pin = button_pin
        GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set button_pin's mode is input, and pull up to high level(3.3V)
        pass

    def callback(self, ev=None):
        if GPIO.input(self.button_pin):
            return
        print("button pressed")
        print(ev, GPIO.input(self.button_pin))
        self.islongPress()

    def islongPress(self, pressed=1):
        counter = 0
        while (pressed == 1):
            if not GPIO.input(self.button_pin):
                counter += 1
                if (counter >= 20):
                    print("LongPress")
                    pressed = 0
                    return True
                else:
                    time.sleep(.2)
            else:
                print("Not LongPress")
                pressed = 0
        return False

    def ignore(self):
        GPIO.remove_event_detect(self.button_pin)

    def listen(self, callback):
        if not callback:
            callback = self.callback
        GPIO.add_event_detect(self.button_pin,
                              GPIO.FALLING,
                              callback=callback,
                              bouncetime=500)

