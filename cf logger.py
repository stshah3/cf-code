#!/usr/bin/env python
#This is a simple program which logs data directly to a file fromm Crazyflie instruments, specifically Accelerometer, Gyroscope, Stabilizer, Barometer, and Battery Voltage .

import logging
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import Log, LogVariable, LogConfig

__author__ = "Samyak Shah"

"""
Choose file name to log to.
If more information is desired, change level to: level = logging.DEBUG
WARNING: filemode is set to 'w', file will overwrite each time this program is executed. 
"""


import logging
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s %(levelname)s %(message)s',
    filename = 'cf log file.txt',
    filemode = 'w'
    )

class Main:
    
    def __init__(self):
        """
        Connect to Crazyflie, initialize drivers and set up callback.
        The callback takes care of logging the accelerometer values.
        """
        logging.info("Connecting to Crazyflie...\n")
        self.crazyflie = Crazyflie()
        cflib.crtp.init_drivers()
        """
        You may need to update this value if your Crazyradio uses a different frequency.
        """
        self.crazyflie.open_link("radio://0/100/250K")
 
        self.crazyflie.connected.add_callback(self.connectSetupFinished)

        print("Please check 'cf log file.txt'")

    def connectSetupFinished(self, linkURI):

        """
        Configure the logger to log accelerometer values and start recording.
 
        The logging variables are added one after another to the logging
        configuration. Then the configuration is used to create a log packet
        which is cached on the Crazyflie. If the log packet is None, the
        program exits. Otherwise the logging packet receives a callback when
        it receives data, which prints the data from the logging packet's
        data dictionary as logging info.
        """

        logging.info("Connected to Crazyflie. Starting log...\n" )

        #Log Accelerometer
        self.logAccel = LogConfig("Accel", 1000)
        self.logAccel.add_variable("acc.x", "float")
        self.logAccel.add_variable("acc.y", "float")
        self.logAccel.add_variable("acc.z", "float")
        
        
        self.crazyflie.log.add_config(self.logAccel)

        if self.logAccel.valid:
            self.logAccel.data_received_cb.add_callback(self.print_accel_data)
            self.logAccel.start()
        else:
            logger.warning("Could not setup log configuration for Accelerometer after connection!")

        ###############################################################################################

        #Log Gyroscope
        self.logGyro = LogConfig("Gyro", 1000)
        self.logGyro.add_variable("gyro.x", "float")
        self.logGyro.add_variable("gyro.y", "float")
        self.logGyro.add_variable("gyro.z", "float")

        self.crazyflie.log.add_config(self.logGyro)

        if self.logGyro.valid:
            self.logGyro.data_received_cb.add_callback(self.print_gyro_data)
            self.logGyro.start()
        else:
            logger.warning("Could not setup log configuration for Gyroscope after connection!")

        ###############################################################################################

        #Log Stabilizer
        self.logStab = LogConfig("Stabilizer", 1000)
        self.logStab.add_variable("stabilizer.roll", "float")
        self.logStab.add_variable("stabilizer.pitch", "float")
        self.logStab.add_variable("stabilizer.yaw", "float")
        self.logStab.add_variable("stabilizer.thrust", "uint16_t")
 
        self.crazyflie.log.add_config(self.logStab)
 
        if self.logStab.valid:
            self.logStab.data_received_cb.add_callback(self.print_stab_data)
            self.logStab.start()
        else:
            logger.warning("Could not setup log configuration for Stabilizer after connection!")

        ###############################################################################################

        #Log Barometer
        self.logBaro = LogConfig("Baro", 1000)
        self.logBaro.add_variable("baro.aslLong", "float")

        self.crazyflie.log.add_config(self.logBaro)
        if self.logBaro.valid:
            self.logBaro.data_received_cb.add_callback(self.print_baro_data)
            self.logBaro.start()
        else:
            logger.warning("Could not setup log configuration for Barometer after connection!")

        ###############################################################################################

        #Log Battery Voltage
        self.logPm = LogConfig("Battery Voltage", 1000)
        self.logPm.add_variable("pm.vbat", "float")

        self.crazyflie.log.add_config(self.logPm)

        if self.logPm.valid:
            self.logPm.data_received_cb.add_callback(self.print_pm_data)
            self.logPm.start()
        else:
            logger.warning("Could not setup log configuration for Battery after connection!")

        ###############################################################################################
        
    def print_accel_data(self, ident, data, logconfig):
        logging.info("Id={0}, Accelerometer: x={1:.2f}, y={2:.2f}, z={3:.2f}".format(ident, data["acc.x"], data["acc.y"], data["acc.z"]))
        
    def print_gyro_data(self, ident, data, logconfig):
        logging.info("Id={0}, Gyro: x={1:.2f}, y={2:.2f}, z={3:.2f}".format(ident, data["gyro.x"], data["gyro.y"], data["gyro.z"]))
    
    def print_stab_data(self, ident, data, logconfig):
        logging.info("Id={0}, Stabilizer: Roll={1:.2f}, Pitch={2:.2f}, Yaw={3:.2f}, Thrust={4:.2f}".format(ident, data["stabilizer.roll"], data["stabilizer.pitch"], data["stabilizer.yaw"], data["stabilizer.thrust"]))

    def print_baro_data(self, ident, data, logconfig):
        logging.info("Id={0}, Barometer: asl={1:.4f}".format(ident, data["baro.aslLong"]))
 
    def print_pm_data(self, ident, data, logconfig):
        logging.info("Id={0}, Battery Voltage(V): vbat={1:.4f}\n".format(ident, data["pm.vbat"]))
    

Main()

