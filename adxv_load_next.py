"""
Subscribes to a redis pub/sub server which feeds the app with the most
recent master and data files to be collected. Third field is oscillation/frame
for calculating the equivalent # of frames for 1 degree of data.
"""



#!/usr/bin/env python3.5
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(fmt=('[%(levelname)s] %(name)s ''%(funcName)s | %(message)s'),
                      datefmt='%Y-%m-%dT%H:%M:%S'))
logger.handlers = [handler]
logger.setLevel('INFO') # or INFO, or DEBUG, etc

logger = logging.getLogger(__name__)

# logger.debug("The list has i elements")
# logger.info("Established ssh connection")
# logger.warning("Max number of iterations reached")
# logger.error("Couldn't copy file. Permission denied")
# logger.critical("Configuration file damaged")



from adxv_socket import adxvsocket
from beamline import redis
from time import sleep
import json
import yaml
import os

# Load config file
with open("./adxv.yaml",'r') as yamlfile:
    cfg = yaml.safe_load(yamlfile)
    logger.debug('Config file: %s' % (cfg))

# Setup redis subscription
pubsub = redis.pubsub()
pubsub.subscribe(cfg['sub'])

def talktoadxv(ip, port, slab, slabs, master, h5):
    """
    Sets up a socket connection with a running adxv session.
    Takes a number of parameters and sends them across the
    connection in the stated order.
    """
    logger.debug('Starting socket connection with arguments:')
    logger.debug('ip: %s' % (ip))
    logger.debug('port: %s' % (port))
    logger.debug('slab: %s' % (slab))
    logger.debug('slabs: %s' % (slabs))
    logger.debug('master: %s' % (master))
    logger.debug('h5: %s' % (h5))
    a = adxvsocket(ip,int(port))
    a.set_slab(int(slab))
    a.increment_slabs()
    a.load_image(master)
    a.load_image(h5)
    a.set_slabs(int(slabs))
    a.stride(int(slabs))
    a.raise_window('Image')
    a.raise_window('Load')

# Listen and load loop
for message in pubsub.listen():

    #Need to filter out first message as it is always '1'.
    if message['data'] != 1:

        data_raw = message['data'] # message contains more than the data field
        data = json.loads(data_raw.decode('utf-8')) # python3 json does not assume text
        master = data[0] # master file
        h5 = data[1] # data file
        slabs = int(1/data[2]) # Osc/frame. Sum until 1 degree.

        # Wait until files hit disk
        while not os.path.exists(h5):
            logger.info('Waiting for files to hit disk...')
            sleep(2)

        # Run function
        talktoadxv(cfg['ip'], cfg['port'], cfg['slab'], slabs, master, h5)

#if __name__ == '__main__':
#    talktoadxv(ip, port, slab, slabs, master, h5)
