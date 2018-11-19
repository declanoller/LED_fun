from LED_grid import LED_grid
from LED_control import LED_control

try:
    control = LED_control(Nx=8, Ny=7, zigzag=True)
    #control.scrollNumbers()
    control.scrollLetters()
except:
    print('something failed, exiting.')
    control.clearAll()
#sim = LED_grid(Nx=15, Ny=20)
#sim.count()
























#
