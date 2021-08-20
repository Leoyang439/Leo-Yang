import board
import time
import busio
import random
from board import SCL, SDA
from adafruit_neotrellis.neotrellis import NeoTrellis
from digitalio import DigitalInOut, Direction, Pull
import neopixel
import pulseio
from adafruit_motor import servo

# declare a PWMOut object
pwm = pulseio.PWMOut(board.A1, duty_cycle=2 ** 15, frequency=50)

# create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA, frequency=400000)

# declare a servo object
thisServo = servo.Servo(pwm)

# create the trellis
trellis = NeoTrellis(i2c_bus)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10)

button = DigitalInOut(board.D4)
button.direction = Direction.INPUT
button.pull = Pull.DOWN

preButton = False
buttonTime = 0
status = 0

# Servo
angle = 30
OPEN = 0
LOCKED = 30

# some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)

passWord = []
rightPassWord1 = []
rightPassWord2 = []
rightPassWord = [0, 1, 2, 3, 4, 5]
wrongPass = []

COLORS = [RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, RED, YELLOW,
          GREEN, CYAN, BLUE, PURPLE, RED, YELLOW, GREEN, CYAN]

CHOICES = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3]
newCHOICES = []

# COLOR DISPLAY
RIGHT = GREEN
WRONG = RED

def LOCKCONTROL(angle):
    thisServo.angle = angle

def DISPLAYCONTROL(colorStatus):
    print(colorStatus, "password !")
    for x in range(16):
        trellis.pixels[x] = colorStatus
    # Display 2 seconds
    time.sleep(2)
    for x in range(16):
        trellis.pixels[x] = OFF

def FUNCTIONBUTTON():
    trellis.pixels[15] = CYAN

def RESETINTERFACE():
    for x in range(6):
        trellis.pixels[x] = COLORS[x]
    FUNCTIONBUTTON()
    rightPassWord1.clear()

def SHUFFLE():

    global CHOICES
    global newCHOICES

    newCHOICES.clear()

    # Shuffle the CHOICES
    newCHOICES = sorted(CHOICES, key=lambda _: random.random())
    print("newCHOICES is:", newCHOICES)
    print("SHUFFLED")
    # Display new CHOICES
    for x in range(16):
        trellis.pixels[x] = COLORS[newCHOICES[x]]

# this will be called when button events are received
def blink(event):
    global status
    global rightPassWord
    global newCHOICES

    # turn the LED on when a rising edge is detected
    if event.edge == NeoTrellis.EDGE_RISING:
        trellis.pixels[event.number] = WHITE

    # turn the LED off when a rising edge is detected
    elif event.edge == NeoTrellis.EDGE_FALLING:
        trellis.pixels[event.number] = OFF

    # enter the Password
    if status == 0:

        if angle == 0:
            FUNCTIONBUTTON()
            if event.edge == NeoTrellis.EDGE_FALLING:
                if event.number == 15:
                    # Close
                    LOCKCONTROL(LOCKED)
                    passWord.clear()
                    SHUFFLE()

        elif angle == 30:

            # add number into passWord
            newNumber = event.number
            if event.edge == NeoTrellis.EDGE_FALLING:
                passWord.append(newCHOICES[newNumber])
                print("newNumber is:", newNumber)

            passWordLength = len(passWord)
            print("passWordLength is:", passWordLength)
            # print("newNumber is:", newNumber)
            print("passWord is:", passWord)

            # compare with rightPassWord
            if passWordLength == 6:
                # Right Password
                if passWord == rightPassWord:
                    DISPLAYCONTROL(RIGHT)
                    # Open
                    LOCKCONTROL(OPEN)
                    # LOCKBUTTON
                    FUNCTIONBUTTON()
                # Wrong Password
                else:
                    DISPLAYCONTROL(WRONG)
                    SHUFFLE()

            # clear passWord
            if passWordLength >= 6:
                passWord.clear()

            # Lock safe
            if thisServo.angle == OPEN:
                if event.edge == NeoTrellis.EDGE_FALLING:
                    if event.number == 15:
                        # Close
                        LOCKCONTROL(LOCKED)
                        passWord.clear()
                        SHUFFLE()

    # Reset Password
    elif status == 1:

        if event.edge == NeoTrellis.EDGE_FALLING:
            # Enter new Password
            if event.number != 15:
                rightPassWord1.append(event.number)
                print("rightPassWord1 is:", rightPassWord1)

                # Check new password length
                if len(rightPassWord1) >= 7:
                    DISPLAYCONTROL(WRONG)
                    RESETINTERFACE()

            # Confirm new Password
            else:
                # Check new Password Length
                if len(rightPassWord1) == 6:
                    # Copy new password to rightPassWord
                    rightPassWord.clear()
                    rightPassWord = rightPassWord1.copy()
                    DISPLAYCONTROL(RIGHT)
                    rightPassWord1.clear()
                    print("rightPassWord is:", rightPassWord)

                else:
                    DISPLAYCONTROL(WRONG)
                    RESETINTERFACE()

for i in range(16):
    # activate rising edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)
    # activate falling edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
    # set all keys to trigger the blink callback
    trellis.callbacks[i] = blink

    # cycle the LEDs on startup
    trellis.pixels[i] = WHITE
    time.sleep(0.05)

for i in range(16):
    trellis.pixels[i] = OFF
    time.sleep(0.05)

SHUFFLE()

while True:

    # reset button status check
    # print(button.value)
    time.sleep(0.05)

    if button.value != preButton:
        preButton = button.value

        # check if the button has changed from not pressed to pressed
        if button.value is True:
            startTime = time.monotonic()
            print("startTime is:", startTime)
            time.sleep(0.05)
        else:
            buttonTime = time.monotonic() - startTime
            print("buttonTime is:", buttonTime)

            if buttonTime > 2:
                pixels[0] = (255, 0, 0)
                status = 1

                for p in range(15):
                    if p < 6:
                        trellis.pixels[p] = COLORS[p]

                    elif p > 14:
                        trellis.pixels[p] = CYAN

                    else:
                        trellis.pixels[p] = OFF

            else:
                status = 0

                pixels[0] = (0, 0, 0)

                FUNCTIONBUTTON()

            startTime = 0
            buttonTime = 0
            time.sleep(0.05)

    # print("The status is:", status)
    # time.sleep(2)

    # call the sync function call any triggered callbacks
    trellis.sync()
    # the trellis can only be read every 17 millisecons or so
    time.sleep(0.02)
