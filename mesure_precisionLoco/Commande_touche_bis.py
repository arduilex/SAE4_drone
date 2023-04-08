""" ce programme se charge de controler le drone avec des entrées clavier
"u" pour up
"l" pour left
"r" pour right
"f" pour forward
"b" pour backward
"L" pour land
les programmes sont géré en asynchrone le fcommande modifie les position en fonction des entrées clavier et le controle envoie le drones à ces position
Une troisieme fonction sauvegarde se charge de sauvegarder les informations du trajet (consigne et valeur de capteur)"""

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
consigne=[]
Valcourant=[]
position=[0,0,2]
appro=[0,0,1.5]
depo=[0,0,1]
pos=(0,0,0)
marche=True
global mc
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



async def controle():
    global URI
    global pos
    global mc
    global position
    path=AppDirs("cfclient","Bitcraze").user_config_dir
    anchor_pos=np.array([[-2.45,-3.25,0.0],[0,0,0],[2.45,0,0],[2.45,-2.6,2.0],[-2.45, 0.0,2.2],[2.45,3.42, 2.0],[-2.45,2.6,0.0]])
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
            await asyncio.sleep(1)
            position=np.array(pos_log.position)
            position[2]+=1
            mc._cf.commander.set_client_xmode(True)
            while(1):
                x=position[0]
                y=position[1]
                z=position[2]                    
                pos=pos_log.position
                mc._cf.commander.send_position_setpoint(x,y,z,0)
                mc._cf.commander.send_position_setpoint(x,y+1,z,0)
                await asyncio.sleep(0.01)
async def fcommande():
     global position
     global mc
     global marche
     while (1):
        commande =await ainput(">>> ")
        await asyncio.sleep(.1)
        if commande=='u':
            position[2]+=.5
        elif commande=='d':
            #if pos_log.position[2]>.1:
            position[2]-=.1
        elif commande=='f':
            position[0]+=.5
        elif commande=='b':
            position[0]-=.5
        elif commande=='l':
            position[1]+=.5
        elif commande=='r':
            position[1]-=.5
        elif commande=='t':
            #if pos_log.position[2]<1:
            position[2]+=1
        elif commande=='L':
            if position[2]>1.5:
                position[0]=appro[0]
                position[1]=appro[1]
                await asyncio.sleep(5)
            position=appro
            await asyncio.sleep(5)
            position=depo
            await asyncio.sleep(2)
            mc.stop()
            marche=False


        print(position)
async def sauvegarde():
    global Valcourant
    global consigne
    global position
    while marche:
        Valcourant.append(pos) 
        consigne.append(position)
        await asyncio.sleep(.01)
    npVal=np.array(consigne)
    np.savetxt("./mesure/consigne.csv",npVal, delimiter=',')
    npVal=np.array(Valcourant)
    np.savetxt("./mesure/val.csv",npVal, delimiter=',')
    print('all done!!!!')    
async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(controle(), fcommande(),sauvegarde())
asyncio.run(main())
