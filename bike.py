import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('processed.csv')
x = data.Angle.to_list()
y = data.Torque.to_list()

plt.figure()
plt.plot(x, np.array(y) + np.array(y[180:] + y[:180]))
plt.show()