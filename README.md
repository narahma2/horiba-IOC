# horiba-IOC
EPICS soft IOC implementation for the Horiba iHR320 spectrometer.

# Quick-Start
This installation requires a python environment, as well as the [yaq](https://yaq.fyi/) tool which handles most of the hardware communication. An `environment.yml` file is provided for a quick conda setup:

```shell
conda env create --file=environment.yml
conda activate horiba
```

You'll also need to create a `config.toml` file based on the target Horiba spectrometer settings--adjust the provided values as needed (most likely the grating settings) and copy into the proper file location. The configuration file can be easily created with:

```shell
yaqd edit-config horiba-ihr320
```

With the Horiba spectrometer connected by USB, start the daemon:

```shell
yaqd-horiba-ihr320
```

In another terminal window, you can query the status:

```shell
yaqd status
```

Finally, to start up the IOC, run the python script:

```shell
python ./scripts/start_ioc.py
```

A .ui file is provided which can be integrated into your typical EPICS setup for interactive control of the associated PVs.

# PV List
The PVs served by this IOC follow a `HORIBA-IHR320:*`/`HORIBA-IHR320:*-RBV` template, where `HORIBA-IHR320:*` is the PV you can update with `caput` and `HORIBA-IHR320:*-RBV` is the current device setting that you can readback with `caget`.

A list of the relevant PVs is below (edit `start_ioc.py` to change the names as desired):

- `HORIBA-IHR320:POSITION` / `HORIBA-IHR320:POSITION-RBV`: Central wavelength position (nm)
- `HORIBA-IHR320:SLIT-WIDTH` / `HORIBA-IHR320:SLIT-WIDTH-RBV`: Entrance horizontal slit width (mm)
- `HORIBA-IHR320:EXIT-MIRROR` / `HORIBA-IHR320:EXIT-MIRROR-RBV`: Exit mirror position (front or side)
- `HORIBA-IHR320:TURRET` / `HORIBA-IHR320:TURRET-RBV`: Turret position (names set in `config.toml`)
