import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3
comparator = 4
troykaModule = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(comparator, GPIO.IN)
GPIO.setup(troykaModule, GPIO.OUT, initial=GPIO.HIGH)

def dec2bin(n):
    return [int(bit) for bit in bin(n)[2:].zfill(bits)]

def dec2dac(n):
    signal = dec2bin(n)
    GPIO.output(dac, signal)
    return signal

def adc():
    for i in range(256):
        dec2dac(i)
        time.sleep(0.001)
        comp_value = GPIO.input(comparator)
        if comp_value == 0:
            return i

try:
    while True:
        value = adc()
        voltage = maxVoltage / levels * value
        print("Digital value: {:^3}, Analog value: {:.2f} V".format(value, voltage))
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)