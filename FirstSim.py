from rocketpy import Environment, SolidMotor, Rocket, Flight

env = Environment(latitude=32.990254, longitude=-106.974998, elevation=1400)

import datetime

tomorrow = datetime.date.today() + datetime.timedelta(days=1)

env.set_date(
    (tomorrow.year, tomorrow.month, tomorrow.day, 12)
)  # Hour given in UTC time

env.set_atmospheric_model(type="Forecast", file="GFS")

AeroTech = SolidMotor(
    thrust_source="C:/Users/cade/OneDrive/Desktop/LRA/Motors/AeroTech_O5500X-PS.eng",
    dry_mass=0,
    dry_inertia=(0, 0, 0),
    nozzle_radius=0.036750000000000005,
    grain_number=1,
    grain_density=1394.8612601528669,
    grain_outer_radius=0.049,
    grain_initial_inner_radius=0.0245,
    grain_initial_height=1.239,
    grain_separation=0,
    grains_center_of_mass_position=0,
    center_of_dry_mass_position=0,
    nozzle_position=-0.6195,
    burn_time=3.9,           #Did not have burn time, and some numbers are zero?
    throat_radius=0.0245,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

calisto = Rocket(
        center_of_mass_without_motor = 1.762,
        coordinate_system_orientation = "nose_to_tail",
        power_off_drag="C:/Users/cade/OneDrive/Desktop/LRA/Motors/powerOffDragCurve.csv",
        power_on_drag="C:/Users/cade/OneDrive/Desktop/LRA/Motors/powerOnDragCurve.csv",
        inertia = [
            0.052,
            0.052,
            15.411
        ],
        mass = 20.254,
        radius = 0.065405
)

calisto.add_motor(AeroTech, position=2.4223477193700154)

rail_buttons = calisto.set_rail_buttons(
    upper_button_position=2.57,
    lower_button_position= 2.91,
    angular_position=0.0,
)

nose_cone = calisto.add_nose(
    length=0.6858, 
    kind="von karman", 
    position=0.0
)

fin_set = calisto.add_trapezoidal_fins(
    n=4,
    root_chord=0.254,
    tip_chord=0.07619999999999999,
    span=0.127,
    position=2.8,
    cant_angle=0.0,
    airfoil=("C:/Users/cade/OneDrive/Desktop/LRA/Motors/NACA0012-radians.csv","radians"),
)

tail = calisto.add_tail(
    top_radius=0.065405, 
    bottom_radius=0.055, 
    length=0.127, 
    position=3.0797499999999998
)

main = calisto.add_parachute(
    name="Main: L3 Elliptical Parachute [Cd 1.55 (30 oz) 151.2 in^3]",
    cd_s=7.004724191043808,
    trigger=243.84,      # ejection altitude in meters
    sampling_rate=105,   # do not have sampling rate, or noise (also not sure about lag being zero)
    lag=0.0,             
    noise=(0, 8.3, 0.5), 
)

drogue = calisto.add_parachute(
    name="Elliptical Parachute [Cd 1.55 (2.2 oz) 12.2 in^3]",
    cd_s=0.6420997175123491,
    trigger="apogee",  # ejection at apogee
    sampling_rate=105,  # do not have sampling rate, or noise (also not sure about lag being zero)
    lag=0.0,
    noise=(0, 8.3, 0.5),
)

test_flight = Flight(
    rocket=calisto, 
    environment=env, 
    rail_length=1.0, 
    inclination=90.0, 
    heading=90.0
    )

test_flight.plots.trajectory_3d()



