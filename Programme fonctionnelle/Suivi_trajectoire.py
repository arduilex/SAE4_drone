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
from os import system
consigne=[]
precision=.1
Valcourant=[]
position=[[0,0,2]]
appro=[0,0,1.5]
depo=[0,0,1]
pos=(0,0,0)
marche=False
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
            await asyncio.sleep(2)
            position.append(np.array(pos_log.position).tolist()) #transformation du tuple recu en vecteur puis en list
            while(1):
                x=position[0][0]
                y=position[0][1]
                z=position[0][2]                    
                pos=pos_log.position
                mc._cf.commander.send_position_setpoint(x,y,z,0)
                await asyncio.sleep(0.01)
async def fcommande():
     global position
     global mc
     global marche
     while (1):
        id=await ainput("id")
        await asyncio.sleep(.1)

        x=await ainput(">>> x=")
        y=await ainput(">>> y=")
        z=await ainput(">>> z=")
        position.append([x,y,z])
        await asyncio.sleep(.1)
        system("clear")
        print(f">>> id={id}\n>>> sequence={np.array(position)}")
        break
        
async def verification():
    global Valcourant
    global consigne
    global position
    await asyncio.sleep(5)
    while 1:
        x,y,z=pos
        X=position[0][0]
        Y=position[0][1]
        Z=position[0][2]  
        dis=np.sqrt((x-X)*2+(y-Y)**2+(z-Z)**2)
        if dis<precision and len(position)>2:
            position.pop(0)
        await asyncio.sleep(.01)


"""        print(position)
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
    """
async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(controle(), fcommande(),verification())
asyncio.run(main())
""""
if __name__ == '__main__':
    #sequence=np.array([[0,0,2],[1,0,2],[1,1,2],[-0.2,2,1.4],[-0.3,2,1.2]]) 
    #temps=[10,10,10,5,5,2]
    path=AppDirs("cfclient","Bitcraze").user_config_dir
    anchor_pos=np.array([[-2.45,-3.25,0.0],[0,0,0],[2.45,0,0],[2.45,-2.6,2.0],[-2.45, 0.0,2.2],[2.45,3.42, 2.0],[-2.45,2.6,0.0]])
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    with SyncCrazyflie(URI) as scf:
        # We take off whent=np.linspace(0,60,N) the commander is created
        with MotionCommander(scf) as mc:
            # mc.stop()

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
            #mc._cf.link='radio://0/20/2M'
            #mc._cf._link_uri='radio://0/20/2M'
            cible=(0,0,2)
            #mc.start_linear_motion(0, 0.00, 0.2)
            v=1
            
            N=500
            val=[]
            i=0.1
            n=0
            for position in sequence:
                x=position[0]
                y=position[1]
                z=position[2]
                print(f"_____________________________________going to {[x,y,z]}\n")
                ix=0
                iy=0     
                iz=0
                pos=pos_log.position    
                dx=x-pos[0]                
                dy=y-pos[1]
                dz=z-pos[2]
                dy1=dy                    
                dx1=dx
                dz1=dz
                mc._cf.commander.set_client_xmode(Truerue)
                #mc.up(1,1)0,,1.5]
                end_time = time.time()+temps[n]
                chrono = time.time()
                print(f'going to {position}')
                while time.time() < end_time :
                
                    
                    pos=pos_log.position
                    angle=pos_log.rpy[0]
                    if time.time() - chrono > 0.1:
                         print(np.array(pos_log.position).round(2))
                         val.append(pos)
                         chrono = time.time()

                    dx=x-pos[0]
                    dy=y-pos[1]
                    dz=z-pos[2]
                    vx=dx-dx1
                    vy=dy-dy1            #npVal=np.array(val)
            # print(f'moyenne={npVal.mean(1)}\nmax={npVal.max(1)}\nmin={npVal.min(1)}')
            #np.savetxt("./mesure/mesure_"+numero+".csv",npVal, delimiter=',')
                    vz=dz-dz1
                    d=np.sqrt(dx**2+dy**2+dz**2)
                    #mc.stop()
                    mc._cf.commander.send_position_setpoint(x,y,z,0)
                    #mc._cf.commander.send_setpprint(np.array(pos_log.position).round(2))oint(0,0,0,30000)

                    #mc.stop()
                    ix=ix+dx
                    iy=iy+dy
                    iz=iz+dz
                    dy1=dy
                    dx1=dx
                    dz1=dz
                    #time.sleep(0.005)
                n=n+1
            mc.stop()
            #mc.land()
            # Wait a bit

            # We land when the MotionCommander goes out of scope
            #numero = input("numero: ")
            #npVal=np.array(val)
            # print(f'moyenne={npVal.mean(1)}\nmax={npVal.max(1)}\nmin={npVal.min(1)}')
            #np.savetxt("./mesure/mesure_"+numero+".csv",npVal, delimiter=',')
        exit()"""
    