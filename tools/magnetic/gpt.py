import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Constants
mu_0 = 4 * np.pi * 1e-7  # Permeability of free space (in T*m/A)
p_x = 1.0  # Dipole moment in the x-direction

# Create a grid of points in 3D space
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
z = np.linspace(-5, 5, 50)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initialize the dipole orientation angle
angle = 0

# Initialize the potential array
potential = np.zeros_like(X)

# Set the position of the dipole
dipole_position = np.array([0, 0, 0])

# Create a dummy scatter plot for the colorbar
sc = ax.scatter([], [], [], c=[], cmap='viridis', s=1, alpha=0.5)  # Adjust alpha for transparency
cbar = fig.colorbar(sc, ax=ax, orientation='vertical', pad=0.05)
cbar.set_label('Scalar Potential')

def update(frame):
    global angle, potential

    # Clear the previous plot
    ax.cla()

    # Calculate the scalar potential at each point for the current orientation
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            for k in range(X.shape[2]):
                # Calculate the rotated position of each point
                x_rot = X[i, j, k] - dipole_position[0]
                y_rot = Y[i, j, k] - dipole_position[1]
                z_rot = Z[i, j, k] - dipole_position[2]
                
                # Apply the rotation matrix
                x_new = x_rot * np.cos(angle) - y_rot * np.sin(angle)
                y_new = x_rot * np.sin(angle) + y_rot * np.cos(angle)
                
                # Calculate the new distance
                r = np.sqrt(x_new**2 + y_new**2 + z_rot**2)
                
                # Calculate the potential
                potential[i, j, k] = mu_0 / (4 * np.pi) * (p_x / r**3)

    # Create a 3D scatter plot for potential with transparency
    sc = ax.scatter(X, Y, Z, c=potential, cmap='viridis', s=1, alpha=0.5)  # Adjust alpha for transparency

    # Add labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Update the angle for the next frame
    angle += np.pi / 50  # Rotate by 3.6 degrees

# Create an animation
ani = FuncAnimation(fig, update, frames=100, interval=100)

# Show the animation
plt.title('Spinning Dipole Animation')
plt.show()

