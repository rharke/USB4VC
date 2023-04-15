import gpiod
import sys
import threading

BCM = None

LOW = 0
HIGH = 1

IN = gpiod.LINE_REQ_DIR_IN
OUT = gpiod.LINE_REQ_DIR_OUT

PUD_OFF = gpiod.LINE_REQ_FLAG_BIAS_DISABLE
PUD_DOWN = gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN
PUD_UP = gpiod.LINE_REQ_FLAG_BIAS_PULL_UP

BOTH = gpiod.LINE_REQ_EV_BOTH_EDGES
FALLING = gpiod.LINE_REQ_EV_FALLING_EDGE
RISING = gpiod.LINE_REQ_EV_RISING_EDGE

PIN_MAP = {
    27: '7J1 Header Pin13', # PLUS_BUTTON_PIN
    19: '7J1 Header Pin35', # MINUS_BUTTON_PIN
    22: '7J1 Header Pin15', # ENTER_BUTTON_PIN
    21: '7J1 Header Pin40', # SHUTDOWN_BUTTON_PIN
    25: '7J1 Header Pin22', # PBOARD_RESET_PIN
    12: '7J1 Header Pin32', # PBOARD_BOOT0_PIN
    26: '7J1 Header Pin37', # SLEEP_LED_PIN
    20: '7J1 Header Pin38', # PCARD_BUSY_PIN
    16: '7J1 Header Pin36', # SLAVE_REQ_PIN
    5: '7J1 Header Pin29', # OLED
    6: '7J1 Header Pin31', # OLED
}

lines = {}
flags = {}
events = {}

def setmode(_):
    pass

def cleanup():
    pass

def _get_line(channel):
    line = lines.get(channel)
    if not line:
        line = gpiod.find_line(PIN_MAP[channel])
        line.request(sys.argv[0])
        lines[channel] = line
    return line

def setup(channel, direction, pull_up_down=None):
    line = _get_line(channel)
    if direction == OUT:
        line.set_direction_output()
    else:
        line.set_direction_input()
    if pull_up_down is not None:
        line.set_flags(pull_up_down)
    flags[channel] = pull_up_down

def output(channel, value):
    line = _get_line(channel)
    line.set_value(value)

def input(channel):
    line = _get_line(channel)
    return line.get_value()

def _poll_event(channel, edge):
    line = lines.get(channel)
    line.set_config(edge, flags[channel])
    while True:
        if event_wait(sec=1):
            event = line.event_read()
            old_events = events.get(channel, [])
            old_events.append(event)
            events[channel] = old_events

def add_event_detect(channel, edge):
    t = threading.Thread(target=_poll_event, args=[line, edge])
    t.daemon = True
    t.start()
