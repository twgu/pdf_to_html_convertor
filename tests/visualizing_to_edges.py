edges = []

import matplotlib.pyplot as plt

plt.figure(figsize=(5, 5))

for edge in edges:
    no = edge['no']
    x0, y0 = edge['x0'], edge['y0']
    x1, y1 = edge['x1'], edge['y1']

    x_coords = [x0, x1]
    y_coords = [y0, y1]

    plt.plot(x_coords, y_coords, marker='o')

    center_x = (x0 + x1) / 2
    center_y = (y0 + y1) / 2

    plt.text(center_x, center_y, str(no), color='red', fontsize=15, ha='center', va='center')

plt.gca().invert_yaxis()
plt.title('Visualizing to Edges')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
