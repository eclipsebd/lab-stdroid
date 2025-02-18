from Adafruit_PCA9685 import PCA9685
from time import sleep

pwm = PCA9685(busnum=1)
pwm.set_pwm_freq(60)  # Set frequency to 60Hz

#channel = 0
#min_pulse = 150  # Min pulse length out of 4096
#max_pulse = 600  # Max pulse length out of 4096

def set_servo_position(channel, position):
    pulse_length = 4096    # The PCA9685 has 4096 steps
    pulse = int(position * pulse_length / 20)  # Convert position to pulse
    pwm.set_pwm(channel, 0, pulse)

# Example usage
while True:
    set_servo_position(0, 0.5)  # Move servo on channel 0 to middle position
    time.sleep(1)
    set_servo_position(0, 2.5)  # Move servo to maximum position
    time.sleep(1)

# Move multiple servos
#set_servo_position(0, 1)  # pan
#set_servo_position(1, 1.5)  # tilt
