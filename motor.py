import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from rocketpy import Environment, Flight, Function, Rocket, SolidMotor
import pandas as pd
import numpy as np

data_entry = input("If you want to manually enter Rocket Motor info enter 1, If you want to upload a CSV enter 0: ")
data_entry = int(data_entry)
if data_entry == 1:
    print("Make sure you are using metric unit (meters, kg, N)")
    motor_structure_mass = input("Enter the motors mass(kg): ")
    motor_structure_mass_unc = input("Enter the motors mass uncertainty: ")
    burn_time = input("Enter the burn time(s): ")
    burn_time_unc = input("Enter the burn time uncertainty: ")
    nozzle_radius = input("Enter the nozzle radius(m): ")
    nozzle_radius_unc = input("Enter the nozzle radius uncertainty: ")
    throat_radius = input("Enter the throat radius(m): ")
    throat_radius_unc = input("Enter the throat radius uncertainty: ")
    grain_seperation = input("Enter the grain seperation (m): ")
    grain_seperation_unc = input("Enter the grain seperation uncertainty: ")
    grain_density = input("Enter the grain density (kg/m3): ")
    grain_density_unc = input("Enter the grain density uncertainty: ")
    grain_outer_radius = input("Enter the grain outer radius(m): ")
    grain_outer_radius_unc = input("Enter the grain outer radius uncertainty: ")
    grain_initial_inner_radius = input("Enter the grain inner radius(m): ")
    grain_initial_inner_radius_unc = input("Enter the grain inner radius uncertainty: ")
    grain_initial_height = input("Enter the grain height(m): ")
    grain_initial_height_unc = input("Enter the grain height uncertainty: ")
    grains_center_of_mass_position = input("Enter the grains center of mass position(m): ")
    grains_center_of_mass_position_unc = input("Enter the grains center of mass position uncertainty: ")
    nozzle_position = input("Enter the nozzle position(m): ")
    nozzle_position_unc = input("Enter the nozzle position uncertainty: ")
    motor_position = input("Enter the motor position(m): ")
    motor_position_unc = input("Enter the motor position uncertainty: ")
    grain_number = input("Enter the grain number: ")
    center_of_dry_mass_position = input("Enter the center of dry mass position: ")
    center_of_dry_mass_position_unc = input("Enter the uncertainty in the center of dry mass position: ")

    parameters = {
        # propulsion details
        "motor_structure_mass": (motor_structure_mass, motor_structure_mass_unc),
        "burn_time": (burn_time, burn_time_unc),
        "nozzle_radius": (nozzle_radius, nozzle_radius_unc),
        "throat_radius": (throat_radius, throat_radius_unc),
        "grain_separation": (grain_seperation, grain_seperation_unc),
        "grain_density": (grain_density, grain_density_unc),
        "grain_outer_radius": (grain_outer_radius, grain_outer_radius_unc),
        "grain_initial_inner_radius": (grain_initial_inner_radius, grain_initial_inner_radius_unc),
        "grain_initial_height": (grain_initial_height, grain_initial_height_unc),
        "grains_center_of_mass_position": (grains_center_of_mass_position, grains_center_of_mass_position_unc),
        "nozzle_position": (nozzle_position, nozzle_position_unc),
        "motor_position": (motor_position, motor_position_unc),
        "grain_number": (grain_number),
        "center_of_dry_mass_position": (center_of_dry_mass_position, center_of_dry_mass_position_unc)
    }
       
if data_entry == 0:
    file_location = input("Please paste the full file location here (ensure to add .csv to the file name): ")
    df = pd.read_csv(file_location, dtype = {'data':np.float16})
    file_data = df["data"]
    file_data = file_data.tolist()
        
    parameters = {
        "motor_structure_mass": (file_data[0], file_data[1]),
        "burn_time": (file_data[2], file_data[3]),
        "nozzle_radius": (file_data[4], file_data[5]),
        "throat_radius": (file_data[6], file_data[7]),
        "grain_separation": (file_data[8], file_data[9]),
        "grain_density": (file_data[10], file_data[11]),
        "grain_outer_radius": (file_data[12], file_data[13]),
        "grain_initial_inner_radius": (file_data[14], file_data[15]),
        "grain_initial_height": (file_data[16], file_data[17]),
        "grains_center_of_mass_position": (file_data[18], file_data[19]),
        "nozzle_position": (file_data[20], file_data[21]),
        "motor_position": (file_data[22], file_data[23]),
        "grain_number": (int(file_data[24])),
        "center_of_dry_mass_position": (file_data[25], file_data[26])
    }


Quest_Micro_Maxx_II = SolidMotor(
    thrust_source="C:/Users/keena/Desktop/LRA/Motor Thrust Curves/AeroTech_O5500X-PS.eng",
    burn_time=parameters.get("burn_time")[0],
    dry_mass=parameters.get("motor_structure_mass")[0],
    dry_inertia=(0, 0, 0),
    center_of_dry_mass_position=parameters.get("center_of_dry_mass_position")[0],
    grains_center_of_mass_position=parameters.get("grains_center_of_mass_position")[0],
    grain_number=parameters.get("grain_number"),
    grain_separation=parameters.get("grain_separation")[0],
    grain_density=parameters.get("grain_density")[0],
    grain_outer_radius=parameters.get("grain_outer_radius")[0],
    grain_initial_inner_radius=parameters.get("grain_initial_inner_radius")[0],
    grain_initial_height=parameters.get("grain_initial_height")[0],
    nozzle_radius=parameters.get("nozzle_radius")[0],
    throat_radius=parameters.get("throat_radius")[0],
    interpolation_method="linear",
    nozzle_position=parameters.get("nozzle_position")[0],
    coordinate_system_orientation="combustion_chamber_to_nozzle",  # combustion_chamber_to_nozzle"
)

Quest_Micro_Maxx_II.all_info()