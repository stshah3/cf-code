import time
from threading import Thread
 
import cflib.crtp
from cflib.crazyflie import Crazyflie

class Main:
 
    # Initial values, you can use these to set trim etc.
    roll = 0.0
    pitch = 0.0
    yawrate = 0
    thrust = 10001
 
    def __init__(self):
        self.crazyflie = Crazyflie()
        cflib.crtp.init_drivers()
 
        # You may need to update this value if your Crazyradio uses a different frequency. This value can be found from Crazyflie PC client.
        self.crazyflie.open_link("radio://0/100/250K")
 
        self.crazyflie.connected.add_callback(self.connectSetupFinished)
 
    def connectSetupFinished(self, linkURI):
        # Keep the commands alive so the firmware kill-switch doesn't kick in.
        Thread(target=self.pulse_command).start()
 
        while 1:
            self.thrust = int(raw_input("Set thrust (10001-60000):"))
 
            if self.thrust == 0:
                self.crazyflie.close_link()
                break
            elif self.thrust <= 10000:
                self.thrust = 10001
            elif self.thrust > 60000:
                self.thrust = 60000
 
    def pulse_command(self):
        self.crazyflie.commander.send_setpoint(self.roll, self.pitch, self.yawrate, self.thrust)
        time.sleep(0.1)
 
        # ..and go again!
        self.pulse_command()
 
Main()