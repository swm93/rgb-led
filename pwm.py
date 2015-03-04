import RPi.GPIO as GPIO



class PWM(GPIO.PWM):
    def __init__(self, pin_num, pwm_frequency):
        self.duty_cycle = 0

        super().__init__(pin_num, pwm_frequency)

    def ChangeDutyCycle(self, dc):
        self.duty_cycle = dc
        super().ChangeDutyCycle(dc)
