import subprocess
import time

leftCommand = "echo {color} > /sys/class/leds/system76::kbd_backlight/color_left"
rightCommand = "echo {color} > /sys/class/leds/system76::kbd_backlight/color_right"
centerCommand = "echo {color} > /sys/class/leds/system76::kbd_backlight/color_center"
brightnessCommand = "echo {brightness} > /sys/class/leds/system76::kbd_backlight/brightness"


swicted_off = '000000'
leftColor = swicted_off
centerColor = swicted_off
rightColor = swicted_off


def get_color(step_count=16):
    step_size = 255/(step_count/3)

    red = [r for r in range(0, 256, step_size)]
    green = [g for g in range(0, 256, step_size)]
    blue = [b for b in range(0, 256, step_size)]

    while True:
        for r in red:
            for g in green:
                for b in blue:
                    yield '{:02X}{:02X}{:02X}'.format(r, g, b)


def get_brightness(step_count=16, low=8, high=255):
    real_low = 0
    real_high = 256

    if low < real_low:
        low = real_low

    if high > real_high:
        high = real_high

    while True:
        for n in range(low, high, high / step_count):
            yield n
        for n in reversed(range(low, high, high / step_count)):
            yield n


brightness_generator = get_brightness()

for i in get_color():
    brightness = brightness_generator.next()
    print('color', i)
    print('brightness', brightness)

    if leftColor == swicted_off and centerColor == swicted_off and rightColor == swicted_off:
        leftColor = i
    elif leftColor != swicted_off and centerColor == swicted_off and rightColor == swicted_off:
        centerColor = i
    elif leftColor != swicted_off and centerColor != swicted_off and rightColor == swicted_off:
        rightColor = i
    else:
        rightColor = centerColor
        centerColor = leftColor
        leftColor = i

    subprocess.check_output(['bash', '-c', leftCommand.format(color=leftColor)])
    subprocess.check_output(['bash', '-c', centerCommand.format(color=centerColor)])
    subprocess.check_output(['bash', '-c', rightCommand.format(color=rightColor)])
    subprocess.check_output(['bash', '-c', brightnessCommand.format(brightness=brightness)])

    time.sleep(0.1)




