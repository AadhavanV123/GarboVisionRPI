# import RPi.GPIO as GPIO
# import time

# GPIO.setmode(GPIO.BCM)

# BUZZER = 18
# GPIO.setup(BUZZER, GPIO.OUT)

# buzzer = GPIO.PWM(BUZZER, 1000)  # 1000 Hz tone
# for i in range(5):
#     buzzer.start(2)  # 20% duty cycle = quieter sound
#     time.sleep(2)
#     buzzer.stop()
#     time.sleep(2)
# GPIO.cleanup()

# from RPLCD.i2c import CharLCD
# import time

# lcd = CharLCD('PCF8574', 0x27)

# lcd.write_string("GarboVision Bot")
# time.sleep(3)

# lcd.clear()
# lcd.write_string("helloo")
# lcd.cursor_pos = (1, 0)
# lcd.write_string("it is working :)")

import RPi.GPIO as GPIO
import time

servo_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)   # 50Hz for servo
pwm.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

set_angle(0)
time.sleep(1)
set_angle(90)
time.sleep(1)
set_angle(180)

pwm.stop()
GPIO.cleanup()

def main():
    print("pogchamp")

if __name__ == '__main__':
    main()