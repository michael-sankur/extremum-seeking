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
        utemp = np.zeros((0,1))
        if kt == 0:
            for k1, es in enumerate(self.es_list):
                utemp = np.vstack((utemp,es.theta[:,kt:kt+1]))
        if kt >= 1:
            for k1, es in enumerate(self.es_list):
                utemp = np.vstack((utemp,es.theta[:,kt-1:kt]))
        # utemp = utemp[1:,:]
        
        self.u[:,kt:kt+1] = utemp # store system input
            
        self.y[:,kt:kt+1] = self.pass_through_function(self.u[:,kt:kt+1]) # calculate system output
        
        
class LinearSystem():
    
    def __init__(self, time, dT, A, B, C, D, x0=None, ystar=None):
        
        self.time = time
        
        self.dT = dT
        
        self.A = A # system matrix
        
        self.B = B # input matrix
        
        self.C = C # output matrix
        
        self.D = D # feedthrough matrix
        
        self.nx = self.A.shape[0] # number of system states
        
        self.nu = self.B.shape[1] # number of inputs
        
        self.ny = self.C.shape[0] # number of outputs
        
        self.x = np.zeros((self.nx,len(self.time))) # state
        
        self.xdot = np.zeros((self.nx,len(self.time))) # time derivative of state
        
        self.u = np.zeros((self.nu,len(self.time))) # input
        
        self.y = np.zeros((self.ny,len(self.time))) # output
        
        # initialize state
        # if no initial state condition, initialize as 0
        if x0 is None:
            pass
        else:
            self.x[:,0:1] = x0.reshape(-1,1)
        
        # reference output value
        # if no reference value, initialize as 0
        if ystar is None:
            self.ystar = np.zeros((ny,len(self.time)))
        else:
            self.ystar = ystar.reshape(-1,len(time))
                
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
        utemp = np.zeros((0,1))
        if kt == 0:
            for k1, es in enumerate(self.es_list):
                utemp = np.vstack((utemp,es.theta[:,kt:kt+1]))
        if kt >= 1:
            for k1, es in enumerate(self.es_list):
                utemp = np.vstack((utemp,es.theta[:,kt-1:kt]))
        # utemp = utemp[1:,:]

        self.u[:,kt:kt+1] = utemp # store system input        
        
        self.xdot[:,kt:kt+1] = self.A@self.x[:,kt:kt+1] + self.B@self.u[:,kt:kt+1] # time derivative of state
        
        self.x[:,kt+1:kt+2] = self.x[:,kt:kt+1] + self.dT*self.xdot[:,kt:kt+1] # integrate dx/dt to update state
        
        self.y[:,kt:kt+1] = self.C@self.x[:,kt:kt+1] + self.D@self.u[:,kt:kt+1] # calculate system output
        