import numpy as np
from itertools import product
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

atm = 101325
g = 9.81
R = 8.315


# air density in kg/m^3
def air_density(altitude=500, T=293):
    L = 0.0065
    T0 = 298
    M = 0.02896
    Rs = 287.058
    p_exp = M*g/(R*L)
    p = atm*(1-(L*altitude/T0))**p_exp
    return p/(Rs*T)

# resisting force from air
def F_air(mph, CdA, rho=air_density()):
    speed = mph/2.237
    return 0.5 * CdA * rho * speed**2

def F_roll(grad, m, Crr):
    return Crr * np.cos(np.arctan(grad)) * m * g

def F_grav(grad, m):
    return np.sin(np.arctan(grad)) * m * g


def P_needed(mph, grad, m, CdA, Crr, rho, L_dt=0.051):
    speed = mph/2.237 # convert to m/s
    F_resist = F_air(mph, CdA, rho) + F_roll(grad, m, Crr) + F_grav(grad, m)
    return F_resist * speed / (1.0-L_dt)

def Wperkg(body_mass, bike_mass, mph, grad, CdA=0.45, Crr=0.00483, rho=air_density()):
    W = P_needed(mph, grad, body_mass+bike_mass, CdA, Crr, rho)
    return W / body_mass

mph_vals = np.arange(4,12.1,0.1)
grad_vals = np.arange(0.0, 0.25, 0.03)
df = pd.DataFrame.from_records(data=[p for p in product(mph_vals, grad_vals)], columns=["speed", "gradient"])
# calculate for me and my bike
df['W/kg'] = [Wperkg(63.5, 8.0, a.speed, a.gradient) for a in df.itertuples()]
sns.lineplot(x='speed', y='W/kg', data=df, hue='gradient', palette=sns.cubehelix_palette(len(grad_vals), start=0, rot=.5))
# plus some plot formatting stuff

plt.show()