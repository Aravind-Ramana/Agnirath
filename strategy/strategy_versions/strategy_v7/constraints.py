import numpy as np

# Import configuration variables and functions from config and car modules
from config import BatteryCapacity, DeepDischargeCap, MaxVelocity, Mass, MaxCurrent, BusVoltage, InitialBatteryCapacity
from car import calculate_dt, calculate_power
from solar import calculate_incident_solarpower

# Safe battery level is calculated based on BatteryCapacity and DeepDischargeCap
SafeBatteryLevel = BatteryCapacity * DeepDischargeCap
# Maximum power the system can handle is calculated based on MaxCurrent and BusVoltage
MaxPower = MaxCurrent * BusVoltage

# Function to get the bounds for the velocity profile
def get_bounds(N):
    """
    Generate bounds for the velocity profile.
    
    Parameters:
    N (int): The number of segments in the velocity profile.
    
    Returns:
    list: A list of tuples representing the bounds for each segment.
          The bounds are (0, 0) for the first and last segment, and (0.01, MaxVelocity) for the others.
    """
    return [(0, 0)] + [(0.01, MaxVelocity)] * (N - 2) + [(0, 0)]

# Objective function to minimize the total time taken
def objective(velocity_profile, segment_array):
    """
    Calculate the objective function, which is the total time taken for the given velocity profile.

    Parameters:
    velocity_profile (numpy.ndarray): Array of velocities at each segment.
    segment_array (numpy.ndarray): Array of distances for each segment.
    
    Returns:
    float: The total time taken for the trip.
    """
    dt = calculate_dt(velocity_profile[:-1], velocity_profile[1:], segment_array)
    return np.sum(dt)

# Constraint function for battery and acceleration
def battery_acc_constraint_func(v_prof, segment_array, slope_array, latitude_array, longitude_array):
    """
    Constraint function that ensures battery levels remain safe and checks for acceleration limits.
    
    Parameters:
    v_prof (numpy.ndarray): Array of velocities at each segment.
    segment_array (numpy.ndarray): Array of distances for each segment.
    slope_array (numpy.ndarray): Array of slope angles for each segment.
    latitude_array (numpy.ndarray): Array of latitudes for each segment.
    longitude_array (numpy.ndarray): Array of longitudes for each segment.
    
    Returns:
    tuple: Minimum battery level, maximum power over mass*velocity - acceleration,
           (MaxPower - max power consumption (commented out)).
    """
    start_speeds, stop_speeds = v_prof[:-1], v_prof[1:]
    
    # Calculate average speed for each segment
    avg_speed = (start_speeds + stop_speeds) / 2
    # Calculate time intervals between segments
    dt = calculate_dt(start_speeds, stop_speeds, segment_array)
    # Calculate acceleration for each segment
    acceleration = (stop_speeds - start_speeds) / dt

    # Calculate power consumption and power output due to the vehicle movement
    P, PO = calculate_power(avg_speed, acceleration, slope_array)
    # Calculate solar power incident on the vehicle
    SolP = calculate_incident_solarpower(dt.cumsum(), latitude_array, longitude_array)

    # Calculate energy consumption and the battery profile
    energy_consumption = ((P - SolP) * dt).cumsum() / 3600
    battery_profile = InitialBatteryCapacity - energy_consumption - SafeBatteryLevel

    # Return the minimum battery level, maximum power usage related to acceleration,
    # and the commented out part for maximum power constraint
    return np.min(battery_profile), np.max(PO.clip(0) / (Mass * avg_speed) - acceleration)
# , MaxPower - np.max(P)
