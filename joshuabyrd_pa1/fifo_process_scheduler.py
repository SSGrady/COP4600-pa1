# Implement FIFO
# Author: ChatGPT
# Co-Programmer: Joshua Byrd - COP 4600 PA#1 Group 13
import sys

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.start_time = None
        self.finish_time = None
        self.wait_time = None
        self.turnaround_time = None
        self.response_time = None


def parse_input_file(input_file):
    processes = []
    run_for = None
    algorithm = None
    quantum = None
    process_count = None
    required_params = {
        'processcount': False,
        'runfor': False,
        'use': False
    }
    
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('processcount'):
                process_count = int(line.split()[1])
                required_params['processcount'] = True
            elif line.startswith('runfor'):
                run_for = int(line.split()[1])
                required_params['runfor'] = True
            elif line.startswith('use'):
                algorithm = line.split()[1]
                required_params['use'] = True
            elif line.startswith('quantum'):
                quantum = int(line.split()[1])
            elif line.startswith('process'):
                parts = line.split()
                try:
                    name = parts[2]
                    arrival = int(parts[4])
                    burst = int(parts[6])
                    processes.append(Process(name, arrival, burst))
                except (IndexError, ValueError):
                    print("Error: Missing parameter in process line")
                    sys.exit(1)
            elif line.startswith('end'):
                break

    # Check for missing parameters
    for param, is_present in required_params.items():
        if not is_present:
            print(f"Error: Missing parameter {param}")
            sys.exit(1)

    if algorithm == 'rr' and quantum is None:
        print("Error: Missing quantum parameter when use is 'rr'")
        sys.exit(1)

    return processes, run_for, algorithm, quantum


def calculate_metrics(processes, run_for):
    for process in processes:
        if process.finish_time is None:
            process.finish_time = run_for  # Set finish_time to run_for if not completed
        if process.start_time is None:
            process.start_time = process.arrival  # Set start_time to arrival if not set
        
        process.turnaround_time = process.finish_time - process.arrival
        process.wait_time = process.turnaround_time - process.burst
        process.response_time = process.start_time - process.arrival


def write_output(filename, processes, events, run_for):
    output_file = filename.replace('.in', '.out')
    
    with open(output_file, 'w') as file:
        file.write(f"{len(processes)} processes\n")
        file.write("Using First-Come First-Served\n")
        for event in events:
            file.write(f"{event}\n")
        file.write(f"Finished at time {run_for}\n")
        
        for process in processes:
            file.write(f"{process.name} wait {process.wait_time} turnaround {process.turnaround_time} response {process.response_time}\n")


def fifo_scheduler(processes, run_for):
    time = 0
    events = []
    processes_queue = []
    current_process = None
    
    while time < run_for:
        # Add new arrivals to the queue
        for process in processes:
            if process.arrival == time:
                processes_queue.append(process)
                events.append(f"Time {time} : {process.name} arrived")
                if current_process is None and len(processes_queue) == 1:
                    # Start the first process if no process is currently running
                    current_process = processes_queue.pop(0)
                    current_process.start_time = time
                    events.append(f"Time {time} : {current_process.name} selected (burst {current_process.burst})")
        
        # Process the current process if there is one
        if current_process:
            if time == current_process.start_time + current_process.burst:
                # Finish the current process
                current_process.finish_time = time
                events.append(f"Time {time} : {current_process.name} finished")
                current_process = None  # No process is currently running
                
                # If there are no processes left in the queue, log Idle
                if not processes_queue:
                    events.append(f"Time {time} : Idle")
                elif processes_queue:
                    current_process = processes_queue.pop(0)
                    current_process.start_time = time
                    events.append(f"Time {time} : {current_process.name} selected (burst {current_process.burst})")
        else:
            # Log idle time if no process is running and the queue is empty
            if not processes_queue:
                events.append(f"Time {time} : Idle")
        
        time += 1
    
    return events


def main(input_file):
    processes, run_for, algorithm, quantum = parse_input_file(input_file)
    
    # Run the appropriate scheduler (currently only supporting FCFS/FIFO)
    if algorithm == 'fcfs':
        events = fifo_scheduler(processes, run_for)
    
    # Calculate metrics (turnaround, wait, and response times)
    calculate_metrics(processes, run_for)
    
    # Write the output to a file
    write_output(input_file, processes, events, run_for)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: scheduler.py <input file>")
        sys.exit(1)
    main(sys.argv[1])
