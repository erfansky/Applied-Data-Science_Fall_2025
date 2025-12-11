import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Domain
x = np.linspace(0.5, 1.0, 200)
y = np.linspace(0.0, 0.5, 200)
X, Y = np.meshgrid(x, y)

# Function
Z = -0.5 + X - X*Y

# Mask for positive values
Z_pos = np.where(Z > 0, Z, np.nan)

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Full surface
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6)

# Positive region highlighted
ax.plot_surface(X, Y, Z_pos, cmap='autumn', edgecolor='none')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('Surface z = -1/2 + x - x*y with Positive Region Highlighted')

plt.show()
