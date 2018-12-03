import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from time import sleep

fig, ax = plt.subplots(1,1)

plt.show(block=False)

for x in np.linspace(0,1,20):
    #print(x)
    # 0-.33 fades from R-G
    # .33-.66 from G-B
    # .66-1 from B-R
    if x>=0 and x<0.33:
        color = (3*(.33 - x), 3*x, 0)
    if x<0.66 and x>=0.33:
        color = (0, 3*(0.66 - x), 3*(x - 0.33))
    if x>=0.66 and x<1:
        color = (3*(x - 0.66), 0, 3*(1 - x))

    ax.add_patch(patches.Rectangle((0,0),5,2,facecolor=color))
    fig.canvas.draw()
    sleep(0.2)
