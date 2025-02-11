intersections = []

import matplotlib.pyplot as plt

plt.figure(figsize=(5, 5))

no_values = [intersection['no'] for intersection in intersections]
x_values = [intersection['x'] for intersection in intersections]
y_values = [intersection['y'] for intersection in intersections]

plt.scatter(x_values, y_values, color='blue')

for no, x, y in zip(no_values, x_values, y_values):
    plt.text(x, y, str(no), color='red', fontsize=15, ha='center', va='center')

plt.gca().invert_yaxis()
plt.title('Visualizing to Intersections')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
