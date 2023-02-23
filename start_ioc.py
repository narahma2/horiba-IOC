import asyncio
import numpy as np
import yaqc

from softioc import softioc, builder, asyncio_dispatcher


# Make sure the yaqd-horiba-ihr320 daemon is running!
# Command to run within the conda environment that has yaqd-horiba:
# $ yaqd-horiba-ihr320

# Connect to Horiba daemon
c = yaqc.Client(39876)

# Set initial values
init_position = 0
init_slit = 7
init_mirror = 'front'
init_turret = 'low'

# Create an asyncio dispatcher, the event loop is now running
dispatcher = asyncio_dispatcher.AsyncioDispatcher()

# Record prefix
builder.SetDeviceName('HORIBA-IHR320')

# Create some records
rec_pos = builder.aOut(
                       'POSITION',
                       initial_value=init_position,
                       on_update=lambda v: c.set_position(v)
                       )
rec_slit = builder.aOut(
                        'SLIT-WIDTH',
                        initial_value=init_slit,
                        on_update=lambda v: c.set_front_entrance_slit(v)
                        )
rec_mirror = builder.aOut(
                          'EXIT-MIRROR',
                          initial_value=init_mirror,
                          on_update=lambda v: c.set_exit_mirror(v)
                          )
rec_turret = builder.aOut(
                          'TURRET',
                          initial_value=init_turret,
                          on_update=lambda v: c.set_turret(v)
                          )

# Boiletplate get the IOC started
builder.LoadDatabase()
softioc.iocInit(dispatcher)

# Finally leave the IOC running with an interactive shell
softioc.interactive_ioc(globals())
