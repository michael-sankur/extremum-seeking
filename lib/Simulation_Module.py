# Simulation Class

import numpy as np

class Simulation():
    
    def __init__(self, time, dT, system_list=None, es_list=None, obj_list=None, obj_to_es_map=None):
        
        self.time = time # time array
        
        self.dT = dT # timestep
        
        self.system_list = system_list # list of systems in this simulation
        
        self.es_list = es_list # list of ES controllers in this simulation
        
        self.obj_list = obj_list # list of objective functions in this simulation
        
        # self.input_mapping = input_mapping
        
        # mapping defining which objective function each ES controller in this simulation will minimize/maximize
        # indices of obj_to_es_map represent the ES controller, and values represent the objective function
        # example: [0, 0] means that two ES controllers receive and operate on a single objective function
        # example: [0, 1] means that ES controller 0 receives objective function 0, and ES controller 1 receives objective function 1
        # example: [0, 0, 1] means that ES controllers 0 and 1 receive objective function 0, and ES controller 2 receives objective function 1
        # if obj_to_es_map is None, then the mapping is ES controller k receives objective function k
        self.obj_to_es_map = obj_to_es_map
        
    def run_simulation(self):
        
        # simulate system and ES Algorithm
        for kt in range(0,len(self.time)):
            
            # each system takes a time step
            for k1, sys in enumerate(self.system_list):
                sys.step(kt)
            
            # each objective function receives measurements and calculates its value
            for k1, obj in enumerate(self.obj_list):
        
                obj.get_measurements(kt) # objective function(s) receive measurement(s)

                obj.compute_objective_function(kt) # objective function(s) calculate value(s)
            
            # each ES controller calculates its setpoint and control
            for k1, es in enumerate(self.es_list):
                # if no objective to es mapping, then map 1 to 1 in indexed order
                if self.obj_to_es_map is None:
                    es.ES_function(kt, self.obj_list[k1].psi[kt])
                # if objective to es mapping, then each ES contoller will receive the appropriate objective function value
                else:
                    obj_idx = self.obj_to_es_map[k1]
                    es.ES_function(kt, self.obj_list[obj_idx].psi[kt])
