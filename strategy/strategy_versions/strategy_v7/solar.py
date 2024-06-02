import numpy as np

from config import PanelArea, PanelEfficiency, RaceStartTime, RaceEndTime

# Constants
DT = RaceEndTime - RaceStartTime  # Duration of the race in seconds
_power_coeff = PanelArea * PanelEfficiency  # Coefficient for power calculation based on panel area and efficiency

def _calc_solar_irradiance(time):
    """
    Calculate the solar irradiance based on a specific time using a Gaussian distribution.
    
    Parameters:
    time (float): The time in seconds since the start of the race.
    
    Returns:
    float: The solar irradiance in W/m^2.
    """
    return 1073.099 * np.exp(-0.5 * ((time - 51908.735) / 11484.950)**2)

def calculate_incident_solarpower(globaltime, latitude, longitude):
    """
    Calculate the incident solar power based on the global time, latitude, and longitude.
    
    Parameters:
    globaltime (float): The global time in seconds.
    latitude (float): The latitude of the location.
    longitude (float): The longitude of the location.
    
    Returns:
    float: The incident solar power in watts.
    """
    # Calculate the time within the race duration
    gt = globaltime % DT
    
    # Calculate the solar irradiance at the specific time
    intensity = _calc_solar_irradiance(RaceStartTime + gt)
    
    # Calculate and return the incident solar power
    return intensity * _power_coeff
