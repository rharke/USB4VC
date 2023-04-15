import sys

def _is_armbian():
    return True

def _is_rpi():
    return True

if _is_armbian():
    from usb4vc_gpiod import *
elif _is_rpi():
    from RPi.GPIO import *
else:
    sys.stderr.write('Unknown board\n')
    sys.exit(1)
