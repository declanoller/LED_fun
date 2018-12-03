from LED_control import LED_control


try:
    #control = LED_control(Nx=8, Ny=7, zigzag=True, run_type='simulation')
    control = LED_control(Nx=8, Ny=7, zigzag=True, run_type='simulation')

    control.horizontalScroll('saboner and deshlong  ', color_cycle=True)
    #control.horizontalScroll('abcdefghijklmnopqrstuvwxyz')
except:
    print('something failed, exiting.')
    control.clearAll()























#
