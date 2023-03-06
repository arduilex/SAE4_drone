import logging
import time
from cfclient.ui.pose_logger import PoseLogger
import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie import Crazyflie
from lpslib.lopoanchor import LoPoAnchor
from cfclient.ui.tabs.locopositioning_tab import LocoPositioningTab
import numpy as np
from cflib.positioning.position_hl_commander import PositionHlCommander
from appdirs import AppDirs
URI = 'radio://0/80/2M'
def write_positions_to_anchors(cf, anchor_positions):
        lopo = LoPoAnchor(cf)

        for _ in range(3):
            for id, position in enumerate(anchor_positions):
                lopo.set_position(id, position)
            time.sleep(0.2)
# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)
from lpslib.lopoanchor import LoPoAnchor

if __name__ == '__main__':
    path=AppDirs("cfclient","Bitcraze").user_config_dir
    anchor_pos=np.array([[-2.45,-3.25,0.0],[0,0,0],[2.45,0,0],[2.45,-2.6,2.0],[-2.45, 0.0,2.2],[2.45,3.42, 2.0],[-2.45,2.6,1.0]])
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    with SyncCrazyflie(URI) as scf:
        # We take off when the commander is created
        with MotionCommander(scf) as mc:
            anchor=LoPoAnchor(scf.cf)
            for i in range(7):
                 if i==1:
                      pass
                 anchor.set_mode(i,1)
                 anchor.set_position(i,anchor_pos[i])
            ## configuration de la class poselogger qui s'occupe d'obtenir les informations  
            pos_log=PoseLogger(scf.cf)
            pos_log._connected(URI)
            time.sleep(1)

            cible=(0,0,2)
            #mc.start_linear_motion(0, 0.00, 0.2)
            for i in range(100):
                
                print(pos_log.position)
                #mc.start_linear_motion((cible[0]-pos_log.position[0]),(cible[1]-pos_log.position[1]),(cible[2]-pos_log.position[2]+0.2),0)
                #print("reste",cible-pos_log.position)
                scf.cf.commander.send_position_setpoint(0,0,2,0)
                time.sleep(0.1)
                mc.stop()
            mc.stop()
            # Wait a bit
            time.sleep(1)
            

            # We land when the MotionCommander goes out of scope
            print('Landing!')
