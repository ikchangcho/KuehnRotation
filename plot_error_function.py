import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf

# Define the constants
c = 1.0  # Adjust this value as needed
L = 0.01  # Adjust this value as needed
D = 1e-9  # Adjust this value as needed

# Define the function
def f(t, L, D):
    term1 = 1 - erf(L / (2 * np.sqrt(D * t)))
    term2 = (2 * (-1 + np.exp(-L**2 / (4 * D * t))) * np.sqrt(D * t)) / (L * np.sqrt(np.pi))
    return term1 - term2

# Define the time range
t_values = np.linspace(0.01, 2e7, 1000)  # Avoid t=0 to prevent division by zero
dC_dt_values = f(t_values, L, D)

# Plot the function
plt.figure(figsize=(10, 6))
plt.plot(t_values/3600, dC_dt_values, label=r'$\frac{dC(t)}{dt}$')
plt.axhline(y=0.9, color='r', linestyle='--', label='y=0.9')
plt.xlabel('Time (hour)')
plt.ylabel(r'$\frac{1}{cL}\frac{dC(t)}{dt}$')
plt.title(r'Plot of $\frac{1}{cL}\frac{dC(t)}{dt}$' f'when D={D}, L={L}')
plt.legend()
plt.grid(True)
plt.show()