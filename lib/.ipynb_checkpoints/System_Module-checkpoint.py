import numpy as np


class PassThroughSystem():
    
    def __init__(self, time, dT, nu, ny, pass_func=None, ystar=None):
        
        self.time = time # time array
        
        self.dT = dT # time step
        
        self.nu = nu # number of system inputs
        
        self.ny = ny # number of system outputs
        
        self.pass_through_function = pass_func # pass-through function
        
        # reference output value
        if ystar is None:
            self.ystar = np.zeros((ny,len(self.time)))
        else:
            self.ystar = ystar.reshape(-1,len(time)) 
        
        self.u = np.zeros((self.nu,len(self.time))) # array of system input values
        
        self.y = np.zeros((self.ny,len(self.time))) # array of system output values
        
        self.es_list = None
        
    # set list of ES controllers that provide input to the system
    # inputs are stacked vertically while timestepping
    def set_es_list(self, es_list):
        
        self.es_list = es_list # list of ES controllers that provide input to the system
        
        # calculate number of system inputs and create new system input array
        self.nu = 0
        for k1, es in enumerate(self.es_list):
            self.nu = self.nu + es.nc
        self.u = np.zeros((self.nu,len(self.time)))
    
    # step through time
    def step(self, kt, u=None):
        
        # stack ES control values into system input vector
        utemp = np.zeros((1,1))
        if kt == 0:
            for k1, es in enumerate(self.es_list):
                utemp = np.vstack((utemp,es.theta[:,kt:kt+1]))
        if kt >= 1:
            for k1, es in enumerate(self.es_list):
                utemp = np.vstack((utemp,es.theta[:,kt-1:kt]))
        utemp = utemp[1:,:]
        
        self.u[:,kt:kt+1] = utemp # store system input
            
        self.y[:,kt:kt+1] = self.pass_through_function(self.u[:,kt:kt+1]) # calculate system output
