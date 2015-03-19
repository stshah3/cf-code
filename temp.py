import cflib.crtp
from cfclient.utils.logconfigreader import LogConfig
from cfclient.utils.logconfigreader import LogVariable
from cflib.crazyflie import Crazyflie

class Main:
    def __init__(self):
        self.crazyflie = Crazyflie()
        cflib.crtp.init_drivers()

        self.crazyflie.connectSetupFinished.add_callback(
                                                    self.connectSetupFinished)

        self.crazyflie.open_link("radio://0/10/250K")

    def connectSetupFinished(self, linkURI):
      # Set accelerometer logging config
        accel_log_conf = LogConfig("Accel", 10)
        accel_log_conf.addVariable(LogVariable("acc.x", "float"))
        accel_log_conf.addVariable(LogVariable("acc.y", "float"))
        accel_log_conf.addVariable(LogVariable("acc.z", "float"))

        # Now that the connection is established, start logging
        self.accel_log = self.crazyflie.log.create_log_packet(accel_log_conf)

        if self.accel_log is not None:
            self.accel_log.dataReceived.addCallback(log_accel_data)
            self.accel_log.start()
        else:
            print("acc.x/y/z not found in log TOC")

    def log_accel_data(self, data):
        logging.info("Accelerometer: x=%.2f, y=%.2f, z=%.2f" %
                     (data["acc.x"], data["acc.y"], data["acc.z"]))

Main()