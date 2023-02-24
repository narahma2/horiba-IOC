import asyncio
import numpy as np
import os
import time
import yaqc

from softioc import alarm, asyncio_dispatcher, builder, softioc


# Set environment
os.environ['EPICS_CA_SERVER_PORT'] = '5100'
os.environ['EPICS_CA_REPEATER_PORT'] = '5101'
os.environ['EPICS_CA_ADDR_LIST'] = 'localhost:5100'
#os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'NO'

# Make sure the yaqd-horiba-ihr320 daemon is running!
# Command to run within the conda environment that has yaqd-horiba:
# $ yaqd-horiba-ihr320

# Connect to Horiba daemon
c = yaqc.Client(39876)

# Initial values
init_position = c.get_position()
init_slit = c.get_front_entrance_slit()
init_mirror = 'front'
init_turret = 'low'

# Initialize spectrometer
# Waiting for tasks to finish before continuing
c.set_position(init_position)
c.set_front_entrance_slit(init_slit)
c.set_exit_mirror(init_mirror)
c.set_turret(init_turret)

# Fetch an alarm status
alarm = alarm.STATE_ALARM
alarm_green = 0
alarm_red = 2

# Create an asyncio dispatcher, the event loop is now running
dispatcher = asyncio_dispatcher.AsyncioDispatcher()

# Record prefix
builder.SetDeviceName('HORIBA-IHR320')

# Set blocking
builder.SetBlocking(True)

# Create some records
# Spectrometer status check
rbv_status = builder.boolIn('STATUS', initial_value=False)
rbv_status_label = builder.stringIn(
                                    'STATUS-LABEL',
                                    initial_value='Spectrometer ready!',
                                    status=alarm,
                                    severity=alarm_green
                                    )

# Wavelength position
rbv_pos = builder.aIn('POSITION-RBV', initial_value=c.get_position())
rec_pos = builder.aOut(
                       'POSITION',
                       initial_value=init_position,
                       on_update=lambda v: c.set_position(v),
                       DRVL=0,
                       DRVH=1200,
                       )

# Entrance slit
rbv_slit = builder.aIn(
                       'SLIT-WIDTH-RBV',
                       initial_value=c.get_front_entrance_slit()
                       )
rec_slit = builder.aOut(
                        'SLIT-WIDTH',
                        initial_value=init_slit,
                        on_update=lambda v: c.set_front_entrance_slit(v)
                        )

# Exit mirror
rbv_mirror = builder.stringIn(
                              'EXIT-MIRROR-RBV',
                              initial_value=c.get_exit_mirror()
                              )
rec_mirror = builder.stringOut(
                               'EXIT-MIRROR',
                               initial_value=init_mirror,
                               on_update=lambda v: c.set_exit_mirror(v)
                               )

# Turret setting
rbv_turret = builder.stringIn(
                              'TURRET-RBV',
                              initial_value=c.get_turret()
                              )
rec_turret = builder.stringOut(
                               'TURRET',
                               initial_value=init_turret,
                               on_update=lambda v: c.set_turret(v)
                               )

# Boilerplate get the IOC started
builder.LoadDatabase()
softioc.iocInit(dispatcher)

# Status update
async def update_status():
    while True:
        rbv_status.set(c.busy())
        if c.busy():
            rbv_status_label.set('Spectrometer busy...', severity=alarm_red)
        else:
            rbv_status_label.set('Spectrometer ready!', severity=alarm_green)

        rbv_pos.set(c.get_position())
        rbv_slit.set(c.get_front_entrance_slit())
        rbv_mirror.set(c.get_exit_mirror())
        rbv_turret.set(c.get_turret())
        await asyncio.sleep(0.5)


dispatcher(update_status)

# Finally leave the IOC running with an interactive shell
softioc.interactive_ioc(globals())
