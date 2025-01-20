import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Pins connected to the servo and LED
servo_pin = 17  # GPIO17
led_pin = 4     # GPIO4 (for the LED)

# Set the servo and LED pins as output
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT)

# Set PWM frequency (50Hz is standard for most servos)
pwm = GPIO.PWM(servo_pin, 50)

# Start PWM with a 0% duty cycle (servo will be at its initial position)
pwm.start(0)

positions = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180]

def set_servo_angle(angle):
    """
    Set the servo angle and control the LED.
    """
    # Convert angle to duty cycle (calibrated for SG-90)
    duty_cycle = max(2, min(12, float(angle) / 18 + 2))  # Clamp to range [2, 12]
    print(f"Setting angle to {angle}° (Duty Cycle: {duty_cycle:.2f}%)")
    
    # Turn the LED on
    GPIO.output(led_pin, GPIO.HIGH)
    
    # Set the servo angle
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.25)  # Short delay for the servo to settle
    
    # Stop sending the PWM signal to reduce jitter
    pwm.ChangeDutyCycle(0)
    
    # Turn the LED off
    GPIO.output(led_pin, GPIO.LOW)

try:
    while True:
        for position in positions:
            print("Moving to 0°...")
            set_servo_angle(position)
            time.sleep(.25)

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    # Clean up PWM and GPIO resources
    print("Stopping PWM and cleaning up GPIO...")
    pwm.ChangeDutyCycle(0)  # Ensure PWM signal is stopped
    pwm.stop()              # Stop the PWM instance
    del pwm                 # Explicitly delete the PWM object
    GPIO.cleanup()          # Reset GPIO settings
    print("Cleanup complete.")
