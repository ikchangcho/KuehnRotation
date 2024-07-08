import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf

# Define the function
def f(t, L, D):
    term1 = L * (1 - erf(L / (2 * np.sqrt(D * t))))
    term2 = -2 * (-1 + np.exp(-L**2 / (4 * D * t))) * np.sqrt(D * t) / np.sqrt(np.pi)
    return term1 + term2

# Parameters
L = 1  # Adjust L as needed
D = 1  # Adjust D as needed

# Generate t values
t_values = np.linspace(0.00001, 100, 100)  # Avoiding t=0 to prevent division by zero

# Compute function values
f_values = f(t_values, L, D)

# Plot the function
plt.figure(figsize=(10, 6))
plt.plot(t_values, f_values, label=r'$f(t) = L \left(1 - \text{erf} \left(\frac{L}{2 \sqrt{D t}}\right) \right) - \frac{2 \left(-1 + e^{-\frac{L^2}{4 D t}}\right) \sqrt{D t}}{\sqrt{\pi}}$')
plt.xlabel('t')
plt.ylabel('f(t)')
plt.title('Plot of the given function')
plt.legend()
plt.grid(True)
plt.show()