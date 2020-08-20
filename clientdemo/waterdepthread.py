# Import Required Python libraries
import RPi.GPIO as GPIO
import time
import rrdtool

# GPIO configuration
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Define a function to measure the water depth of the fish tank
# The ultrasonic sensor will be measuring from the top of the tank

def depth():

#Settle sensor first
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(2)

# Send a Pulse
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()


# Measure the time between the pulses
    while GPIO.input(GPIO_ECHO) == 0: 
        pulseStart = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        pulseEnd = time.time()

# Calculate the distance of the pulse based on the duration

    pulseDuration = pulseEnd - pulseStart
    pulseDistance = round(pulseDuration * 17150, 2) # A calculation based on the ultrasonic speed there an back again

# Our water depth will be the height of the sensor from the bottom of the tank, minus the pulse distance

    tankDepth = 770 - pulseDistance

    return tankDepth

# Loop every 15 seconds

try:
    while True:
	waterDepth = depth()
#	print waterDepth
	value="N:" + str(waterDepth)
	rrdtool.update("depth.rrd", value)
        rrdtool.graph("depthlast2hours.png", "--start", "-2h", "DEF:Depth=depth.rrd:depth:AVERAGE","LINE1:Depth#FF0000:Depth",
                 "-v","Centimetres", "-t", "Last 2 Hours")
        rrdtool.graph("depthlast24hours.png", "--start", "-24h", "DEF:Depth=depth.rrd:depth:AVERAGE","LINE1:Depth#FF0000:Depth",
                "-v","Centimetres", "-t", "Last 24 Hours")
        rrdtool.graph("depthlastweek.png", "--start", "-1w", "DEF:Depth=depth.rrd:depth:AVERAGE","LINE1:Depth#FF0000:Depth",
                 "-v","Centimetres", "-t", "Last Week")


	time.sleep(15)
except KeyboardInterrupt:
	print("Script Stopped")
	GPIO.cleanup()

