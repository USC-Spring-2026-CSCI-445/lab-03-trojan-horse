#!/usr/bin/env python3
"""
CSCI 445 Lab 02 - Regression Analysis Tutorial
This script demonstrates how to perform regression on IR sensor data
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ============================================================================
# STEP 1: Enter your calibration data
# ============================================================================

# Example data from the lab (cardboard box measurements)
# Format: [ground_truth_distance (m), mean_raw_sensor_value]
calibration_data_wood = [
    [0.1, 647.2],
    [0.2, 365.0],
    [0.3, 293.0],
    [0.4, 300.0],
    [0.5, 252.4],
    [0.6, 294.4],
    [0.7, 297.6],
]

calibration_data_foam = [
    [0.1, 706.8],
    [0.2, 387.0],
    [0.3, 273.2],
    [0.4, 215.4],
    [0.5, 207.4],
    [0.6, 201.4],
    [0.7, 208.0],
]

calibration_data = calibration_data_wood # change this to foam if you want to view foam

# Separate into arrays
distances = np.array([point[0] for point in calibration_data])  # Ground truth (meters)
raw_values = np.array([point[1] for point in calibration_data])  # Sensor readings

print("=" * 70)
print("REGRESSION ANALYSIS FOR IR DISTANCE SENSOR")
print("=" * 70)
print("\nCalibration Data:")
print(f"{'Distance (m)':<15} {'Raw Sensor Value':<20}")
print("-" * 35)
for dist, raw in zip(distances, raw_values):
    print(f"{dist:<15.2f} {raw:<20.1f}")

# ============================================================================
# STEP 2: Define candidate regression functions
# ============================================================================

def power_law(x, a, b):
    """
    Power law: y = a * x^b
    """
    return a * np.power(x, b)

def inverse_linear(x, a):
    """
    Simple inverse: y = a / x
    """
    return a / x

# ============================================================================
# STEP 3: Perform regression for each function type
# ============================================================================

print("\n" + "=" * 70)
print("REGRESSION RESULTS")
print("=" * 70)

# Fit 1: Power Law (most flexible)
params_power, _ = curve_fit(power_law, raw_values, distances, p0=[100, -1])
a_power, b_power = params_power
print(f"\n1. POWER LAW: distance = a * (raw)^b")
print(f"   Coefficients: a = {a_power:.4f}, b = {b_power:.4f}")

# Fit 2: Simple Inverse
params_inv, _ = curve_fit(inverse_linear, raw_values, distances, p0=[70])
a_inv = params_inv[0]
print(f"\n2. SIMPLE INVERSE: distance = a / raw")
print(f"   Coefficient: a = {a_inv:.4f}")

# ============================================================================
# STEP 4: Evaluate accuracy of each model
# ============================================================================

print("\n" + "=" * 70)
print("MODEL ACCURACY COMPARISON")
print("=" * 70)

# Calculate predictions and errors
predictions_power = power_law(raw_values, a_power, b_power)
predictions_inv = inverse_linear(raw_values, a_inv)

errors_power = distances - predictions_power
errors_inv = distances - predictions_inv

rmse_power = np.sqrt(np.mean(errors_power**2))
rmse_inv = np.sqrt(np.mean(errors_inv**2))

print(f"\nRoot Mean Square Error (RMSE):")
print(f"  Power Law:         {rmse_power:.6f} m")
print(f"  Simple Inverse:    {rmse_inv:.6f} m")

print(f"\nDetailed Predictions (metre):")
print(f"{'True Dist':<12} {'Raw':<8} {'Power Law':<12} {'Simple Inv':<12}")
print("-" * 60)
for i in range(len(distances)):
    print(f"{distances[i]:<12.3f} {raw_values[i]:<8.1f} "
          f"{predictions_power[i]:<12.3f} {predictions_inv[i]:<12.3f}")

# ============================================================================
# STEP 5: Visualize the results
# ============================================================================

print("\n" + "=" * 70)
print("Generating plots...")
print("=" * 70)

# Create smooth curve for visualization
raw_smooth = np.linspace(min(raw_values), max(raw_values), 100)
dist_power_smooth = power_law(raw_smooth, a_power, b_power)
dist_inv_smooth = inverse_linear(raw_smooth, a_inv)
# Plot 1: Distance vs Raw Value with all fits
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.scatter(raw_values, distances, s=100, c='red', marker='o', label='Measured Data', zorder=5)
plt.plot(raw_smooth, dist_power_smooth, 'b-', linewidth=2, label=f'Power Law (RMSE={rmse_power:.4f})')
plt.plot(raw_smooth, dist_inv_smooth, 'g--', linewidth=2, label=f'Simple Inverse (RMSE={rmse_inv:.4f})')
plt.xlabel('Raw Sensor Value', fontsize=12)
plt.ylabel('Distance (m)', fontsize=12)
plt.title('Distance vs Raw Sensor Value\n(Comparison of Regression Models)', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 2: Residual plot (errors)
plt.subplot(1, 2, 2)
plt.scatter(raw_values, errors_power * 100, s=80, c='blue', marker='o', label='Power Law')
plt.scatter(raw_values, errors_inv * 100, s=80, c='green', marker='s', label='Simple Inverse')
plt.axhline(y=0, color='k', linestyle='--', linewidth=1)
plt.xlabel('Raw Sensor Value', fontsize=12)
plt.ylabel('Error (cm)', fontsize=12)
plt.title('Prediction Errors\n(How far off is each model?)', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
# plt.savefig('~/home/regression_analysis.png', dpi=150, bbox_inches='tight')
# print("\nPlot saved to: regression_analysis.png")
plt.show()