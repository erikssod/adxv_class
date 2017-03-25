class adxvsocket(object):
    '''
    Sets up a socket connection to a running adxv session, as long as it has 
    been started in socket mode (i.e adxv -socket 1234). Adxv defaults to port 8100,
    unless given as an argument after the socket flag. Can also be set with the
    environment variable ADXV_DISPLAY_PORT.
    
    Class provides one function per socket command for clarity.
    
    Note that some of these functions require a beta release of adxv, but should work just fine for the stable release. 
    
    See http://www.scripps.edu/tainer/arvai/adxv/AdxvUserManual.pdf for adxv manual. 
    '''   
    
    
    def __init__(self, host, port):
        
        import logging
        import socket
        
        self.logger = logging.getLogger()
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(fmt=('[%(levelname)s] %(name)s ''%(funcName)s | %(message)s')))
        self.logger.handlers = [handler]
        self.logger.setLevel('INFO') # or INFO, or DEBUG, etc

        self.logger = logging.getLogger(__name__)

        # logger.debug("The list has i elements")
        # logger.info("Established ssh connection")
        # logger.warning("Max number of iterations reached")
        # logger.error("Couldn't copy file. Permission denied")
        # logger.critical("Configuration file damaged")
        
        self.logger.debug('Attempting to connect to Host:Port - %s:%i' % (host, port))
        
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.clientsocket.connect((host, port))
            self.logger.info('Connected to Host:Port - %s:%i' % (host, port))
        except Exception as e:
            self.logger.error(e)        

    ##############################
    #     Socket commands
    ##############################    

    def load_image(self,image_file):
        '''
        Load an image file  
        '''
        payload = 'load_image %s\n' % (image_file)
        self.send(payload)

    def raise_window(self,window):
        '''
        Raises a Window. <window> must be one of 
        'Control', 'Image', 'Magnify', 'Line', or 
        'Load'. 
        '''
        payload = 'raise_window %s\n' % (window)
        self.send(payload)

    def raise_image(self):
        '''
        Raises image window; see raise_window for 
        additional options but this seems like the 
        most common one.
        '''
        payload = 'raise_window Image\n'
        self.send(payload)

    def save_image(self,path_name_format):
        '''
        Save an image file (jpeg or tiff) 
        '''
        payload = 'save_image %s\n' % (path_name_format)
        self.send(payload)

    def slab(self,N):
        '''
        Display slab N 
        '''
        payload = 'slab %i\n' % (N)
        self.send(payload)

    def set_slab(self,N):
        '''
        Same as slab, but don’t load the image 
        '''
        payload = 'set_slab %i\n' % (N)
        self.send(payload)

    def slabs(self,N):
        '''
        Slab thickness to display 
        '''
        payload = 'slabs %i\n' % (N)
        self.send(payload)

    def set_slabs(self,N):
        '''
        Same as slabs, but don’t load the image 
        '''
        payload = 'set_slabs %i\n' % (N)
        self.send(payload)

    def exit(self):
        '''
        Exit Adxv
        '''
        payload = 'exit\n'
        self.send(payload)
            
    def stride(self, N):
        """
        stride - sets Stride in the Load Window
        """
        payload = 'stride %i\n' % (N)
        self.send(payload)
        
    def increment_slabs(self):
        """
        increment_slabs - checks the +Slabs checkbox in the Load Window
        """
        payload = 'increment_slabs\n'
        self.send(payload)
        
    def increment_files(self):
        """
        increment_files - unchecks the +Slabs checkbox in the Load Window
        """
        payload = 'increment_files\n'
        self.send(payload)
        
    def contrast_min(self, N):
        """
        contrast_min - sets the min contrast value
        """
        payload = 'contrast_min %i\n' % (N)
        self.send(payload)
        
    def contrast_max(self, N):
        """
        contrast_max - sets the max contrast value
        """
        payload = 'contrast_max %i\n' % (N)
        self.send(payload)
        
    def send(self,payload):
        '''
        Takes command, encodes it, and sends it down the socket.
        '''
        try:
            self.logger.debug("payload = %s" % (payload))
            self.clientsocket.sendall(payload.encode())
        except Exception as e:
            self.logger.error(e)
