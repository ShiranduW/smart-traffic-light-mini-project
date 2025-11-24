import simpy;
import random;
import pandas as pd; # For exporting simulation results to CSV files.

# Create the environment.
env = simpy.Environment()

wait_times = []      # Stores how long each vehicle waited
vehicles_passed = 0  # Counts vehicles that have crossed
queue_lengths = []
queue = []  # Create an empty list to store vehicles waiting at the intersection.

# Define a function to simulate vehicle arrivals.
def vehicle_arrival(env, queue, arrival_rate):
    while True:
        # random.expovariate(1.0 / arrival_rate) creates a random time.
        yield env.timeout(random.expovariate(1.0 / arrival_rate))
        # Record the time and add to queue when the vehicle arrived.
        arrival_time = env.now
        queue.append(arrival_time)
        print(f"Vehicle arrived at {env.now} seconds, queue length: {len(queue)}")

def traffic_light_cycle(env, queue, green_time, yellow_time, red_time, service_time):
    # Keeps track about the number of vehicles crossed the intersection.
    global vehicles_passed
    while True:
        # RED LIGHT.
        # Waiting for the red light period.
        red_end = env.now + red_time
        print(f"Red light ON at {env.now} seconds")
        yield env.timeout(red_end - env.now)
        print(f"Red light OFF at {env.now} seconds")
        
        # Take queue length.
        queue_lengths.append(len(queue)) 
        
        # YELLOW LIGHT
        yellow_end = env.now + yellow_time
        print(f"Yellow light ON at {env.now} seconds")
        yield env.timeout(yellow_end - env.now)
        print(f"Yellow light OFF at {env.now} seconds")
        
        # GREEN LIGHT.
        print(f"Green light ON at {env.now} seconds")
        # Calculate the end time of the green light.
        green_end = env.now + green_time

        # Let vehicles cross during green light.
        while env.now < green_end and queue:
            # Delete the first vehicle in the queue.
            arrival_time = queue.pop(0)
            wait_time = env.now - arrival_time
            wait_times.append(wait_time) # Collect wait time.
            vehicles_passed += 1
            print(f"Vehicle passed at {env.now} seconds, waited {wait_time} seconds")
            # Wait for the vehicle to cross the intersection before next one.
            yield env.timeout(service_time)

        print(f"Green light OFF at {env.now} seconds")
        
# Define a function to export simulation results to CSV files.
def export_results(wait_times, queue_lengths, vehicles_passed, filename_prefix):
    max_len = max(len(wait_times), len(queue_lengths))
    wait_times_padded = wait_times + [None] * (max_len - len(wait_times))
    queue_lengths_padded = queue_lengths + [None] * (max_len - len(queue_lengths))

    df = pd.DataFrame({
        'WaitTime': wait_times_padded,
        'QueueLength': queue_lengths_padded
    })
    df.to_csv(f'{filename_prefix}_simulation_data.csv', index=False)

    summary = {
        'AverageWaitTime': sum(wait_times) / len(wait_times) if wait_times else 0,
        'MaxQueueLength': max(queue_lengths) if queue_lengths else 0,
        'TotalVehiclesPassed': vehicles_passed
    }
    pd.DataFrame([summary]).to_csv(f'{filename_prefix}_summary.csv', index=False)
        
# Run the simulation for a given scenario separately.
def run_scenario(arrival_rate, green_time, yellow_time, red_time, service_time, end_time=900):
    # global is for sharing variables between functions.
    global wait_times, vehicles_passed, queue_lengths, queue
    wait_times, vehicles_passed, queue_lengths = [], 0, []
    queue = []
    
    # Run the simulation.
    env = simpy.Environment()
    env.process(vehicle_arrival(env, queue, arrival_rate))
    env.process(traffic_light_cycle(env, queue, green_time, yellow_time, red_time, service_time))
    
    env.run(until=end_time) # Run the simulation for 900 seconds.
    
    # Calculate average wait time and max queue length.
    if wait_times:
        avg_wait = sum(wait_times) / len(wait_times)
    else:
        avg_wait = 0
    if queue_lengths:
        max_queue = max(queue_lengths)
    else:
        max_queue = 0
    
    # print scenario.
    print("=" * 40)
    print(f"Scenario with arrival rate {arrival_rate}, Green time {green_time}, and , service time {service_time}")
    print("=" * 40)
    
    # Export results to CSV files with scenario details in filename.
    filename_prefix = f'arr{arrival_rate}_green{green_time}_serv{service_time}'
    export_results(wait_times, queue_lengths, vehicles_passed, filename_prefix)
    
    return avg_wait, max_queue, vehicles_passed

# Run multiple repetitions of the same scenario.
def run_multiple_repetitions(arrival_rate, green_time, yellow_time, red_time, service_time, runs=5, warmup_duration=100, measurement_duration=900):
    total_avg_wait, total_max_queue, total_vehicles = 0, 0, 0

    for i in range(runs):
        # Run simulation with warm-up: just run environment for warmup_duration to let system stabilize without collecting data.
        # Then run measurement period from warmup_duration to warmup_duration + measurement_duration.
        avg_wait, max_queue, vehicles_passed = run_scenario(arrival_rate, green_time, yellow_time, red_time, service_time, 
        end_time = warmup_duration + measurement_duration)                                                 
        total_avg_wait += avg_wait
        total_max_queue = max(total_max_queue, max_queue) 
        total_vehicles += vehicles_passed
    
# Run five scenarios separately.
run_multiple_repetitions(10, 30, 3, 50, 1.5, runs=5) # Baseline traffic scenario
run_multiple_repetitions(20, 30, 3, 50, 1.5, runs=5) # Heavy traffic scenario
run_multiple_repetitions(5, 30, 3, 50, 1.5, runs=5)  # Low Traffic Scenario
run_multiple_repetitions(10, 30, 3, 50, 1, runs=5)   # Faster servicec scenario
run_multiple_repetitions(10, 40, 3, 50, 1.5, runs=5) # Improved signal timing scenario