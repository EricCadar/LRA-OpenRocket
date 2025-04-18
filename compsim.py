from rocketpy import Environment, SolidMotor, Rocket, Flight
from rocketpy import Function
import numpy as np
import pandas as pd

import requests
import json
from scipy.interpolate import interp1d
#env = Environment(latitude=32.990254, longitude=-106.974998, elevation=1400)

import datetime

#Location + Key
latitude = 30.2849
longitude = -97.7341
windy_api_key = "nmFllby1i6VwIRg79M6TLBp8ScsZUxz1"

def get_windy_forecast(lat, lon, key):
    url = f"https://api.windy.com/api/point-forecast/v2"
    headers = {"Content-Type": "application/json", "Authorization": key}
    body = {
        "lat": lat,
        "lon": lon,
        "model": "gfs",
        "parameters": ["wind", "temp", "pressure"],
        #Pressure Levels
        "levels": ["surface", "1000h", "950h", "925h", "900h", "850h", "800h", "700h", "600h", "500h", "400h", "300h", "200h", "150h"],
        "key": key
    }
    response = requests.post(url, json=body, headers=headers)
        
    data = response.json()
    #print(json.dumps(data, indent=2))
    
    #Getting TimeStamp Data
    timestamps = data["ts"]
    time_values = [datetime.datetime.fromtimestamp(ts/1000, datetime.UTC) for ts in timestamps]
    
    #Storing Data at Each Level
    level_data = {}
    
    #Processing Levels to Correspond with heights
    for level in body["levels"]:
        #Check is parameters exist at this level
        if f"wind_u-{level}" in data and f"wind_v-{level}" in data and f"temp-{level}" in data:
            level_data[level] = {
                "wind_u": data[f"wind_u-{level}"][0],
                "wind_v": data[f"wind_v-{level}"][0],
                "temp": data[f"temp-{level}"][0],
            }
            
            if level == "surface":
                level_data[level]["altitude"] = 0
            else:
                #Correspond pressure levels with altitude (approximated)
                pressure_heights = {
                    "1000h": 100,
                    "950h": 500,
                    "925h": 800,
                    "900h": 1000,
                    "850h": 1500,
                    "800h": 2000,
                    "700h": 3000,
                    "600h": 4200,
                    "500h": 5500,
                    "400h": 7000,
                    "300h": 9000,
                    "200h": 12000,
                    "150h": 13500
                }
                level_data[level]["altitude"] = pressure_heights.get(level, 0)
    
    # Create organized arrays for altitude and corresponding values
    altitudes = []
    wind_u_values = []
    wind_v_values = []
    temp_values = []
    
    for level, val in level_data.items():
        altitudes.append(val["altitude"])
        wind_u_values.append(val["wind_u"])
        wind_v_values.append(val["wind_v"])
        temp_values.append(val["temp"])
    
    #Sort variables by altitude
    altitude_data = sorted(zip(altitudes, wind_u_values, wind_v_values, temp_values))
    sorted_altitudes, sorted_wind_u, sorted_wind_v, sorted_temp = zip(*altitude_data)
    
    return {
        "time": time_values[0],  # Using first forecast time
        "altitudes": sorted_altitudes,
        "wind_u": sorted_wind_u,
        "wind_v": sorted_wind_v,
        "temp": sorted_temp
    }

#Getting Data from Windy API
forecast_data = get_windy_forecast(lat=latitude, lon=longitude, key=windy_api_key)

#Create the interpolation functions
wind_u_interpolator = interp1d(
    forecast_data["altitudes"], 
    forecast_data["wind_u"], 
    kind='linear', 
    bounds_error=False, 
    fill_value=(forecast_data["wind_u"][0], forecast_data["wind_u"][-1])
)

wind_v_interpolator = interp1d(
    forecast_data["altitudes"], 
    forecast_data["wind_v"], 
    kind='linear', 
    bounds_error=False, 
    fill_value=(forecast_data["wind_v"][0], forecast_data["wind_v"][-1])
)

temp_interpolator = interp1d(
    forecast_data["altitudes"], 
    forecast_data["temp"], 
    kind='linear', 
    bounds_error=False, 
    fill_value=(forecast_data["temp"][0], forecast_data["temp"][-1])
)


def wind_u_func(h):
    if hasattr(h, "__len__"):
        #Array Input
        return float(wind_u_interpolator(h))
    else:
        #Scalar Input
        return float(wind_u_interpolator(float(h)))

def wind_v_func(h):
    if hasattr(h, "__len__"):
        return float(wind_v_interpolator(h))
    else:
        return float(wind_v_interpolator(float(h)))

def temperature_func(h):
    if hasattr(h, "__len__"):
        return float(temp_interpolator(h)) + 273.15
    else:
        return float(temp_interpolator(float(h))) + 273.15

#Approximating Pressure from Height
def calculate_pressure(h):
    p0 = 101325  #sea level P
    T0 = 288.15  #sea level temp (K)
    g = 9.80665  #Gravity
    M = 0.0289644  #molar mass of air
    R = 8.31447  #gas constant
    
    #formula for pressure at given altitude
    return p0 * np.exp((-g * M * h) / (R * T0))

pressure_func = Function(lambda h: calculate_pressure(h) if hasattr(h, "__len__") else calculate_pressure(float(h)))

# Set forecast time
forecast_time = forecast_data["time"]

#Setting Up Environment
env = Environment(
    latitude=latitude,
    longitude=longitude,
    elevation=150  #Height of Launch site
)

env.set_atmospheric_model(
    type="custom_atmosphere",
    wind_u=wind_u_func,
    wind_v=wind_v_func,
    temperature=temperature_func,
    pressure=pressure_func
)

env.set_date((forecast_time.year, forecast_time.month, forecast_time.day, forecast_time.hour))

tomorrow = datetime.date.today() + datetime.timedelta(days=1)

env.set_date(
    (tomorrow.year, tomorrow.month, tomorrow.day, 12)
)  # Hour given in UTC time

env.set_atmospheric_model(type="Forecast", file="GFS")

aerotech = SolidMotor(
    thrust_source="C:/Users/zacht_o13hkk4/Desktop/Simulations/First Rocket/AeroTech_O5500X-PS.csv",
    dry_mass=7.158,
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=.0381,
    grain_number=3, 
    grain_density=1746,
    grain_outer_radius=.0405,
    grain_initial_inner_radius=.01755,
    grain_initial_height=2*.183,
    grain_separation=0,
    grains_center_of_mass_position=.83566,
    center_of_dry_mass_position=0.71,
    nozzle_position=1.496,
    burn_time=4,
    throat_radius=.0169,
    coordinate_system_orientation="combustion_chamber_to_nozzle"
)

'''
#Seymour Motor
seymour=SolidMotor(
    thrust_source="C:/Users/zacht_o13hkk4/Desktop/Simulations/First Rocket/Cesaroni_9977M2245-P.csv",
    dry_mass=,
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=,
    grain_number=, 
    grain_density=,
    grain_outer_radius=,
    grain_initial_inner_radius=,
    grain_initial_height=,
    grain_separation=0,
    grains_center_of_mass_position=,
    center_of_dry_mass_position=,
    nozzle_position=,
    burn_time=,
    throat_radius=.,
    coordinate_system_orientation="combustion_chamber_to_nozzle"
)
'''
#aerotech.draw()

triton = Rocket(
    radius=.0655,
    mass=15.84,
    inertia=(6.41, 6.41, 0.047),
    power_off_drag="C:\\Users\\zacht_o13hkk4\\Desktop\\Simulations\\First Rocket\\powerOffDragCurve.csv",
    power_on_drag="C:\\Users\\zacht_o13hkk4\\Desktop\\Simulations\\First Rocket\\powerOnDragCurve.csv",
    center_of_mass_without_motor=1.5,
    coordinate_system_orientation="nose_to_tail",
)

triton.add_motor(aerotech, position=1.895)

rail_buttons = triton.set_rail_buttons(
upper_button_position=2.72,
lower_button_position=3.1,
angular_position=45
)

nose_cone = triton.add_nose(
    kind="lvhaack",
    length=.686,
    position=0,
    base_radius=.0655
  
)

fin_set = triton.add_trapezoidal_fins(
    n=4,
    span=.117,
    root_chord=.241,
    tip_chord=.0698,
    position=3.01,
    cant_angle=0,
    radius=.0655,
    sweep_length=.171
  
)

tail = triton.add_tail(
    top_radius=.0655,
    bottom_radius=.055,
    length=.127,
    radius=.0655,
    position=3.28
)

main = triton.add_parachute(
    name="main",
    cd_s=1.5*5.896,
    trigger=305

)

drogue = triton.add_parachute(
    name="elliptical",
    cd_s=1.55*.8992,
    trigger="apogee"
)

#env=Environment(latitude= 28.61,longitude= -80.6,elevation= 0.0)

triton.draw()
test_flight = Flight(rocket=triton,environment=env,rail_length=1,inclination=87,heading=0)

#trajectory plots
test_flight.plots.trajectory_3d()

print(test_flight.prints.apogee_conditions())
#Engine info
print(aerotech.info())
#all plots
#test_flight.all_info()