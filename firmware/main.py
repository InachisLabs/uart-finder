import board
import adafruit_dotstar
import busio
import digitalio
import time
 
###############################################################################
## Parameters

# UART baudrates to scan.
BAUDRATES = [9600, 19200, 57000, 115200]

# ms timeout for blocking uart.read(...).
# Time to test a pin-pair = TIMEOUT * 2 * len(BAUDRATES) + 1ms
TIMEOUT  = 10

# Global objects
rgb = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
led = digitalio.DigitalInOut(board.D13)

###############################################################################
## Functions

def testecho(uart, direction):
    uart.write(' ')
    data = uart.read(1)

    if not data:
        return

    elif data == b' ':
        if direction == 0:
            rgb[0] = (0xff, 0, 0)
        else:
            rgb[0] = (0,0,0xff)
        print(uart.baudrate)
        time.sleep(1)

    elif data in range(0x21, 0x7e):
        if direction == 0:
            rgb[0] = (0xff,0xff,0)
        else:
            rgb[0] = (0,0xff,0xff)
        print(uart.baudrate)
        print(data)
        time.sleep(1)

    rgb[0] = (0,0,0)

def setup():
    rgb[0] = (0,0,0)
    led.direction = digitalio.Direction.OUTPUT

def main_loop():
    while True:
        led.value = True
        led.value = False
        for baudrate in BAUDRATES:
            uart = busio.UART(board.D0, board.D4, baudrate=baudrate, timeout=TIMEOUT)
            testecho(uart, 0)
            uart.deinit()

            uart = busio.UART(board.D4, board.D0, baudrate=baudrate, timeout=TIMEOUT)
            testecho(uart, 1)
            uart.deinit()

###############################################################################
## Entrypoint

setup()
main_loop()
