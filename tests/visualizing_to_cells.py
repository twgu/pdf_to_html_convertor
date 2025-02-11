cells = []

import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(5, 5))

for cell in cells:
    no = cell['no']
    x0, y0 = cell['x0'], cell['y0']
    x1, y1 = cell["x1"], cell["y1"]

    rect = patches.Rectangle(
        (x0, y0),
        x1 - x0,
        y1 - y0,
        linewidth=1,
        edgecolor='blue' if no != 0 else 'red',
        facecolor='none'
    )

    ax.add_patch(rect)

    center_x = (x0 + x1) / 2
    center_y = (y0 + y1) / 2

    ax.text(center_x, center_y, str(no), color='red', fontsize=15, ha='center', va='center')

min_x0 = min(cell['x0'] for cell in cells)
max_x1 = max(cell['x1'] for cell in cells)
min_y0 = min(cell['y0'] for cell in cells)
max_y1 = max(cell['y1'] for cell in cells)

ax.set_xlim(min_x0 - 30, max_x1 + 30)
ax.set_ylim(min_y0 - 30, max_y1 + 30)

ax.invert_yaxis()
ax.set_title('Visualizing to Cells')
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.show()
