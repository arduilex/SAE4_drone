from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt 

# N=100
# val=np.ndarray([3,N])


data1 = np.loadtxt("./mesure/mesure_60S_10ms.csv", delimiter=',')
data2 = np.loadtxt("./mesure/mesure_60S_10ms_2.csv", delimiter=',')
data3 = np.loadtxt("./mesure/mesure_60S_10ms_4.csv", delimiter=',')

N,n=data1.shape
t=np.linspace(0,60,N)

fig, axs = plt.subplots(3)

axs[0].plot(t,data1[:,0])
axs[0].plot(t,data1[:,1])
axs[0].plot(t,data1[:,2])

N,n=data2.shape
t=np.linspace(0,60,N)
axs[1].plot(t,data2[:,0])
axs[1].plot(t,data2[:,1])
axs[1].plot(t,data2[:,2])

N,n=data3.shape
t=np.linspace(0,60,N)
axs[2].plot(t,data3[:,0])
axs[2].plot(t,data3[:,1])
axs[2].plot(t,data3[:,2])

axs[0].legend(["x","y","z"])
axs[0].grid()
axs[1].legend(["x","y","z"])
axs[1].grid()
axs[2].legend(["x","y","z"])
axs[2].grid()
plt.show()