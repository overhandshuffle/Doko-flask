import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0.2,10,100)
fig,ax = plt.subplots()
ax.plot(x,1/x)
ax.plot(x,np.log(x))

ax.grid(True)
ax.axhline(y=0, color='b')
ax.axvline(x=0, color='k')
plt.show()