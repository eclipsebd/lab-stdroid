from gpiozero import LED
import time

led = LED(4)
print("Program started")

# Blink the LED
try:
    while True:
        # Turn LED on
        led.on()
        time.sleep(1)  # Wait for 1 second
        
        # Turn LED off
        led.off()
        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    # Release the GPIO pin and close the handle
    led.close()