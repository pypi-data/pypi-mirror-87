from ezblock.modules import Buzzer
from ezblock import PWM
from ezblock.modules import RGB_LED
from ezblock import Taskmgr
from ezblock import Pin, Ultrasonic
import i2clcd
import RPi.GPIO as GPIO
import time

# Usage example
#buzz = Buzz()
#buzz.play("B7")
class Buzz():
    def __init__(self, pwm="P8"):
        self.buzz = Buzzer(PWM(pwm))
        self.notes = {"E7" : 2637, "F7" : 2793, "G7" : 3136, "A7" : 3520, "B7" : 3951}

    def play(self, note, duration=1000):
        # duration is in ms

        print(" [.] Playing", note)
        freq = self.notes[note]
        self.buzz.play(freq, duration)

# Usage example
# fill a line by the text
'''
lcd.print_line('hello', line=0)
lcd.print_line('world!', line=1, align='RIGHT')

# print text at the current cursor position
lcd.move_cursor(1, 0)
lcd.print('the')

# custom character
char_celsius = (0x10, 0x06, 0x09, 0x08, 0x08, 0x09, 0x06, 0x00)
lcd.write_CGRAM(char_celsius, 0)
lcd.move_cursor(0, 6)
lcd.print(b'CGRAM: ' + i2clcd.CGRAM_CHR[0])
'''
class LCD1602:
    def __init__(self):
        self.lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x27, lcd_width=16)
        self.lcd.init()
        print(" [.] Created LCD1602", self.lcd)

    def write_line(self, line, data, align='LEFT'):
        self.lcd.print_line(data, line)


class Leds():
    def __init__(self, led_colors=['red', 'yellow', 'green'], available_pins=['P9', 'P10', 'P11']):
        self.available_pins = available_pins 
        self.leds = self.__create_leds(led_colors)

    # private method
    def __create_leds(self, led_colors):
        leds = dict()
        for color in led_colors:
            leds[color] = dict()
            leds[color]['state'] = 0

            try:
                leds[color]['pin'] = self.available_pins.pop(0) # pop(0) to get first available pin
                leds[color]['pwm'] = PWM(leds[color]['pin'])
                leds[color]['pwm'].freq(50)           # set frequency (go)
                leds[color]['pwm'].pulse_width(0)          # off it

            except IndexError as e:
                print("Not enough available pins to perform led creation", led_colors, e)

        print(" [.] Created leds", leds)
        return leds


    def stop(self):
        for color in self.leds:
            if self.leds[color]['state']:
                self.leds[color]['pwm'].off()          # off it

    def toggle(self, color):
        try:
            if self.leds[color]['state'] == 0:
                self.leds[color]['pwm'].pulse_width(100)         # set pulse_width (go)
            else:
                self.leds[color]['pwm'].pulse_width(0)          # off it

            self.leds[color]['state'] = 1 - self.leds[color]['state']
        except KeyError as e:
            print("The color", color, "doesn't exist!")
            print("Available colors:", self.leds)


class RGB():
    def __init__(self, p_red="P9", p_green="P10", p_blue="P11"):
        self.rgb = RGB_LED(PWM(p_red), PWM(p_green), PWM(p_blue))
        self.color_dict = {'red': '#ff0000', 'orange': '#ffa500', 'yellow': '#ffff00', 'green': '#008000', 'blue': '#0000ff', 'indigo': '#4b0082', 'violet': 'ee82ee', 'white': '#ffffff', 'black': '000000'}

    def write(self, color):
        print(" [.] Update RGB led state to", color)
        color = self.color_dict[color]
        self.rgb.write(color)
        

# Usage example
#stats = PiStatus()
#print(stats.status())
class PiStatus():
    def __init__(self):
        self.taskmgr = Taskmgr()
        print(" [.] Created status verifier", self.taskmgr)
    def status(self):
        return str(self.taskmgr.read())


# Usage example
#reader = FrontalDistance()
#print(reader.read())
class FrontalDistance():
    def __init__(self, trig="D0", echo="D1"):
        self.ultrasonic = Ultrasonic(Pin(trig), Pin(echo)) # create an Ultrasonic object from pin
        print(" [.] Created ultrasonic object", self.ultrasonic) 

    def read(self):
        return self.ultrasonic.read() # read an analog value


'''# Usage example
wheels = Wheels()

wheels.forward()

time.sleep(5)
wheels.stop()

wheels.right()
time.sleep(2)

wheels.left()
time.sleep(2)

wheels.backward()

time.sleep(2)
wheels.stop()
'''
class Wheels():

    def __init__(self, motor1_pwm_pin="P13", motor2_pwm_pin="P12", motor1_dir_pin="D4", motor2_dir_pin="D5"):

        self.motor1_pwm = PWM(motor1_pwm_pin)
        self.motor2_pwm = PWM(motor2_pwm_pin)
        self.motor1_dir = Pin(motor1_dir_pin)
        self.motor2_dir = Pin(motor2_dir_pin)

        self.motor_direction = [self.motor1_dir, self.motor2_dir]
        self.motor_speed = [self.motor1_pwm, self.motor2_pwm]

        print(" [.] Created left and right wheel in stop position")

        self.cali_dir_value = [1, -1]
        self.cali_speed_value = [0, 0]

        self.PERIOD = 4095
        self.PRESCALER = 10

        for pin in self.motor_speed:
            pin.period(self.PERIOD)
            pin.prescaler(self.PRESCALER)

        self.motor_direction_calibration(1, 1) # motor1 in forward mode
        self.motor_direction_calibration(2, 1) # motor2 in forward mode


    def stop(self):
        self.set_motor_speed(1, 0)               # Stop motor1
        self.set_motor_speed(2, 0)               # Stop motor2


    def forward(self):
        self.motor_direction_calibration(1, 1) 
        self.motor_direction_calibration(2, -1) 
        self.set_motor_speed(1, 25)               # Speed motor1
        self.set_motor_speed(2, 21)               # Speed motor2


    def right(self):
        self.motor_direction_calibration(1, 1) 
        self.motor_direction_calibration(2, -1) 
        self.set_motor_speed(1, 0)                # Stop motor1
        self.set_motor_speed(2, 25)               # Speed motor2
        

    def left(self):
        self.motor_direction_calibration(1, 1) 
        self.motor_direction_calibration(2, -1) 
        self.set_motor_speed(2, 0)                # Stop motor2
        self.set_motor_speed(1, 25)               # Speed motor1

    
    def backward(self):
        self.stop()

        self.motor_direction_calibration(1, -1) 
        self.motor_direction_calibration(2, 1) 
        self.set_motor_speed(1, 25)
        self.set_motor_speed(2, 21)


    def set_motor_speed(self, motor, speed):
        motor -= 1
        if speed >= 0:
            direction = 1 * self.cali_dir_value[motor]
        elif speed < 0:
            direction = -1 * self.cali_dir_value[motor]
        speed = abs(speed)
        if speed != 0:
            speed = int(speed /2 ) + 30
        speed = speed - self.cali_speed_value[motor]
        if direction > 0:
            self.motor_direction[motor].high()
            self.motor_speed[motor].pulse_width_percent(speed)
        else:
            self.motor_direction[motor].low()
            self.motor_speed[motor].pulse_width_percent(speed)


    def motor_speed_calibration(self, value):
        if value < 0:
            self.cali_speed_value[0] = 0
            self.cali_speed_value[1] = abs(value)
        else:
            self.cali_speed_value[0] = abs(value)
            self.cali_speed_value[1] = 0


    def motor_direction_calibration(self, motor, value):
        # 1: positive direction
        # -1: negative direction
        motor -= 1
        self.cali_dir_value[motor] = value
        


