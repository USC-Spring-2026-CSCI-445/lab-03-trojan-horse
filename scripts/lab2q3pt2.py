import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

distances = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]

wood_readings = {
    0.1: [656, 648, 642, 653, 637],
    0.2: [357,364 ,358 ,382 ,364 ],
    0.3: [282, 290, 300, 310, 283],
    0.4: [296, 288, 288, 339, 289],
    0.5: [248, 267, 250, 248, 249],
    0.6: [294, 297, 293, 293, 295],
    0.7: [297, 282, 322, 288, 299],
}

foam_readings = {
    0.1: [705, 707, 710, 706, 706],
    0.2: [389, 387, 386, 388, 385],
    0.3: [270, 271 ,277 ,272 , 276],
    0.5: [208,209 ,207 ,206 ,207 ],
    0.4: [225,228 ,208 , 209, 207 ],
    0.6: [200, 201, 204, 200, 202],
    0.7: [206, 208, 212, 207, 207],
}

print("WOOD")
print("Distance | Mean | Std Dev | Measurements")
for d in distances:
    r = wood_readings[d]  #print out mean and standard dev
    m = np.mean(r)
    s = np.std(r, ddof=1)
    print(f"{d} m | {m:.1f} | {s:.2f} | {r}")

print("\nWHITE TURTLEBOT BOX")
print("Distance | Mean | Std Dev | Measurements")
for d in distances:
    r = foam_readings[d]
    m = np.mean(r)
    s = np.std(r, ddof=1)
    print(f"{d} m | {m:.1f} | {s:.2f} | {r}")

wood_means = np.array([np.mean(wood_readings[d]) for d in distances]) #an array of the means
foam_means = np.array([np.mean(foam_readings[d]) for d in distances])
distances_array = np.array(distances) #an array of the distances

wood_all = [v for vals in wood_readings.values() for v in vals] #puts all readings into a single list
foam_all = [v for vals in foam_readings.values() for v in vals]

plt.figure(figsize=(8, 6))
plt.plot(distances, wood_means, 'o-', linewidth=2, markersize=8, label='Wood block')
plt.plot(distances, foam_means, 'o-', linewidth=2, markersize=8, label='Foam')
plt.xlabel('distance [m]') #plotting distance vs measurement
plt.ylabel('measurement')
plt.title('Distance vs Measurement value')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('distance_vs_measurement.png', dpi=300)
plt.show()

def exponential(x, a, b): 
    return a * (x ** b) #using exponential

wood_params, _ = curve_fit(exponential, wood_means, distances_array) #finds the parameters for wood and foam of best fit
foam_params, _ = curve_fit(exponential, foam_means, distances_array)

a_wood, b_wood = wood_params
a_foam, b_foam = foam_params

print(f"\nWood: distance = {a_wood} * (raw ** {b_wood})")
print(f"Foam: distance = {a_foam} * (raw ** {b_foam})")

x_fit = np.linspace(min(min(wood_means), min(foam_means)), #used for drawing smooth curve
                     max(max(wood_means), max(foam_means)), 200)
wood_fit = exponential(x_fit, a_wood, b_wood) #finds predicted distances
foam_fit = exponential(x_fit, a_foam, b_foam)

plt.figure(figsize=(10, 6))
plt.scatter(wood_means, distances_array, s=80, label='Wood data', color='brown', zorder=3) #plotting everything
plt.scatter(foam_means, distances_array, s=80, label='Foam data', color='lightblue', zorder=3)
plt.plot(x_fit, wood_fit, '-', linewidth=2, label=f'Wood fit', color='darkred')
plt.plot(x_fit, foam_fit, '-', linewidth=2, label=f'Foam fit', color='blue')
plt.xlabel('measurement (unitless)')
plt.ylabel('distance [m]')
plt.title('Measurement to Distance Regression')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('regression.png', dpi=300)
plt.show()