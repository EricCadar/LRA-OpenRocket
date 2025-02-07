import os
from rocketpy import Environment, SolidMotor, Rocket, Flight, MonteCarlo
from first_rocket import calisto, env, Pro75M1670, nose_cone, fin_set, tail

# Define the stochastic models
#Where my code starts
from rocketpy.stochastic import (
    StochasticEnvironment, 
    StochasticSolidMotor, 
    StochasticTrapezoidalFins,
    StochasticFlight,
    StochasticNoseCone,
    StochasticTail,
    StochasticRocket,
)


# Define the stochastic models
stochastic_env = StochasticEnvironment(
    environment=env,
    elevation=(env.elevation, 10, "normal"),  # Example: normal distribution with 10m standard deviation
    wind_velocity_x_factor=(1, 0.2),  # Example: normal distribution with 20% standard deviation
)

stochastic_motor = StochasticSolidMotor(
    solid_motor=Pro75M1670,
    thrust_source=[
        "Cesaroni_M1670.eng",
        "Cesaroni_M1670.eng",
    ],  # Example: list of thrust sources
    total_impulse=(Pro75M1670.total_impulse, 20, "normal"),  # Example: normal distribution with 20 Ns standard deviation
)

stochastic_nose_cone = StochasticNoseCone(
    nosecone=nose_cone,
    length=(nose_cone.length, 0.01, "normal"),  # Example: normal distribution with 1cm standard deviation
)

stochastic_fin_set = StochasticTrapezoidalFins(
    trapezoidal_fins=fin_set,
    span=(fin_set.span, 0.005, "normal"),  # Example: normal distribution with 5mm standard deviation
    cant_angle=(fin_set.cant_angle, 0.1, "normal"),  # Example: normal distribution with 0.1 degrees standard deviation
)

stochastic_tail = StochasticTail(
    tail=tail, #nothing special just "tail" lol
    top_radius=(tail.top_radius, 0.002, "normal"),  # Example: normal distribution with 2mm standard deviation
)

# Define the stochastic rocket
stochastic_rocket = StochasticRocket(
    rocket=calisto, #sets the rocket for mc simulations equal to the calisto rocket from previous
    mass=(calisto.mass, 0.1, "normal"),  # Example: normal distribution with 100g standard deviation
)
stochastic_rocket.add_motor(stochastic_motor, position=(-1.255, 0.01, "normal"))  # Example: normal distribution with 1cm standard deviation in motor position
stochastic_rocket.add_nose(stochastic_nose_cone)
stochastic_rocket.add_trapezoidal_fins(stochastic_fin_set)
stochastic_rocket.add_tail(stochastic_tail)

# Define a nominal flight
flight = Flight(rocket=calisto, environment=env, rail_length=5.2)

# Define the stochastic flight
stochastic_flight = StochasticFlight(
    flight=flight,
    rail_length=(5.2, 0.05, "normal"),  # Example: normal distribution with 5cm standard deviation
)

# Create a Monte Carlo simulation object
mc = MonteCarlo(    
    filename = "calisto_sim",
    environment=stochastic_env,
    rocket=stochastic_rocket,
    flight=stochastic_flight,
    export_list=['apogee', 'max_speed'],
)

# Run the simulation (example: 100 simulations)
mc.simulate(number_of_simulations = 10)

# Process and analyze results
mc.set_results() ## cretes a disctionary that holds all the values in export list

max_s = max(mc.results['max_speed']) # gets max speed
max_a = max(mc.results['apogee']) # gets max apogee


min_s = min(mc.results['max_speed']) # gets max speed
min_a = min(mc.results['apogee']) # gets max apogee


print(f"\nThe MAX speed is {max_s} and the MAX apogee is {max_a} \n")
print(f"The MIN speed is {min_s} and the MIN apogee is {min_a} \n")


mc.prints.all()
mc.plots.all()
