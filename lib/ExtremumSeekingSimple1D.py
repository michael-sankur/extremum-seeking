# 1D Extremum Seeking Class

import numpy as np


class ExtremumSeekingSimple1D():
    """
    Class comments
    """
    
    def __init__(self, time, dT, fes, aes, kint, mode="minimize", thetahat0=None, **kwargs):
        
        self.name = ""
        if "name" in kwargs.keys():
            self.name = kwargs["name"]
        
        self.nc = 1 # number of ES channels
        
        self.time = time # time array
        
        self.dT = dT # timestep
        
        # ES algorithm probing and signal processing paramters
        self.fes = fes # ES sinusoidal modulation frequency [Hz]
        self.wes = 2*np.pi*self.fes # ES sinusoidal modulation angular frequency
        
        self.aes = aes # ES sinusoidal modulation amplitude (peak - zero)
        
        self.mode = mode # ES mode (minimize or maximize)
        
        self.whpf = self.wes/10 # ES high-pass filter angular frequency
        
        self.wlpf = self.wes/10 # ES low-pass filter angular frequency
        
        self.kint = kint # ES integrator gain
        
#         # ES measurement parameters and arrays        
#         self.ny = ny # number of measurements
        
#         self.y = np.zeros((self.ny,len(time))) # measurements passed into ES
        
#         self.ystar = np.zeros((self.ny,len(time))) # desired measurement value (reference signal)
        
        # ES algorithm arrays
        self.psi = np.zeros(len(time)) # objective function values
        
        self.rho = np.zeros((self.nc,len(time))) # high-pass filtered objective function
        
        self.rho2 = np.zeros((self.nc,len(time))) # high-pass filtered objective function
        
        self.eps = np.zeros((self.nc,len(time))) # low-pass filtered objective function
        
        self.sigma = np.zeros((self.nc,len(time))) # demodulated value
        
        self.xihat = np.zeros((self.nc,len(time))) # gradient estimate (with respect to thetahat)
        
        self.thetahat = np.zeros((self.nc,len(time))) # ES setpoint
        
        self.theta = np.zeros((self.nc,len(time))) # ES control value
        
        # Initialize setpoint and control states
        if thetahat0 is not None:
            self.thetahat[0] = thetahat0 # initialize setpoint
        
        self.theta[0] = self.thetahat[0] + self.aes*np.sin(self.wes*self.time[0]) # initialize control

    # def set_objective_function(self, obj_func):
    #     self.objective_function = obj_func
    

    def get_objective_value(self, kt, psi):
        """
        Receive the objective function value (computed externally to an ES instance), and store in array.
        
        At the first timestep, set the initial value of psi (low-pass filtered objective function) to the objective function value
        """
        
        self.psi[kt] = psi
        if kt == 0:
            self.eps[0] = self.psi[0]
    
    def ES_function(self, kt, psi=None):
        """
        Computes the optimizer estimate, theta, progressing the ES algorithm by one timestep
        
        Inputs:
        kt: int
            the current timestep
        psi: float, optional
            objective function value (default is None)
            
        Outputs:
        
        If the current timestep is 0: then do nothing except to set initial value of eps(ilon) to psi
        
        If the current timestep is 1 or greater:
        
        """
        
        # receive objective function value
        if psi != None:
            self.psi[kt] = psi
            
        # ES controller algorithm
        
        # at the first timestep, set the value of eps to the objective function value psi[0]
        if kt == 0:
            
            # initialize lowpass filtered objective
            self.eps[0,kt] = self.psi[kt]
            
        if kt >= 1:

            # no highpass filter
            self.rho[0,kt] = self.psi[kt]
            # highpass filter
            self.rho[0,kt] = (1 - self.whpf*self.dT)*self.rho[0,kt-1] + self.psi[kt] - self.psi[kt-1]

            # objective function error
            self.eps[0,kt] = self.psi[kt] - self.rho[0,kt]

            # demodulate
            self.sigma[0,kt] = 2/self.aes*np.sin(self.wes*self.time[kt])*self.rho[0,kt]

            # no lowpass filter
            self.xihat[0,kt] = self.sigma[0,kt]
            # lowpass filter demodulated values
            self.xihat[0,kt] = (1 - self.wlpf*self.dT)*self.xihat[0,kt-1] + self.wlpf*self.dT*self.sigma[0,kt-1]

            # integrate to obtain setpoint
            # + to maximize objective function
            # - to minimize objective function
            if self.mode == "minimize":
                self.thetahat[0,kt] = self.thetahat[0,kt-1] - self.kint*self.dT*self.xihat[0,kt-1]
            if self.mode == "maximize":
                self.thetahat[0,kt] = self.thetahat[0,kt-1] + self.kint*self.dT*self.xihat[0,kt-1]

            # add probe to setpoint
            self.theta[0,kt] = self.thetahat[0,kt] + self.aes*np.sin(self.wes*self.time[kt])
            