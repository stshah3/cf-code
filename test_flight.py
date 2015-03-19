#!/usr/bin/python
import time
import argparse
import logging
from threading import Thread

import cflib
from cflib.crazyflie import Crazyflie
from cfclient.utils.logconfigreader import LogConfig
from cfclient.utils.logconfigreader import LogVariable

from threading import Thread, Event

# Set up command line argument parsing
parser = argparse.ArgumentParser(
    description='Execute a variety of test flights with the Bitcraze Crazyflie.')
parser.add_argument('thrust_profile', metavar='thrust_profile', type=str,
    help='Thrust profile to use for the test flight. Available options are: increasing_step, hover, prbs_hover, prbs_asc, prbs_desc.')
args = parser.parse_args()

# Make sure the requested thrust profile is valid
if args.thrust_profile not in ['increasing_step', 'hover', 'prbs_hover', 'prbs_asc', 'prbs_desc']:
    print 'Requested thrust profile not found. Check your spelling, fool!\nTry test_flight.py -h for a list of available thrust profiles.'
    raise SystemExit

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class TestFlight:
    def __init__(self):
        """
        Initialize the quadcopter
        """
        self.crazyflie = cflib.crazyflie.Crazyflie()
        logging.info("Initializing drivers")
        cflib.crtp.init_drivers()
 
        logging.info("Searching for available devices")
        available = cflib.crtp.scan_interfaces()

        radio = False
        for i in available:
            # Connect to the first device of the type 'radio'
            if 'radio' in i[0]:
                radio = True
                dev = i[0]
                logging.info("Connecting to interface with URI [{0}] and name {1}".format(i[0], i[1]))
                self.crazyflie.open_link(dev)
                break

        if not radio:
            logging.info("No quadcopter detected. Try to connect again.")
            exit(-1)

        # Set up the callback when connected
        self.crazyflie.connectSetupFinished.add_callback(self.connectSetupFinished)


    def connectSetupFinished(self, linkURI):
        """
        Set the loggers
        """
        # Log stabilizer
        self.logStab = LogConfig("Stabalizer", 200)
        self.logStab.add_variable("stabilizer.roll", "float")
        self.logStab.add_variable("stabilizer.pitch", "float")
        self.logStab.add_variable("stabilizer.yaw", "float")
        self.logStab.add_variable("stabilizer.thrust", "uint16_t")
 
        self.crazyflie.log.add_config(self.logStab)
 
        if self.logStab.valid:
            self.logStab.data_received_cb.add_callback(self.print_stab_data)
            self.logStab.start()
        else:
            logger.warning("Could not setup log configuration for stabilizer after connection!")

        # Log barometer
        self.logBaro = LogConfig("Baro", 200)
        self.logBaro.add_variable("baro.aslLong", "float")

        self.crazyflie.log.add_config(self.logBaro)
        if self.logBaro.valid:
            self.logBaro.data_received_cb.add_callback(self.print_baro_data)
            self.logBaro.start()
        else:
            logger.warning("Could not setup log configuration for barometer after connection!")

        # Log Accelerometer
        self.logAccel = LogConfig("Accel",200)
        self.logAccel.add_variable("acc.x", "float")
        self.logAccel.add_variable("acc.y", "float")
        self.logAccel.add_variable("acc.z", "float")

        self.crazyflie.log.add_config(self.logAccel)

        if self.logAccel.valid:
            self.logAccel.data_received_cb.add_callback(self.print_accel_data)
            self.logAccel.start()
        else:
            logger.warning("Could not setup log configuration for accelerometer after connection!")

        # Call the requested thrust profile. 
        # Start a separate thread to run test.
        # Do not hijack the calling thread!
        if args.thrust_profile == 'increasing_step':
            Thread(target=self.increasing_step).start()
        if args.thrust_profile == 'prbs_hover':
            Thread(target=self.prbs_hover).start()
        if args.thrust_profile == 'prbs_asc':
            Thread(target=self.prbs_asc).start()
        if args.thrust_profile == 'prbs_desc':
            Thread(target=self.prbs_desc).start()


    def print_baro_data(self, ident, data, logconfig):
        logging.info("Id={0}, Barometer: asl={1:.4f}".format(ident, data["baro.aslLong"]))
 
    def print_stab_data(self, ident, data, logconfig):
        logging.info("Id={0}, Stabilizer: Roll={1:.2f}, Pitch={2:.2f}, Yaw={3:.2f}, Thrust={4:.2f}".format(ident, data["stabilizer.roll"], data["stabilizer.pitch"], data["stabilizer.yaw"], data["stabilizer.thrust"]))

    def print_accel_data(self, ident, data, logconfig):
        logging.info("Id={0}, Accelerometer: x={1:.2f}, y={2:.2f}, z={3:.2f}".format(ident, data["acc.x"], data["acc.y"], data["acc.z"]))


    # Thrust Profiles
    def increasing_step(self):
        thrust          = 30000
        pitch               = 0
        roll                = 0
        yaw_rate            = 0

        self.crazyflie.commander.send_setpoint(roll, pitch, yaw_rate, thrust)

        self.crazyflie.commander.send_setpoint(0,0,0,0)
        
        # Make sure that the last packet leaves before the link is closed since the message queue is not flushed before closing
        time.sleep(0.1)
        self.crazyflie.close_link()

    def prbs_hover(self):
        pass

    def prbs_asc(self):
        pass

    def prbs_desc(self):
        pass


TestFlight()
