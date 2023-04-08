from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt 

# N=100
# val=np.ndarray([3,N])


data1 = np.loadtxt("./mesure/mesure_60S_10ms_2.csv", delimiter=',')
data2 = np.loadtxt("./mesure/mesure_60S_10ms_3.csv", delimiter=',')
data3 = np.loadtxt("./mesure/mesure_60S_10ms_4.csv", delimiter=',')

N,n=data1.shape
t=np.linspace(0,.01*N,N)

fig, axs = plt.subplots(3,figsize=(18,18))
x=[t[0],t[-1]]
moy=data1[:,0].mean()
max=data1[:,0].max()
min=data1[:,0].min()
axs[0].plot(t,data1[:,0],label='position en x')
axs[0].plot(x,[moy,moy],label='moyenne x')
axs[0].plot(x,[min,min],label='minimum x')
axs[0].plot(x,[max,max],label='maximum x')
axs[0].set_title("precision en x")
axs[1].set_title("precision en y")
axs[2].set_title("precision en z")
axs[0].text(50,0.05,f"variance en x ={np.var(data1[:,0])}")
axs[0].text(50,0.1,f"ecart type en x ={np.nanstd(data1[:,0])}")

moy=data1[:,1].mean()
max=data1[:,1].max()
min=data1[:,1].min()
axs[1].plot(t,data1[:,1],label='position en y')
axs[1].plot(x,[moy,moy],label='moyenne y')
axs[1].plot(x,[min,min],label='minimum y')
axs[1].plot(x,[max,max],label='maximum y')
axs[1].text(50,-0.025,f"variance en y ={np.var(data1[:,1])}")
axs[1].text(50,-0.05,f"ecart type en y ={np.nanstd(data1[:,1])}")
moy=data1[:,2].mean()
max=data1[:,2].max()
min=data1[:,2].min()
axs[2].plot(t,data1[:,2],label='position en z')
axs[2].plot(x,[moy,moy],label='moyenne z')
axs[2].plot(x,[min,min],label='minimum z')
axs[2].plot(x,[max,max],label='maximum z')
axs[2].text(50,1.1,f"variance en z ={np.var(data1[:,2])}")
axs[2].text(50,1.15,f"ecart type en z ={np.nanstd(data1[:,2])}")
#axs[0].plot(t,data1[:,1],label='position en y')
#axs[0].plot(t,data1[:,2],label='position en z')
#axs[0].set_xlabel("temps")
#axs[0].set_ylabel("Valeur")
axs[0].grid()
axs[1].grid()
axs[2].grid()
axs[0].legend()
axs[1].legend()
axs[2].legend()
fig.tight_layout()



"""
N,n=data2.shape
t=np.linspace(0,.01*N,N)
axs[1].plot(t,data2[:,0],label='position en x')
axs[1].plot(t,data2[:,1],label='position en y')
axs[1].plot(t,data2[:,2],label='position en z')
axs[1].set_xlabel("temps")
axs[1].set_ylabel("Valeur")

N,n=data3.shape
t=np.linspace(0,.01*N,N)
t=np.linspace(0,60,N)
axs[2].plot(t,data3[:,0],label='position en x')
axs[2].plot(t,data3[:,1],label='position en y')
axs[2].plot(t,data3[:,2],label='position en z')
axs[2].set_xlabel("temps")
axs[2].set_ylabel("Valeur")
axs[0].legend()
axs[0].grid()
axs[1].legend()
axs[1].grid()
axs[2].legend()
axs[2].grid()"""

plt.show()