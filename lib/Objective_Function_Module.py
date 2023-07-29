import numpy as np

class ObjectiveFunction():
    
    def __init__(self, time, dT, obj_func=None, ystar=None):
        
        self.time = time # time array
        
        self.dT = dT # timestep
        
        self.objective_function = obj_func # objective function
        
        self.ystar = ystar # reference signal
        
        self.psi = np.zeros(len(self.time)) # objective function value
        
        self.sys_list = None # list of systems
        
    # set list of systems from which outputs values are used to calculate objective function value
    # system outputs are stacked vertically
    def set_system_list(self, sys_list):
        
        self.sys_list = sys_list # system list
        
        # calculate number of system outputs and create new system output measurement array
        self.ny = 0
        for k1, sys in enumerate(self.sys_list):
            self.ny = self.ny + sys.ny
        self.y = np.zeros((self.ny,len(self.time)))
        
        # redefine reference signal if None given
        if self.ystar is None:
            self.ystar = np.zeros((self.ny,len(self.time)))
        
    # receive measurements from system(s) in sys_list
    def get_measurements(self, kt):

        # stack system output measurements vertically
        ytemp = np.zeros((0,1))
        for k1, sys in enumerate(self.sys_list):
            ytemp = np.vstack((ytemp, sys.y[:,kt:kt+1]))            
        # ytemp = ytemp[1:,:]
        self.y[:,kt:kt+1] = ytemp

    # calculate objective function value
    def compute_objective_function(self, kt):

        # if no reference signal, calculate objective function value assuming reference of 0 for all outputs
        if self.ystar is None:
            self.psi[kt] = self.objective_function(self.y[:,kt])
        # if reference signal exists, calculate objective function value
        else:
            if self.ystar.ndim == 1:
                self.psi[kt] = self.objective_function(self.y[:,kt], self.ystar[kt])
            if self.ystar.ndim == 2:
                self.psi[kt] = self.objective_function(self.y[:,kt], self.ystar[:,kt])