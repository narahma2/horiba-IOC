# horiba-IOC
EPICS soft IOC implementation for the Horiba iHR320 spectrometer.

![image](https://github.com/user-attachments/assets/6f996cee-d74d-4c4b-9e69-81a4fb5ad734)


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
    - Valid values: `0 <-> 1000`
- `HORIBA-IHR320:SLIT-WIDTH` / `HORIBA-IHR320:SLIT-WIDTH-RBV`: Entrance horizontal slit width (mm)
    - Valid values: `0 <-> 7`
- `HORIBA-IHR320:EXIT-MIRROR` / `HORIBA-IHR320:EXIT-MIRROR-RBV`: Exit mirror position (front or side)
    - Valid values: `front`, `side`
- `HORIBA-IHR320:TURRET` / `HORIBA-IHR320:TURRET-RBV`: Turret position (names set in `config.toml`)
    - Valid values: `mirror`, `gr300`, `gr600`

# Drivers
The yaq software uses the libusb library for communicating with the Horiba device instead of the vendor drivers. For Windows installations, the vendor driver can be overridden with WinUSB using the tool found here: https://zadig.akeo.ie/ (can be removed in case you want to go back to the vendor defaults).

# Daemon
The installation procedure described above assumes you're okay with keeping two terminal sessions open to keep the daemon and python IOC server running. They can alternatively be ran in the background, just like any other system daemon: https://yaq.fyi/blog/installing-yaq/#run-your-daemon-in-the-background

# Future improvements
This setup was meant to be a quick way to get EPICS working with the Horiba spectrometer. Although beyond the original scope of the project, some potential improvements include:

- Driver support through USB commands instead of relying on yaq (one less thing to install)
- Integration with [areaDetector](https://areadetector.github.io/areaDetector/) for a UI with live wavelength readout on the captured images
- Incorporating an autocalibration routine into the wavelength positions (currently the central position is estimated based on the selected grating)

# Credits
- softioc: https://github.com/DiamondLightSource/pythonSoftIOC
- yaq: https://github.com/yaq-project
