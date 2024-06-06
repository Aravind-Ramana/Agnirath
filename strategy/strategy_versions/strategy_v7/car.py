import numpy as np

# Import necessary constants and variables from the config module
from config import (
    Mass, ZeroSpeedCrr, AirDensity, CDA, R_Out, Ta,
    GravityAcc,
)

EPSILON = 10**-8  # Small value to avoid division by zero

# Precomputed constants based on imported configuration values
_frictional_tou = R_Out * Mass * GravityAcc * ZeroSpeedCrr
_drag_coeff = 0.5 * CDA * AirDensity * (R_Out ** 3)
_drag_coeff_wR2 = _drag_coeff / R_Out**2
_slope_coeff = Mass * GravityAcc
_windage_losses_coeff_wR2 = (170.4 * (10**-6)) / (R_Out **2)

def calculate_power(speed, acceleration, slope):
    """
    Calculate the net power consumption and output power based on speed, acceleration, and slope.

    Parameters:
    speed (numpy.ndarray): Array of speeds.
    acceleration (numpy.ndarray): Array of accelerations.
    slope (numpy.ndarray): Array of slopes.

    Returns:
    tuple: Net power consumption and output power.
    """
    speed2 = speed ** 2  # Square of speed

    # Calculate drag torque
    drag_tou = _drag_coeff_wR2 * speed2
    tou = _frictional_tou + drag_tou
    
    # Initial winding temperature
    Tw_i = Ta

    while True:
        # Magnetic remanence calculation
        B = 1.6716 - 0.0006 * (Ta + Tw_i)
        # RMS phase current
        i = 0.561 * B * tou

        # Resistance of windings as a function of temperature
        resistance = 0.00022425 * Tw_i - 0.00820525
        
        # Copper (ohmic) losses
        Pc = 3 * i ** 2 * resistance
        # Eddy current losses
        Pe = (9.602 * (10**-6) * ((B / R_Out) ** 2) / resistance) * speed2
        # Calculate new winding temperature
        Tw = 0.455 * (Pc + Pe) + Ta
    
        # Check if temperature has converged
        cond = np.abs(Tw - Tw_i) < 0.001
        if np.all(cond):
            break

        # Update temperature for the next iteration
        Tw_i = np.where(cond, Tw_i, Tw)

    # Calculate output power
    P_out = tou * speed / R_Out
    # Calculate windage losses
    Pw = speed2 * _windage_losses_coeff_wR2

    # Calculate power due to acceleration and slope
    P_acc = (Mass * acceleration + _slope_coeff * np.sin(np.radians(slope))) * speed

    # Calculate net power consumption
    P_net = P_out + Pw + Pc + Pe + P_acc

    # Return net power (clipped to be non-negative) and output power
    return P_net.clip(0), P_out

def calculate_dt(start_speed, stop_speed, dx):
    """
    Calculate the time intervals between segments based on start and stop speeds.

    Parameters:
    start_speed (numpy.ndarray): Array of starting speeds for each segment.
    stop_speed (numpy.ndarray): Array of stopping speeds for each segment.
    dx (numpy.ndarray): Array of distances for each segment.

    Returns:
    numpy.ndarray: Array of time intervals for each segment.
    """
    dt = 2 * dx / (start_speed + stop_speed + EPSILON)  # Calculate time intervals
    return dt
