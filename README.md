# Traffic Light Simulation - Python (SimPy)
- This is a Python-based simulation project that models a traffic intersection using the SimPy discrete-event simulation library.

- It simulates vehicles arriving at a signal, waiting during red/yellow lights, and passing through during the green light to analyze system performance under different conditions.

# Getting Started
1. Clone the repository.

2. Install the required dependencies using:
`pip install simpy`

3. Run the simulation using:
`python Smarttraffic.py`

# Features
- Traffic light control with Red, Yellow, and Green phases.
- Randomized vehicle arrivals using an exponential distribution.

- Calculates and displays key performance metrics:
    - Average waiting time per vehicle
    - Maximum queue length observed
    - Total number of vehicles passed

- Runs multiple scenarios independently for comparison.

# Scenarios

## Baseline Traffic
In this scenario, the traffic is at its baseline level, with no significant changes.
- Arrival rate: 10 vehicles per second
- Green light: 30 seconds
- Yellow light: 3 seconds
- Red light: 50 seconds
- Service time: 1.5 seconds

## Heavy Traffic
In this scenario, the traffic is heavier, with more vehicles passing through the intersection during the green light phase.
- Arrival rate: 20 vehicles per second
- Green light: 30 seconds
- Yellow light: 3 seconds
- Red light: 50 seconds
- Service time: 1.5 seconds

## Faster Service
In this scenario, the vehicle service time is faster, with vehicles passing through the intersection more quickly during the green light phase.
- Arrival rate: 10 vehicles per second
- Green light: 30 seconds
- Yellow light: 3 seconds
- Red light: 50 seconds 
- Service time: 1 second

Each scenario runs for 500 simulation seconds and displays detailed output in the terminal.

# How It Works

## Vehicle Arrival:
Vehicles arrive randomly using exponential timing based on the defined arrival rate. Each new vehicle joins the waiting queue.

## Traffic Light Cycle:
The signal operates in continuous red, yellow, and green phases:
- Red: All vehicles must stop (no movement).
- Yellow: Transition period; no vehicles pass.
- Green: Vehicles pass one by one, each taking service_time seconds.

## Data Collection:
During the simulation, the system records:
- The waiting time of each vehicle before passing
- Queue lengths after every red light
- The total number of vehicles passed at the end of simulation

## Result Summary:
After each scenario, results are printed including average waiting time, maximum queue length, and total vehicles passed.

# Conclusion
This simulation provides insights into the performance of traffic lights under different traffic conditions. It can help identify areas for improvement and optimize traffic signal timings to enhance system efficiency.

# References
1. SimPy Documentation: https://simpy.readthedocs.io/en/latest/