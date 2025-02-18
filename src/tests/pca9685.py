from Adafruit_PCA9685 import PCA9685
from time import sleep

pwm = PCA9685(busnum=1)
pwm.set_pwm_freq(60)  # Set frequency to 60Hz

def set_servo_position(channel, position):
    print("set_servo_position:", channel, "-", position)
    min_pulse = 150  # Min pulse length
    max_pulse = 600  # Max pulse length
    pulse = int(min_pulse + (position * (max_pulse - min_pulse) / 2.5))  # Scale position
    pwm.set_pwm(channel, 0, pulse)


# Example usage
while True:
    set_servo_position(0, 0.5)
    sleep(1)
    set_servo_position(0, 1.5)
    sleep(1)
    set_servo_position(0, 2.5)
    sleep(1)

    set_servo_position(1, 0.5)
    sleep(1)
    set_servo_position(1, 1.5)
    sleep(1)
    set_servo_position(1, 2.5)
    sleep(1)

