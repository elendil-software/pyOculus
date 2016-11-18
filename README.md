# pyOculus
Python set up for Oculus allsky camera on Raspberry Pi. The code is currently running on an Starlight Xpress Oculus installed in the [Observatorio Astronómico de Javalambre](http://oajweb.cefca.es), in Teruel (Spain).
This project is a fork of [https://github.com/zemogle/pyOculus](https://github.com/zemogle/pyOculus) Many thanks! [Dark Matter Sheep](http://darkmattersheep.uk/blog/).

## Setup (Pending changes)
- A Raspberry Pi
- Need to install [INDI server](http://indilib.org/download/category/6-raspberry-pi.html) for Raspberry Pi.
- Install Swig via `sudo apt-get install swig` you may need to do `sudo apt-get install -f` to get the dependencies
- You may need to install `cmake` with `sudo apt-get install cmake` before the next step
- You may also need to install python dev using `sudo apt-get install python-dev`
- Install the [PyINDI client](https://github.com/zemogle/pyindi-client) by doing
```bash
git clone https://github.com/zemogle/pyindi-client
mkdir libindipython
cd libindipython
```

You will probably also need to replace the file `cmake_modules/findINDI.cmake` with the one from [this INDI issue](https://sourceforge.net/p/pyindi-client/tickets/2/).

```bash
cmake -D PYTHON_LIBRARY=/usr/lib/arm-linux-gnueabihf/libpython2.7.so -D PYTHON_INCLUDE_DIR=/usr/include/python2.7/ ../pyindi-client/swig-indi/swig-indi-python
make
sudo make install
```

You should already have `python` and `git` if you are using Raspbian.

## Instructions (UPDATED! 2016/11/18)

The INDI server handles all the communication with the camera, so the server has to be running for this code to be able to talk to the camera. In our case Oculus uses a Starlight Xpress CCD, so we MUST started the INDI&camera with:

`shellscript/indi.service start`

It would be good idea run as a service. Then copy the script to /etc/init.d/ and execute `sudo rcconf` to enable (needs: rcconf package)

To test, you can take an image with `exposure.py`. It takes an image of 10 sec will named "test_exposure.fits"
You can use args:  `exposure.py texp filename`

## Taking loop images (UPDATED! 2016/11/18)

You must configure with your location in config.yaml file (name, latitude, longitude, elevation).
Other crucial parameters is data destination and logfile.

When executing `main.py`, the program check previously camera is plugged, INDI is running, data location is accesible, space on disk and memory available (latest two parameters configurable in config.yaml)
Then, if it is daylight yet, wait to observe. In "Instrument parameters" you can configure exposures time or offset before/after sunset you want begin. When it will arrive time to start, Loop begins taking images with a short time exposure (configurable in config.yaml). While time go on and pass astronomical twilight, the exposure will be increment to exp_max parameter. Near sunrise, the time exposure will decresasing until the process stop adquiring and close.

If you run this program on a RasberryPi with SenseHat module, you can show the status progress on led screen.

You can use `shellscripts/pyOculus.sh` start/stop the program

`shellscripts/pyOculus [start|stop|viewlog]`

The viewlog option show a console with lastest lines of logfile continuosly.


## Testing Setup (Pending changes)

If you are in doubt of whether the camera is connected and working, you can run the following test script (assuming the INDi server is running):

`python pyindi-client/swig-indi/swig-indi-python/test-indiclient.py`
