# Imports

"""

Comments here

"""

import numpy as np
import matplotlib.pyplot as plt


def plot_es_results(time, dT, sim_list, sys_list, obj_list, es_list, ystar=None, thetastar=None):
    
    plot_objective_function(time, obj_list)
    
    plot_output(time, sim_list, sys_list)
    
    plot_setpoint_and_control(time, es_list)
    
    plot_rho(time, es_list)
    
    plot_eps(time, es_list)
    
    plot_sigma(time, es_list)
    
    plot_xihat(time, es_list)

    
def plot_objective_function(time, obj_list):
    
    plt.figure(figsize=(16,4), facecolor="w", edgecolor="k")
    for k1, obj in enumerate(obj_list):
        plt.plot(time,obj.psi, label=f"Objective function {k1}")
    plt.title("Objective Function(s): " + r"$\Psi$")
    plt.xlabel("Time [s]")
    plt.legend()
    
    plt.show()
    

def plot_output(time, sim_list, sys_list, ystar=None):

#     plt.figure(figsize=(16,4), facecolor="w", edgecolor="k")
#     if ystar is not None:
#         plt.plot(time,ystar.T,"--",label=" desired system output (known)")
#     # plt.plot(time,y.T,"-",label="system output (measured)")
#     if y.ndim == 1:
#         plt.plot(time,y,"-",label="system output (measured)")
#     elif y.ndim == 2:
#         for ky in range(0,y.shape[0]):
#             plt.plot(time,y[ky,:].T,"-",label=f"system output (measured): $y_{ky}$")
#     plt.title("System Output and Reference Signal")
#     plt.xlabel("Time [s]")
#     plt.legend()

#     plt.show()
#     plt.plot(time,y[ky,:].T,"-",label=f"system output (measured): $y_{ky}$")

    plt.figure(figsize=(16,4), facecolor="w", edgecolor="k")
    for k1, sys in enumerate(sys_list):
        if sys.ystar is not None:
            for ky in range(0,sys.ystar.shape[0]):
                plt.plot(time,sys.ystar[ky,:].T,"--",label=f"System {k1} desired output {ky} (known)")
        for ky in range(0,sys.y.shape[0]):
            plt.plot(time,sys.y[ky,:].T,"-",label=f"System {k1} output (measured): $y_{ky}$")
    plt.title("System Output(s) and Reference Signal(s)")
    plt.xlabel("Time [s]")
    plt.legend()
    
    plt.show()
    
    
def plot_setpoint_and_control(time, es_list):

    plt.figure(figsize=(16,4), facecolor="w", edgecolor="k")
    for es in es_list:
        if es.nc == 1:
            if es.name == "":
                plt.plot(time,es.thetahat.T,label="Setpoint " + r"$\hat{\theta}$")
                plt.plot(time,es.theta.T,label="Control " + r"$\theta$")
            else:
                plt.plot(time,es.thetahat.T,label=f"{es.name} Setpoint " + r"$\hat{\theta}$")
                plt.plot(time,es.theta.T,label=f"{es.name} Control " + r"$\theta$")
        if es.nc == 2:
            if es.name == "":
                plt.plot(time,es.thetahat[0,:].T,label="Setpoint Channel 1 " + r"$\hat{\theta}_{c}$")
                plt.plot(time,es.theta[0,:].T,label="Control Channel 1 " + r"$\theta_{c}$")
                plt.plot(time,es.thetahat[1,:].T,label="Setpoint Channel 2 " + r"$\hat{\theta}_{s}$")
                plt.plot(time,es.theta[1,:].T,label="Control Channel 2 " + r"$\theta_{s}$")
            else:
                plt.plot(time,es.thetahat[0,:].T,label=f"{es.name} Setpoint Channel 1 " + r"$\hat{\theta}_{c}$")
                plt.plot(time,es.theta[0,:].T,label=f"{es.name} Control Channel 1 " + r"$\theta_{c}$")
                plt.plot(time,es.thetahat[1,:].T,label=f"{es.name} Setpoint Channel 2 " + r"$\hat{\theta}_{s}$")
                plt.plot(time,es.theta[1,:].T,label=f"{es.name} Control Channel 2 " + r"$\theta_{s}$")
        if es.nc >= 3:
            if es.name == "":
                for kc in range(0,es.nc):
                    plt.plot(time,es.thetahat[kc,:].T,label=f"Setpoint Channel {kc} " + r"$\hat{\theta}$" + f"_{kc}")
                    plt.plot(time,es.theta[kc,:].T,label=f"Control Channel {kc} " + r"$\hat{\theta}$" + f"_{kc}")
            else:
                for kc in range(0,es.nc):
                    plt.plot(time,es.thetahat[kc,:].T,"--",label=f"{es.name} Setpoint Channel {kc} " + r"$\hat{\theta}$" + f"_{kc}")
                    plt.plot(time,es.theta[kc,:].T,label=f"{es.name} Control Channel {kc} " + r"$\hat{\theta}$" + f"_{kc}")
    plt.title("ES Setpoint(s) and Control(s)")
    plt.xlabel("Time [s]")
    plt.legend()
    
    plt.show()
    
    
def plot_rho(time, es_list):

    plt.figure(figsize=(16,4), facecolor="w", edgecolor="k")
    for es in es_list:
        if es.nc == 1:
            if es.name == "":
                plt.plot(time,es.rho.T,label=r"$\rho$")
            else:
                plt.plot(time,es.rho.T,label=f"{es.name} " + r"$\rho$")
        if es.nc == 2:
            if es.name == "":
                plt.plot(time,es.rho[0,:].T,label="Channel 1 $\rho_{c}$")
                plt.plot(time,es.rho[1,:].T,label="Channel 2 $\rho_{s}$")
            else:
                plt.plot(time,es.rho[0,:].T,label=f"{es.name} Channel 1 " + r"$\rho_{c}$")
                plt.plot(time,es.rho[1,:].T,label=f"{es.name} Channel 2 " + r"$\rho_{s}$")
        if es.nc >= 3:
            if es.name == "":
                for kc in range(0,es.nc):
                    plt.plot(time,es.rho[kc,:].T,label=f"Channel {kc} " + r"$\rho$" + f"_{kc}")
            else:
                for kc in range(0,es.nc):
                    plt.plot(time,es.rho[kc,:].T,label=f"{es.name} Channel {kc} " + r"$\rho$" + f"_{kc}")
    plt.title("Highpass Filtered Objective Function(s): " + r"$\rho$")
    plt.xlabel("Time [s]")
    plt.legend()
    
    plt.show()
    

def plot_eps(time, es_list):

    plt.figure(figsize=(16,4), facecolor="w", edgecolor="k")
    for es in es_list:
        if es.nc == 1:
            if es.name == "":
                plt.plot(time,es.eps.T,label="$\epsilon$")
            else:
                plt.plot(time,es.eps.T,label=f"{es.name} " + r"$\epsilon$")
        if es.nc == 2:
            if es.name == "":
                plt.plot(time,es.eps[0,:].T,label="Channel 1 " + r"$\epsilon_{c}$")
                plt.plot(time,es.eps[1,:].T,label="Channel 2 " + r"$\epsilon_{s}$")
            else:
                plt.plot(time,es.eps[0,:].T,label=f"{es.name} Channel 1 " + r"$\epsilon_{c}$")
                plt.plot(time,es.eps[1,:].T,label=f"{es.name} Channel 2 " + r"$\epsilon_{s}$")
        if es.nc >= 3:
            if es.name == "":
                for kc in range(0,es.nc):
                    plt.plot(time,es.eps[kc,:].T,label=f"Channel {kc} " + r"$\epsilon$" + f"_{kc}")
            else:
                for kc in range(0,es.nc):
                    plt.plot(time,es.eps[kc,:].T,label=f"{es.name} Channel {kc} " + r"$\epsilon$" + f"_{kc}")
    plt.title("Lowpass Filtered Objective Function(s): " + r"$\epsilon$")
    plt.xlabel("Time [s]")
    plt.legend()
    
    plt.show()
    
    
def plot_sigma(time, es_list):

    plt.figure(figsize=(16,4), facecolor="w", edgecolor="k")
    for es in es_list:
        if es.nc == 1:
            if es.name == "":
                plt.plot(time,es.sigma.T,label="$\sigma$")
            else:
                plt.plot(time,es.sigma.T,label=f"{es.name} $\sigma$")
        if es.nc == 2:
            if es.name == "":
                plt.plot(time,es.sigma[0,:].T,label="Channel 1 " + r"$\sigma_{c}$")
                plt.plot(time,es.sigma[1,:].T,label="Channel 2 " + r"$\sigma_{s}$")
            else:
                plt.plot(time,es.sigma[0,:].T,label=f"{es.name} Channel 1 " + r"$\sigma_{c}$")
                plt.plot(time,es.sigma[1,:].T,label=f"{es.name} Channel 2 " + r"$\sigma_{s}$")
        if es.nc >= 3:
            if es.name == "":
                for kc in range(0,es.nc):
                    plt.plot(time,es.sigma[kc,:].T,label=f"Channel {kc} " + r"$\sigma$" + f"_{kc}")
            else:
                for kc in range(0,es.nc):
                    plt.plot(time,es.sigma[kc,:].T,label=f"{es.name} Channel {kc} " + r"$\sigma$" + f"_{kc}")
    plt.title("Demodulated Signal(s): " + r"$\sigma$")
    plt.xlabel("Time [s]")
    plt.legend()
    
    plt.show()
    
def plot_xihat(time, es_list):

    plt.figure(figsize=(16,4), facecolor="w", edgecolor="k")
    for es in es_list:
        if es.nc == 1:
            if es.name == "":
                plt.plot(time,es.xihat.T,label=r"$\hat{\xi}$")
            else:
                plt.plot(time,es.xihat.T,label=f"{es.name} " + r"$\hat{\xi}$")
        if es.nc == 2:
            if es.name == "":
                plt.plot(time,es.xihat[0,:].T,label="Channel 1 " + r"$\hat{\xi}_{c}$")
                plt.plot(time,es.xihat[1,:].T,label="Channel 2 " + r"$\hat{\xi}_{s}$")
            else:
                plt.plot(time,es.xihat[0,:].T,label=f"{es.name} Channel 1 " + r"$\hat{\xi}_{c}$")
                plt.plot(time,es.xihat[1,:].T,label=f"{es.name} Channel 2 " + r"$\hat{\xi}_{s}$")
        if es.nc >= 3:
            if es.name == "":
                for kc in range(0,es.nc):
                    plt.plot(time,es.xihat[kc,:].T,label=f"Channel {kc} " + r"$\hat{\xi}$" + f"_{kc}")
            else:
                for kc in range(0,es.nc):
                    plt.plot(time,es.xihat[kc,:].T,label=f"{es.name} Channel {kc} " + r"$\hat{\xi}$" + f"_{kc}")
    plt.title("Gradient Estimate(s): " + r"$\hat{\xi}$")
    plt.xlabel("Time [s]")
    plt.legend()
    
    plt.show()
