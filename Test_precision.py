from datetime import datetime
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
import asyncio
from aioconsole import ainput
position=[0,0,2]
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
    #sequence=np.array([[0,0,2],[1,0,2],[1,1,2],[-0.2,2,1.4],[-0.3,2,1.2]]) 
    #temps=[10,10,10,5,5,2]
    path=AppDirs("cfclient","Bitcraze").user_config_dir
    anchor_pos=np.array([[-2.45,-3.25,0.0],[0,0,0],[2.45,0,0],[2.45,-2.6,2.0],[-2.45, 0.0,2.2],[2.45,3.42, 2.0],[-2.45,2.6,0.0]])
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    with SyncCrazyflie(URI) as scf:
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
        scf.cf.commander.set_client_xmode(True)
        end_time=time.time()+60
        val=[]
        while time.time() < end_time :
            pos=pos_log.position
            val.append(pos)

            time.sleep(0.01)
    #mc.land()
    # Wait a bit

    # We land when the MotionCommander goes out of scope
    #numero = input("numero: ")
    npVal=np.array(val)
    # print(f'moyenne={npVal.mean(1)}\nmax={npVal.max(1)}\nmin={npVal.min(1)}')
    np.savetxt("./mesure/mesure_60S_10ms_4.csv",npVal, delimiter=',')
    print("done!!!!!!!!!!!!!")
exit()