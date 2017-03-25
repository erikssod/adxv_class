# adxv_class
A simple python class wrapping the adxv socket functions.

From the class header:

    Sets up a socket connection to a running adxv session, as long as it has 
    been started in socket mode (i.e adxv -socket 1234). Adxv defaults to port 8100,
    unless given as an argument after the socket flag. Can also be set with the
    environment variable ADXV_DISPLAY_PORT.
    
    Class provides one function per socket command for clarity.
    
    See http://www.scripps.edu/tainer/arvai/adxv/AdxvUserManual.pdf for adxv manual. 
    
See adxv_load_next.py for an example application using the class.
