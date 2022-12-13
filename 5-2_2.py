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

def adc(i, value):
    if i == -1:
        return value
    dec2dac(value + 2**i)
    time.sleep(0.001)
    compValue = GPIO.input(comparator)
    if compValue == 0:
        return adc(i-1, value)
    else:
        return adc(i-1, value+2**i)
    

try:
    while True:
        value = adc(bits-1, 0)
        voltage = maxVoltage / levels * value
        print("Digital value: {:^3}, Analog value: {:.2f} V".format(value, voltage))
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)