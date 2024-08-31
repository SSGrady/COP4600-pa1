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