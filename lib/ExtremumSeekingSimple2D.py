# 2D Extremum Seeking Class

import numpy as np        


class ExtremumSeekingSimple2D():
    """
    Class comments
    """
    
    def __init__(self, time, dT, fes, aes, kint, mode="minimize", thetahat0=np.zeros((2,1)), **kwargs):
        
        self.name = ""
        if "name" in kwargs.keys():
            self.name = kwargs["name"]
        
        self.nc = 2 # number of ES channels
                
        self.time = time # time array
        
        self.dT = dT # timestep
        
        # ES algorithm paramters                
        self.fes = fes # ES sinusoidal modulation frequency [Hz]
        self.wes = 2*np.pi*self.fes # ES sinusoidal modulation angular frequency
        
        self.aes = aes*np.ones(self.nc) # ES sinusoidal modulation amplitude (peak - zero)
        
        self.mode = mode # ES mode (minimize or maximize)
        
        self.whpf = self.wes/10 # ES high-pass filter angular frequency
        
        self.wlpf = self.wes/10 # ES low-pass filter angular frequency
        
        self.kint = kint*np.ones(self.nc) # ES integrator gain
        
        # ES algorithm arrays
        self.psi = np.zeros(len(time)) # objective function values
        
        self.rho = np.zeros((self.nc,len(time))) # high-pass filtered objective function
        
        self.eps = np.zeros((self.nc,len(time))) # low-pass filtered objective function
        
        self.sigma = np.zeros((self.nc,len(time))) # demodulated value
        
        self.xihat = np.zeros((self.nc,len(time))) # gradient estimate (with respect to thetahat)
        
        self.thetahat = np.zeros((self.nc,len(time))) # ES setpoint
        
        self.theta = np.zeros((self.nc,len(time))) # ES control value
        
        # ES measurement arrays
#         self.ny = ny
#         self.y = np.zeros((ny,len(time))) # local objective function
        
#         self.ystar = np.zeros((ny,len(time)))
                
        # Initialize setpoint and control states
        
        self.thetahat[:,0:1] = np.asarray(thetahat0).reshape((self.nc,1))
        
        self.theta[0,0] = self.thetahat[0,0] + self.aes[0]*np.cos(self.wes*self.time[0])
        self.theta[1,0] = self.thetahat[1,0] + self.aes[1]*np.sin(self.wes*self.time[0])
        
#     def get_measurements(self, y):
        
#         self.y[:,kt] = y

    def get_objective_value(self, kt, psi):
        """
        Receive the objective function value (computed externally to an ES instance), and store in array.
        
        At the first timestep, set the initial value of psi (low-pass filtered objective function) to the objective function value
        """
        
        self.psi[kt] = psi
        if kt == 0:
            self.eps[0] = self.psi[0]
    
    def ES_function(self, kt, psi=None):
        
        # receive objective function value
        if psi != None:
            self.psi[kt] = psi
        
        # ES controller algorithm
        if kt == 0:
            
            # initialize lowpass filtered objective
            self.eps[:,0] = self.psi[0]
        
#         elif kt >= 1:
            
#             self.psi[kt] = compute_objective_function(self.y[:,kt], self.ystar[:,kt])
            
        # ES controller algorithm
        if kt == 0:
            self.theta[0,kt] = self.thetahat[0,kt] + self.aes[0]*np.cos(self.wes*self.time[kt])
            self.theta[1,kt] = self.thetahat[1,kt] + self.aes[1]*np.sin(self.wes*self.time[kt])
        elif kt >= 1:

            # no highpass filter
            self.rho[:,kt] = self.psi[kt]
            # highpass filter
            self.rho[:,kt] = (1 - self.whpf*self.dT)*self.rho[:,kt-1] + self.psi[kt] - self.psi[kt-1]

            # objective function error
            self.eps[:,kt] = self.psi[kt] - self.rho[:,kt]

            # demodulate
            self.sigma[0,kt] = 2/self.aes[0]*np.cos(self.wes*self.time[kt])*self.rho[0,kt]
            self.sigma[1,kt] = 2/self.aes[1]*np.sin(self.wes*self.time[kt])*self.rho[1,kt]

            # no lowpass filter
            self.xihat[:,kt] = self.sigma[:,kt]
            # lowpass filter demodulated values
            self.xihat[:,kt] = (1 - self.wlpf*self.dT)*self.xihat[:,kt-1] + self.wlpf*self.dT*self.sigma[:,kt-1]

            # integrate to obtain setpoint
            # + to maximize objective function
            # - to minimize objective function
            if self.mode == "minimize":
                self.thetahat[:,kt] = self.thetahat[:,kt-1] - self.kint[0]*self.dT*self.xihat[:,kt-1]
            if self.mode == "maximize":
                self.thetahat[:,kt] = self.thetahat[:,kt-1] + self.kint[1]*self.dT*self.xihat[:,kt-1]

            # add probe to setpoint
            self.theta[0,kt] = self.thetahat[0,kt] + self.aes[0]*np.cos(self.wes*self.time[kt])
            self.theta[1,kt] = self.thetahat[1,kt] + self.aes[1]*np.sin(self.wes*self.time[kt])
            
                