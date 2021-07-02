# import modules
import math
import time
import random
from adafruit_circuitplayground import cp
import board
import busio as io
import adafruit_ht16k33.matrix
import analogio

# create the I2C instance using default SCL and SDA pins
i2c = io.I2C(board.SCL, board.SDA, frequency=400000)
matrix = adafruit_ht16k33.matrix.Matrix8x8x2(i2c)

# declare analog input object
analog_in = analogio.AnalogIn(board.A1)

ROLL_THRESHOLD = 30

TH1 = 21666
TH2 = 43333

# Lists
number1 = [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0],
      [0, 0, 0, 1, 1, 0, 0, 0],
      [0, 0, 1, 0, 1, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0],
      [0, 0, 1, 1, 1, 1, 1, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
      ]

number2 = [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 2, 2, 2, 2, 0, 0],
      [0, 2, 0, 0, 0, 0, 2, 0],
      [0, 0, 0, 0, 0, 0, 2, 0],
      [0, 0, 2, 2, 2, 2, 0, 0],
      [0, 2, 0, 0, 0, 0, 0, 0],
      [0, 2, 2, 2, 2, 2, 2, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
      ]

number3 = [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 3, 3, 3, 3, 0, 0],
      [0, 3, 0, 0, 0, 0, 3, 0],
      [0, 0, 0, 0, 3, 3, 0, 0],
      [0, 0, 0, 0, 0, 0, 3, 0],
      [0, 3, 0, 0, 0, 0, 3, 0],
      [0, 0, 3, 3, 3, 3, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
      ]

number4 = [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 1, 0, 0],
      [0, 0, 0, 0, 1, 1, 0, 0],
      [0, 0, 0, 1, 0, 1, 0, 0],
      [0, 0, 1, 0, 0, 1, 0, 0],
      [0, 1, 1, 1, 1, 1, 1, 0],
      [0, 0, 0, 0, 0, 1, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
      ]

number5 = [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 2, 2, 2, 2, 2, 2, 0],
      [0, 2, 0, 0, 0, 0, 0, 0],
      [0, 2, 2, 2, 2, 2, 0, 0],
      [0, 0, 0, 0, 0, 0, 2, 0],
      [0, 2, 0, 0, 0, 0, 2, 0],
      [0, 0, 2, 2, 2, 2, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
      ]

number6 = [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 3, 3, 3, 3, 0, 0],
      [0, 3, 0, 0, 0, 0, 0, 0],
      [0, 3, 3, 3, 3, 3, 0, 0],
      [0, 3, 0, 0, 0, 0, 3, 0],
      [0, 3, 0, 0, 0, 0, 3, 0],
      [0, 0, 3, 3, 3, 3, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
      ]

number7 = [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 1, 1, 1, 1, 1, 1, 0],
      [0, 0, 0, 0, 0, 0, 1, 0],
      [0, 0, 0, 0, 0, 1, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0],
      [0, 0, 0, 1, 0, 0, 0, 0],
      [0, 0, 0, 1, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
      ]

number8 = [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 2, 2, 2, 2, 0, 0],
      [0, 2, 0, 0, 0, 0, 2, 0],
      [0, 0, 2, 2, 2, 2, 0, 0],
      [0, 2, 0, 0, 0, 0, 2, 0],
      [0, 2, 0, 0, 0, 0, 2, 0],
      [0, 0, 2, 2, 2, 2, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
      ]

number9 = [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 3, 3, 3, 3, 0, 0],
      [0, 3, 0, 0, 0, 0, 3, 0],
      [0, 3, 0, 0, 0, 0, 3, 0],
      [0, 0, 3, 3, 3, 3, 3, 0],
      [0, 0, 0, 0, 0, 0, 3, 0],
      [0, 0, 3, 3, 3, 3, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
      ]

number10 = [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 1, 0, 0, 1, 1, 0, 0],
      [0, 1, 0, 1, 0, 0, 1, 0],
      [0, 1, 0, 1, 0, 0, 1, 0],
      [0, 1, 0, 1, 0, 0, 1, 0],
      [0, 1, 0, 1, 0, 0, 1, 0],
      [0, 1, 0, 0, 1, 1, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
      ]


my_numbers = [number1, number2, number3, number4, number5,
              number6, number7, number8, number9, number10]

# Initialize the global states
new_roll = False
rolling = False

# Loop forever
while True:

    # gather imput
    reading = analog_in.value

    time.sleep(0.1)

    print(reading)

    if reading > TH2:
        roll_number = random.randrange(0, 10)

    elif reading > TH1:
        roll_number = random.randrange(0, 6)

    else:
        roll_number = random.randrange(0, 3)

    # Compute total acceleration
    X = 0
    Y = 0
    Z = 0
    for i in range(10):
        x, y, z = cp.acceleration
        X = X + x
        Y = Y + y
        Z = Z + z
        time.sleep(0.001)
    X = X / 10
    Y = Y / 10
    Z = Z / 10

    total_accel = math.sqrt(X*X + Y*Y + Z*Z)

    # Play sound if rolling
    if total_accel > ROLL_THRESHOLD:
        roll_start_time = time.monotonic()
        new_roll = True
        rolling = True

    # Rolling momentum
    # Keep rolling for a period of time even after shaking stops
    if new_roll:
        if time.monotonic() - roll_start_time > 0.8:
            rolling = False

    # Compute a random number from 1 to 6
    print(roll_number)

    if rolling:
        # Make some noise and show the dice roll number
        cp.start_tone(random.randrange(400, 1000))

        # light up LEDs
        new_number = my_numbers[roll_number]
        for x in range(8):
            for y in range(8):
                matrix.pixel(x, y, new_number[x][y])

        time.sleep(0.02)
        cp.stop_tone()

    elif new_roll:
        # Show the dice roll number
        new_roll = False

        # light up LEDs
        new_number = my_numbers[roll_number]
        for x in range(8):
            for y in range(8):
                matrix.pixel(x, y, new_number[x][y])
