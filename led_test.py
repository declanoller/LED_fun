from LED_control import LED_control

control = LED_control(Nx=10, Ny=15, zigzag=True, run_type='real')
#control.scrollLetters()
#control.scrollNumbers()

control.horizontalScroll('meow')

exit(0)

try:
    control = LED_control(Nx=8, Ny=7, zigzag=True, run_type='simulation')
    #control.scrollNumbers()
    control.scrollLetters()
except:
    print('something failed, exiting.')
    control.clearAll()























#
