# Implement Pre-emptive SJF Scheduler
import sys

# Creates a dictionary to store the process data
def process_data(name, arrival, burst):
    return 
    {
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
    # Preemptive shortest job first (SJF) scheduler
    time = 0
    completed_processes = []
    running_process = None

    print(f'{len(processes)} processes')
    print('Using preemptive Shortest Job First')

    while time < total_time:
        # Check for newly arrived processes
        new_arrivals = [p for p in processes if p['arrival'] == time]

        for process in new_arrivals:
            # Ensure time is padded w spaces if it has fewer than four digits
            print(f"Time {time:4}: {process['name']} arrived")
        # Get processes that have arrived by the current time
        available_processes = [p for p in processes if p['arrival'] <= time and p['remaining_time'] > 0]

        if available_processes:
            # Select the process w the shortest remaining burst time
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