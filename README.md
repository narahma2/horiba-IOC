# horiba-IOC
EPICS soft IOC implementation for the Horiba iHR320 spectrometer.

# Quick-Start
This installation requires a python environment, as well as the yaq tool which handles most of the hardware communication. An `environment.yml` file is provided for a quick conda setup:

```
$ conda env create --file=environment.yml
$ conda activate horiba
```

You'll also need to create a `config.toml` file based on the target Horiba spectrometer settings--edit the one provided as needed (most likely the grating settings). The configuration file can be easily created with:

```
(horiba) $ yaqd edit-config horiba-ihr320
```

With the Horiba spectrometer connected by USB, start the daemon:

```
(horiba) $ yaqd-horiba-ihr320
```

In another terminal window, you can query the status:

```
(horiba) $ yaqd status
```

Finally, to start up the IOC, run the python script:

```
(horiba) $ python ./scripts/start_ioc.py
```

A .ui file is provided which can be integrated into your typical EPICS setup for interactive control of the associated PVs.
