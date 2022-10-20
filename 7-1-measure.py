import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
GPIO.setmode(GPIO.BCM)
DAC = [26, 19, 13, 6, 5, 11, 9, 10]
LEDS = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troykamodule = 17

GPIO.setup(DAC, GPIO.OUT)
GPIO.setup(troykamodule, GPIO.OUT,  initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(LEDS, GPIO.OUT)

measure = []


def dec2bin(value):
    return[int(element) for element in bin(value)[2:].zfill(8)]


def adc():
    GPIO.output(troykamodule, 1)
    volt = 0
    for i in range(0, 8):
        GPIO.output(DAC, dec2bin(volt + 2**(7 - i)))
        time.sleep(0.001)
        if GPIO.input(comp) == 1:
            volt = volt + 2**(7 - i)
    return volt


def adc0():
    GPIO.output(troykamodule, 0)
    volt = 0
    for i in range(0, 8):
        GPIO.output(DAC, dec2bin(volt + 2**(7 - i)))
        time.sleep(0.001)
        if GPIO.input(comp) == 1:
            volt = volt + 2**(7 - i)
    return volt


start = time.time()

try:
    while True:
        volt = adc()
        print(dec2bin(volt), volt*3.3/256, volt)
        GPIO.output(LEDS[8 - int(volt/29.444):8], 1)
        GPIO.output(LEDS[0:8 - int(volt/29.444)], 0)
        measure.append(volt*3.3/256)
        if volt*3.3/256 >= 3.2:
            break
    while True:
        volt = adc0()
        print(dec2bin(volt), volt*3.3/256, volt)
        GPIO.output(LEDS[8 - int(volt/29.444):8], 1)
        GPIO.output(LEDS[0:8 - int(volt/29.444)], 0)
        measure.append(volt*3.3/256)
        if volt*3.3/256 <= 0.066:
            finish = time.time()
            exp_time = finish - start
            print("\n")
            print('Время эксперимента', exp_time, 'секунд')
            print('Период', exp_time/len(measure), 'секунд')
            print('Частота дискретизации', len(measure)/exp_time, 'секунд')
            print('Шаг квантования АЦП', 3.3/256)

            with open('data.txt', 'w', encoding='utf - 8') as f:
                for i in measure:
                    f.write(str(i))
                    f.write('\n')
                f.close()
            with open('settings.txt', 'w', encoding='utf - 8') as f:
                f.write(str(len(measure)/exp_time))
                f.write('\n')
                f.write(str(3.3/256))
            f.close()

            plt.plot(measure)
            plt.show()
            break
except KeyboardInterrupt:
    finish = time.time()
    print("\n")
    print((finish - start), 'секунд')
    print(measure)
finally:
    GPIO.output(troykamodule, 0)
    GPIO.output(DAC, 0)
    GPIO.output(LEDS, 0)
    GPIO.cleanup()
