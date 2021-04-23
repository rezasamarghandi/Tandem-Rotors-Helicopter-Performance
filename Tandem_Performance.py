#Author: Reza Samarghandi
#
#Email: RezaSamarghandi@yahoo.com

import numpy as np
import math
import matplotlib.pyplot as plt

minvel = float(input("Minimum True Airspeed For Analysis (kts) : "))
maxvel = float(input("Maximum True Airspeed For Analysis (kts) : "))
velocity = np.arange(minvel, maxvel + 1, 1)
alfa_deg = float(input("Angle Of Attack (Degrees): "))
alfa = alfa_deg * math.pi / 180  # angle of attack (rad)
velct = float(input("Climb Velocity (kts) : "))
velc = velct * 1.6878  # Climb Velocity in (ft/s)
rho = float(input("Density Of Air in (lbs/ft^3) : "))
m = float(input("Mass Of The Helicopter in (lbs) : "))
r = float(input("Radius Of The Rotor Blade (ft) : "))
chord = float(input("Chord Of The Rotor Blade (ft) : "))
nb = float(input("Number Of Blades Of Rotor : "))
cd0 = float(input("Rotor Blade Airfoil Drag Coefficient in Zero Angle Of Attack (cd0) : "))
g = 32.17  # Gravitational Acceleration
rpm = float(input("RPM of The Rotor : "))
hpavt = float(input("Available power in hourse power : "))

hpav = hpavt / 2
Pav = hpav * 17696  # Available Power in (lb*ft^2/s^3)
mft = float(input("fuel mass (lbs) : "))
mf = mft / 2
sfchp = float(input("specific fuel consumption (lb/(hp*h) : "))
sfc = sfchp / 17696
n = float(input("Load Factor For Turn Radius (Use Maximum Load Factor To Find Minimum Turn Radius) : "))
f = float(input("Equivalent Flat Plate Area Of The Fuselage (ft^2) : "))
k = float(input("Induced power factor (Preferred Value is 1.15) : "))
kk = float(input("Correction parameter (Preferred Value is 4.7) : "))
ss = float(input("Distance Between Two Rotors (ft) : "))

d = 2 * r  # Diameter Of The Rotor
mp = 2 / math.pi * (math.acos(ss / d) - ss / d * math.sin(math.acos(ss / d)))
kov = 1 + (math.sqrt(2) - 1) * mp  # Induced Power Factor Due To Rotors Overlap

omega = rpm * 2 * math.pi / 60  # Main Rotor Rotational Speed (rad/s)
vtip = r * omega  # Main Rotor Blade Tip Speed (ft/s)
a = math.pi * r ** 2  # Area of The Main Rotor (ft^2)
sigma = nb * chord / (math.pi * r)  # Solidity of The Main Rotor
w = m * g  # Weight of The Helicopter (lb*ft/s^2)
cw = w / (rho * a * vtip ** 2)  # Coefficient of Weight

shp = 17696  # hp to (lb*ft^2/s^3)
Pc = w * velc  # Climb Power (lb*ft^2/s^3)
hpc = Pc / shp  # Climb Power (hp)
cpc = Pc / (rho * a * vtip ** 3)  # Climb Power Coefficient

descends = []
endurances = []
rangs = []
rcs = []
lds = []
radiuss = []
hpis = []
hp0s = []
hpps = []
hps = []
hpavs = []
for j in range(len(velocity)):
    v = velocity[j] * 1.6878  # Forward Velocity in ft / s

    miu = v * math.cos(alfa) / vtip  # Main Rotor Advance Ratio

    landa = math.sqrt(cw / 2)  # Initial Guess Of The Rotor Inflow Ratio
    err = 1
    while err <= 0.01:
        landa_old = landa
        landa = miu * math.tan(alfa) + cw / (2 * math.sqrt(miu ** 2 + landa ** 2))  # Rotor Inflow Ratio
        err = landa - landa_old

    cpi = (2 * kov * k * cw ** 2) / (2 * math.sqrt(miu ** 2 + landa ** 2))  # Rotor Induced Power Coefficient
    cp0 = 2 * sigma * cd0 / 8 * (1 + kk * miu ** 2)  # Rotor Profile Power Coefficient
    cpp = 0.5 * f / a * miu ** 3  # Parasite Power Coefficient Of The Helicopter
    cp = cpi + cp0 + cpp + cpc  # Total Required Power Coefficient
    Pi = cpi * rho * a * vtip ** 3  # Rotor Induced Power
    P0 = cp0 * rho * a * vtip ** 3  # Rotor Profile Power
    Pp = cpp * rho * a * vtip ** 3  # Parasite Power Of The Helicopter
    P = Pi + P0 + Pp + Pc  # Total Required Power
    hpi = Pi / shp  # Induced Power In HP
    hp0 = P0 / shp  # Profile Power In HP
    hpp = Pp / shp  # Parasite Power In HP
    hp = P / shp  # Total Required Power In HP

    descend = -cp / cw * vtip * 60  # Autorotation Rate Of Descend (ft / min)
    descends.append(descend)
    endurance = mf / (P * sfc)  # Endurance Of The Helicopter (Hour)
    endurances.append(endurance)
    rang = mf * v / (P * sfc / 3600)  # Range Of The Helicopter (ft)
    rangs.append(rang)
    rc = (Pav - P) / w  # Rate Of Climb (ft / s)
    rcs.append(rc)
    ld = w * v / P  # L / D Of The Helicopter
    lds.append(ld)
    radius = v ** 2 / (math.sqrt(n ** 2 - 1) * g)  # Turn Radius For specific Load Factor
    radiuss.append(radius)
    
    hpis.append(hpi)
    hp0s.append(hp0)
    hpps.append(hpp)
    hps.append(hp)
    hpavs.append(hpav)
    
plt.figure()
plt.plot(velocity, hpis, 'g', label='Induced Power')
plt.plot(velocity, hp0s, 'b', label='Profile Power')
plt.plot(velocity, hpps, 'c', label='Parasite Power')
plt.plot(velocity, hps, 'm', label='Total Required Power')
plt.plot(velocity, hpavs, 'k', label='Avaiable Power')
plt.title('Power Curve')
plt.xlabel('True Airspeed (kts)')
plt.ylabel('Power (hp)')
plt.legend()
plt.show()


plt.figure()
plt.plot(velocity, descends)
plt.title('Autorotation Descend Rate')
plt.xlabel('True Airspeed (kts)')
plt.ylabel('Descend Rate (ft/min)')
plt.show()

plt.figure()
plt.plot(velocity, lds)
plt.title('Lift to Drag Ratio vs Airspeed')
plt.xlabel('True Airspeed (kts)')
plt.ylabel('L/D')
plt.show()

plt.figure()
plt.plot(velocity, rcs)
plt.title('Rate Of Climb')
plt.xlabel('True Airspeed (kts)')
plt.ylabel('Rate of Climb (ft/s)')
plt.show()

plt.figure()
plt.plot(velocity, rangs)
plt.title('Range Of The Helicopter')
plt.xlabel('True Airspeed (kts)')
plt.ylabel('Range (ft)')
plt.show()

plt.figure()
plt.plot(velocity, endurances)
plt.title('Endurance Of The Helicopter')
plt.xlabel('True Airspeed (kts)')
plt.ylabel('Endurance (hour)')
plt.show()

plt.figure()
plt.plot(velocity, radiuss)
plt.title('Turn Radius')
plt.xlabel('True Airspeed (kts)')
plt.ylabel('Turn Radius (ft)')
plt.show()
