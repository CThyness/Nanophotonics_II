import ft232
from pylablib.devices import Thorlabs as tl
import numpy as np
import time

# Serial numbers for the motors. y axis and z axis on top camera stage are the motorized ones.
serial_y = '26004964'
serial_z = '26004967'

stepper_y = tl.KinesisMotor(serial_y) #Ok, so this is how you get a object of the KinesisMotor class. tl.KinesisMotor("Serialnumber")
stepper_z = tl.KinesisMotor(serial_z)
info = tl.KinesisDevice.get_device_info(stepper_y)
# print(info)
print(tl.KinesisMotor.get_scale(stepper_y))
print(tl.KinesisMotor.get_scale(stepper_z))


print(tl.KinesisMotor.get_position(stepper_z))
print(tl.KinesisMotor.get_position(stepper_y))

tl.KinesisMotor.move_to(stepper_z, 0)
tl.KinesisMotor.move_to(stepper_y, 0)

# tl.KinesisMotor.move_to(stepper_z, 4382342)
# tl.KinesisMotor.move_to(stepper_y, 3303440)

# tl.KinesisMotor.move_by(stepper_z, 500000)

#Both motors are set up so positive steps is positive direction. That is nice at least.

#Position '0' gets reset upon power cycling!!!!!!!!!!!!!
#There is also some bugs in the get_position function. Specifically when moving a negative number of steps
#These issues are also there when using move_to, not only for move_by.
#There can also be issues with get_position when moving a positive amount of steps, but those are smaller (also very scary)
#Also there for both move_by and move_to

#Think I found the issue. For negative values, it seems to overshoot A LOT and then move back to account for mistakes.

#When I moved to 100,000 it now told me it was at position 28

# -3,740,701 steps equals -0.5007mm on motor controller screen (For y direction at least)
# If that is the correct length I do not know. But hey

# 23,145,729 steps equal 3.0980mm on motor controller for z direction
# Still no clue if that is the correct amount of movement... :|

# tl.KinesisDevice._move_to() #Okay, so this exists
# tl.KinesisMotor.move_to() #Hmm, so this exists as well. Don't know which is better