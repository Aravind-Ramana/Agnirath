
# Model Settings
ModelMethod = "COBYLA"
InitialGuessVelocity =25

RaceStartTime = 9 * 3600  # 9:00 am
RaceEndTime = (12 + 5) * 3600  # 5:00 pm

# ---------------------------------------------------------------------------------------------------------
# Car Data

# Battery
BatteryCapacity = 3055 # Wh
DeepDischargeCap = 0.2 
InitialBatteryCapacity = BatteryCapacity * 0.36  # Wh

# Physical Attributes
R_In = 0.214  # Inner radius of wheel
R_Out = 0.2785  # Outer radius of wheel
Mass = 260  # kg
Wheels = 3
StatorRotorAirGap = 1.5 * 10**-3

# Resistive Coeff
ZeroSpeedCrr = 0.0045
Cd = 0.092  # Coefficient of Drag
FrontalArea = 1  # m^2
CDA = Cd * FrontalArea  # Efficetive CDA

# Solar Panel Data
PanelArea = 6  # m^2
PanelEfficiency = 0.19

# Bus Voltage
BusVoltage = 4.2 * 38  # V

# ---------------------------------------------------------------------------------------------------------
# Physical Constants
AirDensity = 1.192  # kg/m^3
g = GravityAcc = 9.81  # m/s^2
AirViscosity = 1.524 * 10**-5  # Pa s (Kinematic viscosity of air)
Ta = 295  # K (Ambient Temperature)

# ---------------------------------------------------------------------------------------------------------
# Car Constraints
MaxVelocity = 35 # m/s
MaxCurrent = 12.3  # Am