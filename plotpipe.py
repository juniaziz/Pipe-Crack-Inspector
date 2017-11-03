import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import math

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
cracks=[(14,30),(14.5,31),(15,30),(15.5,30),(16,30),(16.5,29),(17,28),(17.5,27),(18,28),(18.5,29),(19,30),
        (35.5,-92),(36,-94),(36.5,-95),(37,-93),(37,-91),(37.5,-88),(37.5,-86),(38,-84),(38.5,-85),(39,-88),(39.5,-86),(37.5,-92.5),(38,-94),(38.5,-92),(39,-95),(39.5,-97)]


R=14
L=54
for crack in cracks:
    ax.scatter(R*math.cos(crack[1]/57.3),crack[0],R*math.sin(crack[1]/57.3),c='#ff0000')
# Pipe
x=np.linspace(-1*R, R, 100)
y=np.linspace(0, L, 100)
Xc, Yc=np.meshgrid(x, y)
Zc = np.sqrt(R**2-Xc**2)

# Draw parameters
rstride = 4
cstride = 4
ax.plot_surface(Xc, Yc, Zc, alpha=0.3, rstride=rstride, cstride=cstride)
ax.plot_surface(Xc, Yc, -Zc, alpha=0.3, rstride=rstride, cstride=cstride)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.auto_scale_xyz([-L/2, L/2], [0, L], [-L/2, L/2])
plt.show()
