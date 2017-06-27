import ast
import matplotlib.pyplot as plt
import numpy as np


file = open('Gen8_1-Dist_vs_E.txt', 'r')
for line in file:
    dist_v_energy = ast.literal_eval(line)
x, y = [], []
for ele in dist_v_energy:
    x.append(float(ele[0]))
    y.append(float(ele[1]))
plt.title('Gen 8_1')
plt.plot(x,y, 'bo')
plt.show()

