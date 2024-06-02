import numpy as np
import math
from datetime import datetime
from config import PanelArea, PanelEfficiency, RaceStartTime, RaceEndTime

# Constants
G_s = 1366  # Solar constant in W/m^2
G_s_prime = 0.7 * G_s  # Adjusted solar constant for clear day
_power_coeff = PanelArea * PanelEfficiency
DT = RaceEndTime - RaceStartTime  # Duration of the race in seconds

# Function to calculate the nth day of the year
def day_of_year(date):
    """
    Calculate the day of the year for a given date.
    
    Parameters:
    date (datetime): The date for which the day of the year is calculated.
    
    Returns:
    int: The day of the year.
    """
    return date.timetuple().tm_yday

# Function to calculate B
def calculate_B(N):
    """
    Calculate the parameter B used in the equation of time.
    
    Parameters:
    N (int): The day of the year.
    
    Returns:
    float: The parameter B.
    """
    return (N - 1) * 360 / 365

# Function to calculate the equation of time (E)
def equation_of_time(B):
    """
    Calculate the equation of time (E).
    
    Parameters:
    B (float): The parameter B.
    
    Returns:
    float: The equation of time in minutes.
    """
    return 229.2 * (0.00018865 * math.cos(math.radians(B)) - 0.0032077 * math.sin(math.radians(B)) +
                    0.041016 * math.cos(math.radians(2 * B)) - 0.048093 * math.sin(math.radians(2 * B)))

# Function to calculate solar local time (T_s)
def solar_local_time(standard_time, longitude, standard_meridian, E):
    """
    Calculate the solar local time (T_s).
    
    Parameters:
    standard_time (float): The standard time in hours (decimal).
    longitude (numpy.ndarray): Array of longitudes.
    standard_meridian (numpy.ndarray): Array of standard meridians.
    E (float): The equation of time in minutes.
    
    Returns:
    numpy.ndarray: Array of solar local times.
    """
    return standard_time + (4 * (standard_meridian - longitude) + E) / 60

# Function to calculate hour angle (ω)
def hour_angle(T_s):
    """
    Calculate the hour angle (ω).
    
    Parameters:
    T_s (numpy.ndarray): Array of solar local times.
    
    Returns:
    numpy.ndarray: Array of hour angles.
    """
    return 15 * (T_s - 12)

# Function to calculate sun declination angle (δ)
def sun_declination_angle(N):
    """
    Calculate the sun declination angle (δ).
    
    Parameters:
    N (int): The day of the year.
    
    Returns:
    float: The sun declination angle in degrees.
    """
    return 23.45 * math.sin(math.radians(360 / 365 * (284 + N)))

# Function to calculate solar irradiance (G_b)
def solar_irradiance(G_s_prime, latitude, declination, hour_angle):
    """
    Calculate the solar irradiance (G_b).
    
    Parameters:
    G_s_prime (float): The adjusted solar constant.
    latitude (numpy.ndarray): Array of latitudes.
    declination (float): The sun declination angle in degrees.
    hour_angle (numpy.ndarray): Array of hour angles.
    
    Returns:
    numpy.ndarray: Array of solar irradiance values.
    """
    latitude_rad = np.radians(latitude)
    declination_rad = np.radians(declination)
    hour_angle_rad = np.radians(hour_angle)
    return G_s_prime * (np.cos(latitude_rad) * np.cos(declination_rad) * np.cos(hour_angle_rad) + np.sin(latitude_rad) * np.sin(declination_rad))

# Function to calculate solar irradiance based on time
def _calc_solar_irradiance(time):
    """
    Calculate the solar irradiance based on a specific time using a Gaussian distribution.
    
    Parameters:
    time (float): The time in seconds since the start of the race.
    
    Returns:
    float: The solar irradiance.
    """
    return 1073.099 * np.exp(-0.5 * ((time - 51908.735) / 11484.950)**2)

# Main function to calculate incident solar power
def calculate_incident_solarpower(globaltime, latitude_array, longitude_array):
    """
    Calculate the incident solar power based on time, latitude, and longitude.
    
    Parameters:
    globaltime (numpy.ndarray): Array of global times in seconds.
    latitude_array (numpy.ndarray): Array of latitudes.
    longitude_array (numpy.ndarray): Array of longitudes.
    
    Returns:
    numpy.ndarray: Array of incident solar power values.
    """
    # Assume a fixed date for simplicity, can be changed as needed
    date = datetime.now()
    time = datetime.now()

    # Calculate the day of the year
    N = day_of_year(date)
    B = calculate_B(N)

    # Calculate the standard meridian
    standard_meridian = 15 * (longitude_array / 15).astype(int)

    # Calculate the equation of time
    E = equation_of_time(B)

    # Calculate the standard time in hours (decimal)
    standard_time = time.hour + time.minute / 60

    # Calculate the solar local time for each point
    T_s = solar_local_time(standard_time, longitude_array, standard_meridian, E)

    # Calculate the hour angle for each point
    omega = hour_angle(T_s)

    # Calculate the sun declination angle
    delta = sun_declination_angle(N)

    # Calculate the solar irradiance for each point
    G_b = solar_irradiance(G_s_prime, latitude_array, delta, omega)

    # Adjust for the specific time of day
    gt = globaltime % DT
    intensity = _calc_solar_irradiance(RaceStartTime + gt)
    
    return intensity * _power_coeff
