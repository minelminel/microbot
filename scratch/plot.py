import math
import random
import matplotlib.pyplot as plt

xmin, xmax, ymin, ymax = (0, 10, 0, 10)

x = 3
y = 3
z = 45

# to get Z axis value, we must normalize degrees dividing by 45 and drawing a line with this slope
center = (x, y)
# sin(theta) = O/H
point = (math.sin(math.radians(z)) + x, math.cos(math.radians(z)) + y)
print(center, point)

fig = plt.figure(figsize=(5,5))
# position
ax_pos = fig.add_axes([0, 0, 1, 1])
ax_pos.plot(x, y, "o", markerfacecolor="none", color="blue", ms=50)
ax_pos.set_xlabel("X")
ax_pos.set_ylabel("Y")
ax_pos.grid()
# direction
ax_dir = fig.add_axes([0, 0, 1, 1])
ax_pos.plot(
    [center[0], point[0]],
    [center[1], point[1]],
    "-",
    color="red",
)
# layout
plt.xlim([xmin, xmax])
plt.ylim([ymin, ymax])
plt.show()

# fig.clear()
