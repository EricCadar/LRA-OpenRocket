import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from rocketpy import Environment, Flight, Function, Rocket, SolidMotor
import pandas as pd
import numpy as np
import datetime

tomorrow = datetime.date.today() + datetime.timedelta(days=1)
env = Environment(latitude=32.990254, longitude=-106.974998, elevation=1400)
env.set_date(
    (tomorrow.year, tomorrow.month, tomorrow.day, 12)
)  # Hour given in UTC time

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
    thrust_source="C:/Users/keena/Desktop/Vs Code/LRA/AeroTech_O5500X-PS.eng",
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

#Quest_Micro_Maxx_II.all_info()
# Step 3: Define the rocket
# Step 3: Define the rocket
calisto = Rocket(
    radius=127 / 2000,
    mass=14.426,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag="C:/Users/keena/Desktop/Vs Code/LRA/powerOffDragCurve.csv",
    power_on_drag="C:/Users/keena/Desktop/Vs Code/LRA/powerOnDragCurve.csv",
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",

)

# Add motor to the rocket
calisto.add_motor(Quest_Micro_Maxx_II, position=-1.255)

# Add components
rail_buttons = calisto.set_rail_buttons(
    upper_button_position=0.0818,
    lower_button_position=-0.6182,
    angular_position=45,
)

nose_cone = calisto.add_nose(
    length=0.55829, kind="von karman", position=1.278
)

fin_set = calisto.add_trapezoidal_fins(
    n=4,
    root_chord=0.120,
    tip_chord=0.060,
    span=0.110,
    position=-1.04956,
    cant_angle=0.5,
    airfoil=("C:/Users/keena/Desktop/Vs Code/LRA/NACA0012-radians.csv", "radians"),
)

tail = calisto.add_tail(
    top_radius=0.0635, bottom_radius=0.0435, length=0.060, position=-1.194656
)

main = calisto.add_parachute(
    name="main",
    cd_s=10.0,
    trigger=800,      # ejection altitude in meters
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

drogue = calisto.add_parachute(
    name="drogue",
    cd_s=1.0,
    trigger="apogee",  # ejection at apogee
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)


# Step 4: Define dynamic TVC function
def dynamic_tvc(time, state):
    """
    Dynamic TVC function based on altitude and pitch/roll.
    Adjusts thrust eccentricity to simulate TVC control.
    
    Parameters:
    - time: Current time in seconds.
    - state: Dictionary with flight state variables (e.g., altitude, pitch, roll).
    
    Returns:
    - (float, float): Eccentricity in x and y directions in meters.
    """
    altitude = state.get("altitude", 0)
    pitch = state.get("pitch", 0)  # In degrees
    roll = state.get("roll", 0)    # In degrees
    
    # TVC parameters
    max_angle_deg = 15  # Maximum TVC angle in degrees
    distance_to_cm = 1.255  # Distance from thrust point to CM in meters
    max_offset = np.tan(np.radians(max_angle_deg)) * distance_to_cm
    
    # Altitude-based adjustment
    angle_factor = altitude / 1000 if altitude < 1000 else 1.0
    
    # Feedback-based adjustment
    pitch_factor = pitch / 15
    roll_factor = roll / 15
    
    x_offset = max_offset * angle_factor * roll_factor
    y_offset = max_offset * angle_factor * pitch_factor

    # Log TVC calculations
    print(f"Altitude: {altitude:.2f} m, Pitch Factor: {pitch_factor:.2f}, Roll Factor: {roll_factor:.2f}")
    print(f"Max Offset: {max_offset:.4f}, X Offset: {x_offset:.4f}, Y Offset: {y_offset:.4f}")

    return x_offset, y_offset


# Step 5: Wrap TVC function for RocketPy compatibility
# Step 5: Wrap TVC function for RocketPy compatibility
x_offsets = []
y_offsets = []
times = []

def tvc_wrapper_x(time, environment, rocket):
    state = {
        "altitude": environment.getAltitude(),
        "pitch": rocket.dynamics.pitch,
        "roll": rocket.dynamics.roll,
    }
    print(f"Time: {time:.2f} s, Altitude: {state['altitude']:.2f} m, Pitch: {state['pitch']:.2f}°, Roll: {state['roll']:.2f}°")
    x_offset, _ = dynamic_tvc(time, state)
    x_offsets.append(x_offset)
    times.append(time)
    return x_offset

def tvc_wrapper_y(time, environment, rocket):
    state = {
        "altitude": environment.getAltitude(),
        "pitch": rocket.dynamics.pitch,
        "roll": rocket.dynamics.roll,
    }
    print(f"Time: {time:.2f} s, Altitude: {state['altitude']:.2f} m, Pitch: {state['pitch']:.2f}°, Roll: {state['roll']:.2f}°")
    _, y_offset = dynamic_tvc(time, state)
    y_offsets.append(y_offset)
    return y_offset



# Step 6: Apply dynamic TVC
calisto.add_thrust_eccentricity(x=tvc_wrapper_x, y=tvc_wrapper_y)

# Step 7: Simulate the flight
test_flight = Flight(
    rocket=calisto, environment=env, rail_length=5.2, inclination=85, heading=0
    )

test_flight.post_process()

# Display flight results
test_flight.all_info()

plt.figure(figsize=(10, 6))
plt.plot(times, x_offsets, label="X Offset (m)", color="blue")
plt.plot(times, y_offsets, label="Y Offset (m)", color="red")
plt.xlabel("Time (s)")
plt.ylabel("Thrust Eccentricity (m)")
plt.title("Thrust Vector Control (TVC) Offsets Over Time")
plt.legend()
plt.grid()
plt.show()



