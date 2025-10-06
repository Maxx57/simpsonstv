#!/usr/bin/python3

import logging
import gpiod
import time
import os

# GPIO pin assignments (BCM numbering - same as original)
BUTTON_PIN = 26
BACKLIGHT_PIN = 18
AUDIO_PIN = 19

chip = None
button_line = None
backlight_line = None


def turnOnScreen():
    logging.info("turnOnScreen")
    # Enable audio
    os.system(f"gpioset 0 {AUDIO_PIN}=1")  # Enable audio output
    # Turn on screen backlight
    backlight_line.set_value(1)


def turnOffScreen():
    logging.info("turnOffScreen")
    # Mute audio
    os.system(f"gpioset 0 {AUDIO_PIN}=0")  # Disable audio output
    # Turn off screen backlight
    backlight_line.set_value(0)


def main():
    global chip, button_line, backlight_line
    
    logging.getLogger().setLevel(logging.INFO)

    # Open GPIO chip (gpiochip0 for Raspberry Pi)
    chip = gpiod.Chip('gpiochip0')
    
    # Set pin 26 as input to monitor button press (with pull-up)
    button_line = chip.get_line(BUTTON_PIN)
    button_line.request(consumer="buttons", type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
    
    # Set pin 18 as output to control screen backlight
    backlight_line = chip.get_line(BACKLIGHT_PIN)
    backlight_line.request(consumer="buttons", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])

    turnOffScreen()
    screen_on = False

    try:
        while True:
            # Read button state (1 = not pressed with pull-up, 0 = pressed)
            inp = button_line.get_value()
            if inp != screen_on:
                screen_on = inp
                if screen_on:
                    turnOnScreen()
                else:
                    turnOffScreen()
            time.sleep(0.3)
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    finally:
        if button_line:
            button_line.release()
        if backlight_line:
            backlight_line.release()
        if chip:
            chip.close()


if __name__ == "__main__":
    main()