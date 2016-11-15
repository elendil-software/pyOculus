import logging
import PyIndi

#My config lib
from config import INSTR_DEV
 
class IndiClient(PyIndi.BaseClient):
    device = None

    def __init__(self, exptime=10.0, filename="frame.fits", device=INSTR_DEV):
        super(IndiClient, self).__init__()
        self.logger = logging.getLogger('PyQtIndi.IndiClient')
        self.logger.debug('creating an instance of PyQtIndi.IndiClient')
        self.exptime = exptime
        self.filename = filename
        self.device = device
    def newDevice(self, d):
        self.logger.debug("new device " + d.getDeviceName())
        if d.getDeviceName() == self.device:
            self.logger.debug("Set new device %s!" % self.device)
            # save reference to the device in member variable
            self.device = d
    def newProperty(self, p):
        if self.device is not None and p.getName() == "CONNECTION" and p.getDeviceName() == self.device.getDeviceName():
            self.logger.debug("Got property CONNECTION for %s!" % self.device)
            # connect to device
            self.connectDevice(self.device.getDeviceName())
            # set BLOB mode to BLOB_ALSO
            self.setBLOBMode(1, self.device.getDeviceName(), None)
        if p.getName() == "CCD_EXPOSURE":
            # take first exposure
            self.takeExposure()
    def removeProperty(self, p):
        #self.logger.debug("remove property "+ p.getName() + " for device "+ p.getDeviceName())
        pass
    def newBLOB(self, bp):
        self.logger.debug("new BLOB "+ bp.name.decode())
        # get image data
        img = bp.getblobdata()
        import cStringIO
        # write image data to StringIO buffer
        blobfile = cStringIO.StringIO(img)
        # open a file and save buffer to disk
        with open(self.filename, "wb") as f:
            f.write(blobfile.getvalue())
        # start new exposure for timelapse images!
        # self.takeExposure()
        # disconnect from server
        self.disconnectServer()
    def newSwitch(self, svp):
        #self.logger.info ("new Switch "+ svp.name.decode() + " for device "+ svp.device.decode())
        pass
    def newNumber(self, nvp):
        #self.logger.debug("new Number "+ nvp.name.decode() + " for device "+ nvp.device.decode())
        pass
    def newText(self, tvp):
        #self.logger.debug("new Text "+ tvp.name.decode() + " for device "+ tvp.device.decode())
        pass
    def newLight(self, lvp):
        #self.logger.debug("new Light "+ lvp.name.decode() + " for device "+ lvp.device.decode())
        pass
    def newMessage(self, d, m):
        #self.logger.debug("new Message "+ d.messageQueue(m).decode())
        pass
    def serverConnected(self):
		try:
			self.connected = True
			self.logger.debug("Server connected ("+self.getHost()+":"+str(self.getPort())+")")
		except:
			self.logger.critical("Server conection failed!")
    def serverDisconnected(self, code):
        self.logger.debug("Server disconnected (exit code = "+str(code)+","+str(self.getHost())+":"+str(self.getPort())+")")
        # set connected to False
        self.connected = False
    def takeExposure(self):
        self.logger.debug("> Exposure >>>>>>>>>")
        #get current exposure time
        exp = self.device.getNumber("CCD_EXPOSURE")
        # set exposure time to x seconds
        exp[0].value = self.exptime
        # send new exposure time to server/device
        self.sendNewNumber(exp)

