# extremum-seeking

Extremum Seeking (ES) is a model-free, online or offline, optimization algorithm that approximates gradient descent. ES estimates the gradient of a system by modulating the input to a system, then filtering and demodulation of an objective function value based on system output.

This project contains three implementations of extremum seeking, meant to be plug-and-play into simulations or real-world applications: 1D-ES, 2D-ES, ND-ES (multi-dimensional). Multiple ES instances of any type can be used in conjunction. Jupyter notebooks contain several simulation examples of the ES implementations on static and dynamic systems.


## <center> ES Operation </center>

This section covers the operation of a single 1D-ES algorithm.

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

This section describes the parameters of an instance of 1D-ES with sinusoidal perturbation.

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


## <center> Inside the ES algorithm </center>

This section details the inner workings of the ES algorithm.

Here, we define $s$ as the Laplace variable, $k$ as the index for discretized equations, and $T$ as the discretized timestep. Discretized representations are done using the ZOH method, for display simplicity, where $z = \exp \left( s T \right)$ is approximated by $z \approx 1 + s T$ and $s \approx T^{-1} \left(z - 1 \right)$.

#### Objective function: $\Psi$
The ES algorithm received the objective function value $\Psi$

#### $\rho$: Changes in the objectuve function due to the perturbation
The objective function value, $\Psi$, passes through a high-pass filter to remove low frequency content, such as changes in the objective function value due to changes in the setpoint. Changes in the objective function value due to the sinusoidal perturbation pass through the filter. The output of the high-pass filter is $\rho$:

<p align="center">
Continuous representation: $\rho = \displaystyle \frac{s}{s + \omega_{h}} \Psi$
$\quad | \quad$
Discretized representation, indexed by $k$: $\rho_{k} = \left( 1 - T \omega_{h} \right) \rho_{k-1} + \Psi_{k} - \Psi_{k-1}$
</p>

<!--
\begin{aligned}
\text{Continuous representation: } \rho = \displaystyle \frac{s}{s + \omega_{h}} \Psi \quad | \quad \text{Discretized representation, indexed by } k \text{: } \rho_{k} = \left( 1 - T \omega_{h} \right) \rho_{k-1} + \Psi_{k} - \Psi_{k-1}
\end{aligned}
-->


#### $\epsilon$: Changes in the objective function due to the setpoint
A pertinent value is $\epsilon$, which is the difference between the objective function value and the output of the high-pass filter. This can be viewed as the objective function component due to the setpoint $\hat{\theta}$:

<p align="center">
Continuous representation: $\epsilon = \Psi - \rho$
$\quad | \quad$
Discretized representation, indexed by $k$: $\epsilon_{k} = \Psi_{k} - \rho_{k}$
</p>

<!--
\begin{aligned}
\text{Continuous representation: } \epsilon = \Psi - \rho \quad | \quad \text{Discretized representation, indexed by } k \text{: } \epsilon_{k} = \Psi_{k} - \rho_{k}
\end{aligned}
-->

#### $\sigma$: Demodulated value
The high-pass filtered objective function value $\rho$ then is demodulated by multiplying it by the sinusoidal perturbation, and dividing by the perturbation ampltiude, giving $\sigma$:

<p align="center">
Continuous representation: $\sigma = \displaystyle \frac{2}{a} \sin \left( \omega t \right) \rho$
$\quad | \quad$
Discretized representation, indexed by $k$: $\sigma_{k} = \displaystyle \frac{2}{a} \sin \left( \omega k T \right) \rho_{k}$
</p>

<!--
\begin{aligned}
\text{Continuous representation:  } \sigma = \displaystyle \frac{2}{a} \sin \left( \omega t \right) \rho \quad | \quad \text{Discretized representation, indexed by } k \text{:  } \sigma_{k} = \displaystyle \frac{2}{a} \sin \left( \omega k T \right) \rho_{k}
\end{aligned}
-->


#### $\hat{\xi}$: Gradient Estimate
The demodulated value passes through a low-pass filter to remove sinsoidal and other high frequency content, giving an estimate of the gradient of the objective function $\Psi$ with respect to the setpoint $\hat{\theta}$, $\hat{\xi}$:

<p align="center">
Continuous representation: $\hat{\xi} = \displaystyle \frac{\omega_{l}}{s + \omega_{l}} \sigma$ $\quad$ | $\quad$ Discretized representation, indexed by $k$: $\hat{\xi}_{k} = \left( 1 - T \omega_{l} \right) \hat{\xi}_{k-1} + T \omega_{l} \sigma_{k-1}$
</p>

<!--
\begin{aligned}
\text{Continuous representation: } \hat{\xi} = \displaystyle \frac{\omega_{l}}{s + \omega_{l}} \sigma \quad | \quad \text{Discretized representation, indexed by } k \text{: } \hat{\xi}_{k} = \left( 1 - T \omega_{l} \right) \hat{\xi}_{k-1} + T \omega_{l} \sigma_{k-1}
\end{aligned}
-->

#### $\hat{\theta}$: Setpoint
The ES algotrithm then integrates its gradient estimate, scaled by a gain $b$, to update its setpoint $\hat{\theta}$. Positive values of $b$ are used to maximize $\Psi$, and negative values of $b$ are used to minimize $\Psi$ :

<p align="center">
Continuous representation: $\hat{\theta} = \displaystyle \pm \frac{b}{s} \hat{\xi}$ $\quad$ | $\quad$ Discretized representation, indexed by $k$: $\hat{\theta}_{k} = \hat{\theta}_{k-1} \pm \displaystyle b T \hat{\xi}_{k-1}$
</p>

<!--
\begin{aligned}
\text{Continuous representation: } \hat{\theta} = \displaystyle \pm \frac{b}{s} \hat{\xi} \quad | \quad \text{Discretized representation, indexed by } k \text{: } \hat{\theta}_{k} = \hat{\theta}_{k-1} \pm \displaystyle b T \hat{\xi}_{k-1}
\end{aligned}
-->


#### $\theta$: Control
The ES algotrithm adds the perturbation to its setpointto update its setpoint $\hat{\theta}$, giving the control value, $\theta$:

<p align="center">
  Continuous representation: $\theta = \hat{\theta} + a \sin \left( \omega t \right)$ $\quad$ | $\quad$ Discretized representation, indexed by $k$: $\theta_{k} = \hat{\theta}_{k} + a \sin \left( \omega k T \right)$
</p>

<!--
\begin{aligned}
\text{Continuous representation: } \theta = \hat{\theta} + a \sin \left( \omega t \right) \quad | \quad \text{Discretized representation, indexed by } k \text{: } \theta_{k} = \hat{\theta}_{k} + a \sin \left( \omega k T \right)
\end{aligned}
-->


## <center> Extremum Seeking Gradient Estimation </center>

This section gives a derivation of how the gradient is estimated by ES.

Here, we take advantage of second order Taylor Expansion: where $f(b) \approx f (a) + \displaystyle \left. \frac{df}{dx} \right|_{x = a} \left( b - a \right) + \left. \frac{1}{2} \frac{d^{2}f}{dx^{2}} \right|_{x = a} \left( b - a \right)^{2}$

Using a first order Taylor Expansion, the objective function can be expressed in two parts, a portion due to the setpoint, and a portion due to the perturbation:

<p align="center">
$\Psi ( \theta ) \approx \Psi ( \hat{\theta} ) + \displaystyle \left. \frac{d \Psi}{d \theta} \right|_{\theta = \hat{\theta}} \left( \theta - \hat{\theta} \right) = \Psi ( \hat{\theta} ) + \displaystyle \left. \frac{d \Psi}{d \theta} \right|_{\theta = \hat{\theta}} a \sin \left( \omega t \right)$
</p>

<!--
\begin{aligned}
\Psi ( \theta ) \approx \Psi ( \hat{\theta} ) + \displaystyle \left. \frac{d \Psi}{d \theta} \right|_{\theta = \hat{\theta}} \left( \theta - \hat{\theta} \right) = \Psi ( \hat{\theta} ) + \displaystyle \left. \frac{d \Psi}{d \theta} \right|_{\theta = \hat{\theta}} a \sin \left( \omega t \right)
\end{aligned}
-->

The high-pass filter removes "slow" and low frequency content, such as the portion of the objective function due to the setpoint:

<p align="center">
$\rho \approx \displaystyle \left. \frac{d \Psi}{d \theta} \right|_{\theta = \hat{\theta}} a \sin \left( \omega t \right)$
</p>

<!--
\begin{aligned}
\rho \approx \displaystyle \left. \frac{d \Psi}{d \theta} \right|_{\theta = \hat{\theta}} a \sin \left( \omega t \right)
\end{aligned}
-->

This signal is demodulated by multiplying by $\displaystyle \frac{2}{a} \sin \omega t$. The term $sin^{2}$ has a steady state and sinusoidal component:

<p align="center">
$\sigma \approx 2 \displaystyle \left. \frac{d \Psi}{d \theta} \right|_{\theta = \hat{\theta}} \sin^{2} \left( \omega t \right) = \displaystyle \left. \frac{d \Psi}{d \theta} \right|_{\theta = \hat{\theta}} \left( 1 - \cos \left( 2 \omega t \right) \right)$
</p>

<!--
\begin{aligned}
\sigma \approx 2 \displaystyle \left. \frac{d \Psi}{d \theta} \right|_{\theta = \hat{\theta}} \sin^{2} \left( \omega t \right) = \displaystyle \left. \frac{d \Psi}{d \theta} \right|_{\theta = \hat{\theta}} \left( 1 - \cos \left( 2 \omega t \right) \right)
\end{aligned}
-->

This low-pass filter removes the sinusoidal component from the demodulated signal, leaving an estimate of the gradient of the objective function with respect to the setpoint:

<p align="center">
$\hat{\xi} \approx \displaystyle \left. \frac{d \Psi}{d \theta} \right|_{\theta = \hat{\theta}}$
</p>

<!--
\begin{aligned}
\hat{\xi} \approx \displaystyle \left. \frac{d \Psi}{d \theta} \right|_{\theta = \hat{\theta}}
\end{aligned}
-->

