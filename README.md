# extremum-seeking

 Extremum Seeking (ES) is a model-free, online or offline, optimization algorithm that approximates gradient descent. ES estimates the gradient of a system by modulating the input to a system, then filtering and demodulation of an objective function value based on system output.

This project contains three implementations of extremum seeking, meant to be plug-and-play into simulations or real-world applications: 1D-ES, 2D-ES, ND-ES (multi-dimensional). Multiple ES instances of any type can be used in conjunction. Jupyter notebooks contain several simulation examples of the ES implementations on static and dynamic systems.


## <center> ES Operation </center>

ES approximates gradient descent by steering its optimizer estimate, $\hat{\theta}$, with an estimate of the gradient of an objective function to $\hat{\theta}$.

ES operates as follows:

The system input is formed by adding a sinusoidal perturbation $a \sin \left( \omega t \right)$ to the ES setpoint $\hat{\theta}$, such that $\theta = \hat{\theta} + a \sin \left( \omega t \right)$. The setpoint is the estimate of the (local) optimizer.

The system input $\theta$ passes through the unknown system, resulting in system output (measurements) $\textbf{y} \left( u \right)$.

Either a central entity computes the objective function value $\Psi = \Psi \left( \bf{y} \right)$, or the ES algorithm may take in the measurements $\bf{y}$, and compute $\Psi$ itself.

A high-pass filter removes low-frequency content from $\Psi$, giving $\rho$

This value is demodulated by multiplying by $\sin \left( \omega t \right)$, giving $\sigma$.

A low-pass filter removes high-frequency content from this value, giving the gradient estimate, $\hat{\xi}$.

The gradient estimate is integrated back into the setpoint (optimizer estimate), updating $\hat{\theta}$.


## <center> Extremum Seeking Parameters </center>

This section describes the parameters of an instance of 1D ES with sinusoidal perturbation.

### Parameters for Simple ES

#### Perturbation Frequency: $f$ [Hz]
The perturbation frequency $f$ determines how fast the sinusoidal perturbation cycles. This is converted into an angular frequency $\omega = 2 \pi f$.

#### Perturbation Amplitude: $a$
The perturbation amplitude $a$ determines how far into the search space the perturbation reaches. Larger values tend to provide faster convergence to an optimizer, as the ES can assess more of the search space. Smaller values may provide slower convergence to an optimizer, but the control value will remain closer to the optimizer after convergence.

#### Integrator Gain: $b$
The integerator gain $b$ determines how far the ES algorithm will move in the direction of the gradient estimate. This value essentially scales the gradient estimate. This value can be though of as similar to the step size in gradient descent. Larger values generally provide faster convergence to an optimizer, but may lead to instability.

### Parameters for Advanced ES

#### High-pass filter frequency: $\omega_h$
The high-pass filter frequency determines what frequency content passes through the high-pass filter. This value is typically set to $\omega_{h} = 0.1 \omega$, and SimpleES classes default to this value.

#### Low-pass filter frequency: $\omega_l$
The low-pass filter frequency determines what frequency content passes through the low-pass filter. The low-pass filter attenuates content in the demodulated signal, and typically is used to attenuate content such as that due to the perturbation. This value is typically set to $\omega_{l} = 0.1 \omega$, and SimpleES classes default to this value.
