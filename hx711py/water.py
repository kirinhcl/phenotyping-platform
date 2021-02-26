#! /usr/bin/python2

import time
import sys
import RPi.GPIO as GPIO

EMULATE_HX711=False
GPIO.setwarnings(False)

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)

jdq=17
GPIO.setup(jdq,GPIO.OUT)
# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(92)
hx.set_reference_unit(250)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")

# to use both channels, you'll need to tare them both
#hx.tare_A()
#hx.tare_B()

while True:
    try:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.
        
        # np_arr8_string = hx.get_np_arr8_string()
        # binary_string = hx.get_binary_string()
        # print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        #val = hx.get_weight(5)
        val = max(0, int(hx.get_weight(5)))
        
        if val < 1000:                      #当无盆栽时不进行浇水
            GPIO.output(17,GPIO.LOW) 
            print('nothing')
            time.sleep(1)   
        elif val < 4680:                    #当重量小于4680g浇水至4720g，并在文本中记录浇水结束时的重量，休眠5分钟
            x = int(hx.get_weight(5))
            if x < 4720:
                GPIO.output(17,GPIO.HIGH)
                print('watering___Time:{}___weight={}g'.format(time.ctime(),x))
                time.sleep(1)
            else :
                GPIO.output(17,GPIO.LOW)
                print('watering_finished___Time:{}___weight={}g'.format(time.ctime(),x))
                f=open('/home/pi/Desktop/rizhi-1.txt','a+')
                f.write('\nwatering_finished___Time:{}________weight={}g'.format(time.ctime(),x))
                f.close()
                time.sleep(300)
        else :                              #当重量大于4680g时，每5分钟记录一次重量
            GPIO.output(17,GPIO.LOW)
            print('Time:{}________weight={}g'.format(time.ctime(),val))
            f=open('/home/pi/Desktop/rizhi-1.txt','a+')
            f.write('\nTime:{}________weight={}g'.format(time.ctime(),val))
            f.close()
            time.sleep(300)

        # To get weight from both channels (if you have load cells hooked up 
        # to both channel A and B), do something like this
        #val_A = hx.get_weight_A(5)
        #val_B = hx.get_weight_B(5)
        #print "A: %s  B: %s" % ( val_A, val_B )

        hx.power_down()
        hx.power_up()
        

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
