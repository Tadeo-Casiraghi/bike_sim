import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

with open('data.csv','r') as file:
    lines = file.readlines()

x = []
y = []

for line in lines:
    sepx, sepy = line.strip().split(',')
    x.append(float(sepx))
    y.append(float(sepy))

difer = y[0] - y[-1]

X = x+[359, 360]+list(np.array(x) + 360)
Y = y+[difer*i/3 + y[-1] for i in range(1,3)]+y
yhat = savgol_filter(Y, 51, 3) # window size 51, polynomial order 3

good_x = X[0:360]
good_y = yhat[0:360]

plt.scatter(X,Y)
plt.scatter(X,yhat, color='red')

plt.figure()
plt.plot(good_x, good_y)

with open('processed.csv','w') as file:
    file.write('Angle,Torque\n')
    for Xx, Yy in zip(good_x, good_y):
        file.write(f'{Xx},{Yy}\n')

sumer = 200

ppairs = [[[good_x[0]],[good_y[0]+sumer]]]
npairs = []
pos = True
for xval, yval in zip(good_x[1:],good_y[1:]):
    if pos and yval < 0:
        pos = False
        npairs.append([[xval],[-yval+sumer]])
    elif pos:
        ppairs[-1][0].append(xval)
        ppairs[-1][1].append(yval+sumer)
    elif not pos and yval > 0:
        pos = True
        ppairs.append([[xval],[yval+sumer]])
    else:
        npairs[-1][0].append(xval)
        npairs[-1][1].append(-yval+sumer)


fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)

for pair in ppairs:
    ax.plot(np.array(pair[0])*np.pi/180, pair[1], 'b')
for pair in npairs:
    ax.plot(np.array(pair[0])*np.pi/180, pair[1], 'r')

ax.plot(np.linspace(0,2*np.pi,100), [sumer]*100, 'k')

plt.show()