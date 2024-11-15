import rocketpy
import numpy as np

class Rocket:
    def __init__(self):
        self.max_height = 50000
        self.max_diameter = 3.0
        self.max_weight = 500
        self.stability_margin = 1.5

        self.get_user_inputs()
        
        self.total_mass = self.dry_weight + self.fuel_mass + self.payload_mass

        self.check_constraints()

        self.rocket = rocketpy.Rocket(
            thrustSource=self.thrust_source(),
            burnOut=5,
            radius=self.diameter / 2,
            mass=self.total_mass,
            inertiaI=self.inertia(),
            powerOffDrag=rocketpy.Drag(coefficient=0.75, area=self.cross_sectional_area()),
            position=(0, 0),
            orientation=0
        )

        self.stability_analysis()

    def get_user_inputs(self):
        print("\n=== Rocket Parameter Input ===")
        
        while True:
            try:
                self.name = input("Enter rocket name: ")
                
                self.height = float(input("Enter rocket height (in meters, 0.5-20.0): "))
                if not 0.5 <= self.height <= 20.0:
                    raise ValueError("Height must be between 0.5 and 20.0 meters")
                
                self.diameter = float(input("Enter rocket diameter (in meters, 0.1-3.0): "))
                if not 0.1 <= self.diameter <= self.max_diameter:
                    raise ValueError(f"Diameter must be between 0.1 and {self.max_diameter} meters")
                
                self.dry_weight = float(input("Enter dry weight (in kg, 1-200): "))
                if not 1 <= self.dry_weight <= 200:
                    raise ValueError("Dry weight must be between 1 and 200 kg")
                
                self.engine_thrust = float(input("Enter engine thrust (in Newtons, 50-10000): "))
                if not 50 <= self.engine_thrust <= 10000:
                    raise ValueError("Engine thrust must be between 50 and 10000 Newtons")
                
                self.fuel_mass = float(input("Enter fuel mass (in kg, 1-100): "))
                if not 1 <= self.fuel_mass <= 100:
                    raise ValueError("Fuel mass must be between 1 and 100 kg")
                
                self.payload_mass = float(input("Enter payload mass (in kg, 0-200): "))
                if not 0 <= self.payload_mass <= 200:
                    raise ValueError("Payload mass must be between 0 and 200 kg")
                
                total_mass = self.dry_weight + self.fuel_mass + self.payload_mass
                if total_mass > self.max_weight:
                    raise ValueError(f"Total mass ({total_mass} kg) exceeds maximum limit of {self.max_weight} kg")
                
                break
                
            except ValueError as e:
                print(f"\nError: {str(e)}")
                print("Please try again.\n")

    def thrust_source(self):
        return rocketpy.Thrust(
            thrust=self.engine_thrust,
            burnOut=5
        )

    def inertia(self):
        return (1/12) * self.total_mass * (self.height**2 + self.diameter**2)

    def cross_sectional_area(self):
        return np.pi * (self.diameter / 2) ** 2

    def check_constraints(self):
        print("\n=== Constraint Check ===")
        if self.diameter > self.max_diameter:
            raise ValueError(f"Diameter {self.diameter} exceeds maximum limit {self.max_diameter} m.")
        if self.total_mass > self.max_weight:
            raise ValueError(f"Total weight {self.total_mass} exceeds maximum limit {self.max_weight} kg.")
        print("✓ All constraints satisfied.")

    def stability_analysis(self):
        print("\n=== Stability Analysis ===")
        cm = self.height / 3
        cp = self.height / 2
        static_margin = (cp - cm) / (self.diameter / 2)

        print(f"Center of Mass (CM): {cm:.2f} m")
        print(f"Center of Pressure (CP): {cp:.2f} m")
        print(f"Static Margin: {static_margin:.2f}")

        if static_margin < self.stability_margin:
            print("⚠ Warning: Rocket is unstable! Static margin below acceptable levels.")
        else:
            print("✓ Rocket stability criteria met.")

    def simulate(self):
        print("\n=== Running Simulation ===")
        self.rocket.setInitialConditions(z=0, vz=0)
        self.rocket.simulate()

        print("\nTrajectory Data:")
        print("-" * 40)
        print("Time (s) | Altitude (m)")
        print("-" * 40)
        
        for i in range(0, len(self.rocket.time), 10):
            print(f"{self.rocket.time[i]:8.2f} | {self.rocket.z[i]:11.2f}")
        
        print("-" * 40)
        print(f"Maximum altitude reached: {max(self.rocket.z):.2f} m")
        print(f"Flight duration: {max(self.rocket.time):.2f} s")

if __name__ == "__main__":
    print("Please enter the following parameters for the rocket design.")
    
    try:
        rocket = Rocket()
        rocket.simulate()
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Simulation terminated.")