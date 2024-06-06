import numpy as np

from config import InitialBatteryCapacity, BatteryCapacity
from car import calculate_dt, calculate_power
from solar import calculate_incident_solarpower

def extract_profiles(velocity_profile, segment_array, slope_array, lattitude_array, longitude_array):
    """
    Extract various profiles including distance, velocity, acceleration, battery, energy consumption, 
    energy gain, and cumulative time from the given input arrays.
    
    Parameters:
    velocity_profile (numpy.ndarray): Array of velocities.
    segment_array (numpy.ndarray): Array of segment distances.
    slope_array (numpy.ndarray): Array of slopes.
    lattitude_array (numpy.ndarray): Array of latitudes.
    longitude_array (numpy.ndarray): Array of longitudes.
    
    Returns:
    list: A list containing arrays of distances, velocity profile, acceleration, battery profile,
          energy consumption, energy gain, and cumulative time.
    """
    # Calculate start and stop speeds
    start_speeds, stop_speeds = velocity_profile[:-1], velocity_profile[1:]
    
    # Calculate average speed and time intervals (dt)
    avg_speed = (start_speeds + stop_speeds) / 2
    dt = calculate_dt(start_speeds, stop_speeds, segment_array)
    
    # Calculate acceleration
    acceleration = (stop_speeds - start_speeds) / dt

    # Calculate power and solar power
    P, _ = calculate_power(avg_speed, acceleration, slope_array)
    SolP = calculate_incident_solarpower(dt.cumsum(), lattitude_array, longitude_array)

    # Calculate energy consumption and energy gain
    energy_consumption = P * dt / 3600
    energy_gain = SolP * dt / 3600

    # Calculate net energy profile
    net_energy_profile = energy_consumption.cumsum() - energy_gain.cumsum()
    
    # Calculate battery profile
    battery_profile = InitialBatteryCapacity - net_energy_profile
    battery_profile = np.concatenate((np.array([InitialBatteryCapacity]), battery_profile))

    # Convert battery profile to percentage
    battery_profile = battery_profile * 100 / BatteryCapacity

    # Calculate cumulative distances
    distances = np.append([0], segment_array.cumsum())

    # Return the extracted profiles as a list of arrays
    return [
        distances,
        velocity_profile,
        np.concatenate((np.array([np.nan]), acceleration)),
        battery_profile,
        np.concatenate((np.array([np.nan]), energy_consumption)),
        np.concatenate((np.array([np.nan]), energy_gain)),
        np.concatenate((np.array([0]), dt.cumsum())),
    ]
