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


def get_color():
    colors = [
        '000000',
        '0000FF',
        '00FF00',
        '00FFFF',
        'FF0000',
        'FF00FF',
        'FFFF00',
        'FFFFFF'
    ]
    while True:
        for i in colors:
            yield i


def get_brightness():
    while True:
        for n in range(0, 255, 16):
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

    time.sleep(1)




