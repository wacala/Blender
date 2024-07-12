from curve2mesh import revolve_curve
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Sample 2D curve coordinates
x = np.linspace(0, 1, 100)
z = x ** 2  # Example curve (parabola)

# Revolve the curve
angle_count = 50
faces = revolve_curve(x, z, angle_count, revolve_angle=2*np.pi)

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.add_collection3d(Poly3DCollection(faces, facecolors='g', linewidths=1, alpha=0.5))
ax.set_xlim(-x.max(), x.max())
ax.set_ylim(-x.max(), x.max())
ax.set_zlim(z.min(), z.max())
plt.show()