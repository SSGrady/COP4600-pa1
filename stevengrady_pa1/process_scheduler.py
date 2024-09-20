# Implement Pre-emptive SJF Scheduler
# Author: ChatGPT
# Co-Programmer and lead debugger: Steven Grady - COP 4600 PA#1 Group 13
import sys

# Creates a dictionary to store the process data
def process_data(name, arrival, burst):
    return {
        'name': name,
        'arrival': arrival,
        'burst' : burst,
        'remaining_time': burst,
        'start_time': None,
        'completion_time': None,
        'wait_time': 0,
        'turnaround_time': 0,
        'response_time': None
    }

def sjf_scheduler(processes, total_time):
    """Preemptive Shortest Job First (SJF) scheduler."""
    time = 0
    completed_processes = []
    running_process = None

    print(f'{len(processes)} processes')
    print('Using preemptive Shortest Job First')

    while time < total_time:
        # Check for newly arrived processes
        new_arrivals = [p for p in processes if p['arrival'] == time]

        for process in new_arrivals:
            print(f"Time {time:4}: {process['name']} arrived")

        # Get processes that have arrived by the current time
        available_processes = [p for p in processes if p['arrival'] <= time and p['remaining_time'] > 0]

        if available_processes:
            # Select the process with the shortest remaining burst time
            shortest_job = min(available_processes, key=lambda p: p['remaining_time'])

            if running_process:
                if shortest_job['remaining_time'] < running_process['remaining_time']:
                    # Preempt the running process if a shorter job arrives
                    running_process = shortest_job
            else:
                running_process = shortest_job

            if running_process['start_time'] is None:
                running_process['start_time'] = time
                running_process['response_time'] = time - running_process['arrival']

            print(f"Time {time:4}: {running_process['name']} selected (burst {running_process['remaining_time']:4})")

            # Execute the process for 1 time unit
            running_process['remaining_time'] -= 1

            # If the process is completed, mark it as finished
            if running_process['remaining_time'] == 0:
                running_process['completion_time'] = time + 1
                running_process['turnaround_time'] = running_process['completion_time'] - running_process['arrival']
                running_process['wait_time'] = running_process['turnaround_time'] - running_process['burst']
                print(f"Time {time + 1:4}: {running_process['name']} finished")
                completed_processes.append(running_process)
                running_process = None
        else:
            # No process available, CPU is idle
            print(f"Time {time:4}: Idle")

        time += 1

    print(f"Finished at time {total_time:4}")
    return completed_processes

def round_robin_scheduler(processes, quantum, total_time):
    """Round Robin Scheduler with fixed quantum time slice and formatted output."""
    time = 0
    queue = [p for p in sorted(processes, key=lambda x: x['arrival'])]
    completed_processes = []
    
    print(f"{len(processes)} processes")
    print("Using Round Robin")
    print(f"Quantum {quantum}")
    
    while time < total_time:
        # Check for newly arrived processes
        new_arrivals = [p for p in queue if p['arrival'] == time]
        for process in new_arrivals:
            print(f"Time {time:4}: {process['name']} arrived")
        
        if queue:
            current_process = queue.pop(0)
            
            if current_process['start_time'] is None:
                current_process['start_time'] = time
                current_process['response_time'] = time - current_process['arrival']
            
            print(f"Time {time:4}: {current_process['name']} selected (burst {current_process['remaining_time']:4})")
            
            if current_process['remaining_time'] <= quantum:
                time += current_process['remaining_time']
                current_process['remaining_time'] = 0
                current_process['completion_time'] = time
                current_process['turnaround_time'] = current_process['completion_time'] - current_process['arrival']
                current_process['wait_time'] = current_process['turnaround_time'] - current_process['burst']
                
                print(f"Time {time:4}: {current_process['name']} finished")
                completed_processes.append(current_process)
            else:
                time += quantum
                current_process['remaining_time'] -= quantum
                queue.append(current_process)
        else:
            # No process available, CPU is idle
            print(f"Time {time:4}: Idle")
            time += 1
        
        # Add newly arrived processes to the queue
        queue += [p for p in processes if p['arrival'] == time]

    print(f"Finished at time {total_time:4}")
    return completed_processes



def validate_input(params) -> None:
    """Validates the required input parameters."""
    if 'use' not in params:
        print("Error: Missing parameter 'use'")
        sys.exit(1)
    if params['use'] == 'rr' and 'quantum' not in params:
        print("Error: Missing quantum parameter when use is 'rr'")
        sys.exit(1)
    if 'processcount' not in params or 'runfor' not in params:
        print("Error: Missing essential parameters (processcount, runfor)")
        sys.exit(1)
    return

# Defining the main func framework
def main(input_file):
    params = {}
    processes = []

    try:
        with open(input_file, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if parts[0] == 'processcount':
                    params['processcount'] = int(parts[1])
                elif parts[0] == 'runfor':
                    params['runfor'] = int(parts[1])
                elif parts[0] == 'use':
                    params['use'] = parts[1]
                elif parts[0] == 'quantum':
                    params['quantum'] = int(parts[1])
                elif parts[0] == 'process':
                    name = parts[2]
                    arrival = int(parts[4])
                    burst = int(parts[6])
                    processes.append(process_data(name, arrival, burst))
                elif parts[0] == 'end':
                    break
                
        validate_input(params)
        
        if params['use'] == 'sjf':
            completed_processes = sjf_scheduler(processes, params['runfor'])
        
        # Output the results
        for process in completed_processes:
            print(f"{process['name']} wait {process['wait_time']} turnaround {process['turnaround_time']} response {process['response_time']}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        # this print statement is for the final output script file
        # print("Usage: scheduler-gpt.py <input file>")
        print("Usage: process_scheduler.py <input file>")

    input_file = sys.argv[1]
    main(input_file)