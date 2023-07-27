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

