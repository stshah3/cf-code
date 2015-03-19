import time
from threading import Thread
 
import cflib.crtp
from cflib.crazyflie import Crazyflie

import logging
 


class Main:
    def __init__(self):
        self.crazyflie = Crazyflie()
        cflib.crtp.init_drivers()
        self.crazyflie.connected.add_callback(
                                                    self.connectSetupFinished)
        self.crazyflie.open_link("radio://0/1/250K")

    def connectSetupFinished(self, linkURI):
        self.output_toc()

    def output_toc(self):
        logging.info("printing the TOC")
        toc = self.crazyflie.log.toc

        for group in toc.toc.keys():
            for param in toc.toc[group].keys():
                toc_element = toc.toc[group][param]
                logging.info("name=%s.%s, index=%d, pytype=%s, ctype=%s" %
                    (group, param, toc_element.ident, toc_element.pytype, toc_element.ctype))

                print toc_element.ident
Main()

