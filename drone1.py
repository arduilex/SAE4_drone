"""
This script shows a simple scripted flight path using the MotionCommander class.

Simple example that connects to the crazyflie at `URI` and runs a
sequence. Change the URI variable to your Crazyflie configuration.
"""
import logging
import time

import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

URI = 'radio://0/80/2M'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(URI) as scf:
        # We take off when the commander is created
        with MotionCommander(scf) as mc:
            print('Taking off!')
            time.sleep(1)          


            # There is a set of functions that move a specific distance
            # We can move in all directions
            print('Moving up 0.2m')
            #mc.take_off(3,0.2)
            # Wait a bit
            #mc._is_flying=False
            mc.up(5,velocity=1)
            time.sleep(1)
            print("!!!!")
            mc.start_linear_motion(0, 0.00, 0.2)
            
            time.sleep(7)
            mc.stop()

            print('Moving down 0.2m')
            mc.down(1.2,velocity=0.5)
            # Wait a bit
            time.sleep(1)


            # We land when the MotionCommander goes out of scope
            print('Landing!')
