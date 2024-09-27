# Any lines manually added or modified by me will be started with "JL: ".

import os
import sys
from collections import deque

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = -1  # Initialized as -1 to detect first response
        self.completed = False
        self.appended = False # JL: I added this attribute.

    def __repr__(self):
        return (f"Process(name={self.name}, arrival_time={self.arrival_time}, "
                f"burst_time={self.burst_time}, wait_time={self.wait_time}, "
                f"turnaround_time={self.turnaround_time}, response_time={self.response_time})")

def parse_input_file(file_path):
    process_count = None
    run_for = None
    scheduling_algo = None
    quantum = None
    processes = []

    with open(file_path, 'r') as file:
        for line in file:
            tokens = line.strip().split()

            if not tokens:
                continue

            if tokens[0] == 'processcount':
                process_count = int(tokens[1])

            elif tokens[0] == 'runfor':
                run_for = int(tokens[1])

            elif tokens[0] == 'use':
                scheduling_algo = tokens[1]

            elif tokens[0] == 'quantum':
                quantum = int(tokens[1])

            elif tokens[0] == 'process':
                # Parse process arguments like name P1 arrival 0 burst 5 (space between arguments)
                process_args = {tokens[i]: tokens[i + 1] for i in range(1, len(tokens), 2)}
                name = process_args['name']
                arrival = int(process_args['arrival'])
                burst = int(process_args['burst'])

                process = Process(name, arrival, burst)
                processes.append(process)

            elif tokens[0] == 'end':
                break

    # Error checking for missing parameters
    if process_count is None:
        print("Error: Missing parameter processcount")
        sys.exit(1)
    if run_for is None:
        print("Error: Missing parameter runfor")
        sys.exit(1)
    if scheduling_algo is None:
        print("Error: Missing parameter use")
        sys.exit(1)
    if scheduling_algo == 'rr' and quantum is None:
        print("Error: Missing quantum parameter when use is 'rr'")
        sys.exit(1)

    return process_count, run_for, scheduling_algo, quantum, processes

def round_robin_scheduling(processes, run_for, quantum):
    time = 0
    ready_queue = deque()
    timeline = []
    active_processes = {p.name: p for p in processes}

    # Simulation loop
    while time < run_for:
        # Check if any processes are arriving at the current time
        for process in processes:
            
            # JL: I added the process.appended check.
            if process.arrival_time == time and process.appended == False:
                ready_queue.append(process)
                timeline.append(f"Time {time}: {process.name} arrived")
        
        # If there's a process in the ready queue, process it
        if ready_queue:
            current_process = ready_queue.popleft()

            # If the process is selected for the first time, log it and set response time
            if current_process.response_time == -1:
                current_process.response_time = time - current_process.arrival_time

            timeline.append(f"Time {time}: {current_process.name} selected (burst {current_process.remaining_time})")

            # Run the process for the quantum or for its remaining time, whichever is smaller
            time_slice = min(quantum, current_process.remaining_time)
            current_process.remaining_time -= time_slice
            time += time_slice
            
            # Check if any processes are arriving during this time slice
            # JL: I widened the range by 1 to the right.
            for t in range(time - time_slice, time+1):
                for process in processes:
                    
                    # JL: I added the "process.response_time == -1" check and "process.appended" modification.
                    if process.arrival_time == t and process.response_time == -1 and process.completed == False and process not in ready_queue and process.remaining_time > 0:
                        process.appended = True
                        ready_queue.append(process)
                        timeline.append(f"Time {t}: {process.name} arrived")
                        
            # If the process finishes
            if current_process.remaining_time == 0:
                current_process.completed = True
                current_process.turnaround_time = time - current_process.arrival_time
                current_process.wait_time = current_process.turnaround_time - current_process.burst_time
                timeline.append(f"Time {time}: {current_process.name} finished")
            else:
                ready_queue.append(current_process)  # Put back into the queue if not finished
            
        else:
            # If no process is in the queue, the CPU is idle
            timeline.append(f"Time {time}: Idle")
            time += 1

    return timeline

def fcfs_scheduling(processes, run_for):
    """First-Come, First-Served (FCFS) scheduling."""
    time = 0
    timeline = []
    process_queue = []
    running_process = None
    last_process = None  # JL: To track the last logged process, similar to other schedulers

    processes.sort(key=lambda p: p.arrival_time)
    
    while time < run_for:
        # Check for arriving processes at the current time
        for process in processes:
            if process.arrival_time == time:
                process_queue.append(process)
                timeline.append(f"Time {time}: {process.name} arrived")

        # If there's no running process and there are processes in the queue
        if not running_process and process_queue:
            running_process = process_queue.pop(0)
            
            # Set the response time if it's the first time the process is selected
            if running_process.response_time == -1:
                running_process.response_time = time - running_process.arrival_time
            
            # Log the process selection only if it's different from the last process
            if last_process != running_process.name:
                timeline.append(f"Time {time}: {running_process.name} selected (burst {running_process.remaining_time})")
                last_process = running_process.name

        if running_process:
            # Process is running, execute it for 1 time unit
            running_process.remaining_time -= 1
            
            # If the process finishes
            if running_process.remaining_time == 0:
                running_process.completed = True
                running_process.turnaround_time = (time + 1) - running_process.arrival_time
                running_process.wait_time = running_process.turnaround_time - running_process.burst_time
                timeline.append(f"Time {time + 1}: {running_process.name} finished")
                running_process = None
                last_process = None  # Reset last process since the current one finished
        else:
            # If no process is running, the CPU is idle
            timeline.append(f"Time {time}: Idle")
            last_process = None  # Reset last process during idle time

        time += 1

    return timeline


def sjf_scheduling(processes, run_for):
    """Preemptive Shortest Job First (SJF) scheduler with reduced redundant logging for processes."""
    time = 0
    timeline = []
    ready_queue = []
    running_process = None
    completed_processes = []
    last_process = None  # To keep track of the last logged process (not idle)

    processes.sort(key=lambda p: p.arrival_time)

    while time < run_for:
        # Check for newly arrived processes
        for process in processes:
            if process.arrival_time == time:
                ready_queue.append(process)
                timeline.append(f"Time {time}: {process.name} arrived")

        # Remove finished processes from the ready queue
        ready_queue = [p for p in ready_queue if p.remaining_time > 0]

        if ready_queue:
            # Select the process with the shortest remaining burst time
            shortest_job = min(ready_queue, key=lambda p: p.remaining_time)

            # Preempt the running process if a shorter job arrives or there's no running process
            if running_process is None or shortest_job.remaining_time < running_process.remaining_time:
                running_process = shortest_job

            # If the process is selected for the first time, set response time
            if running_process.response_time == -1:
                running_process.response_time = time - running_process.arrival_time

            # Log the process only if it's a different process from the last one
            if last_process != running_process.name:
                timeline.append(f"Time {time}: {running_process.name} selected (burst {running_process.remaining_time})")
                last_process = running_process.name

            # Execute the process for 1 time unit
            running_process.remaining_time -= 1

            # If the process completes, mark it as finished
            if running_process.remaining_time == 0:
                running_process.completed = True
                running_process.turnaround_time = (time + 1) - running_process.arrival_time
                running_process.wait_time = running_process.turnaround_time - running_process.burst_time
                timeline.append(f"Time {time + 1}: {running_process.name} finished")
                last_process = None  # Reset last_process as the current process finished
                completed_processes.append(running_process)
                running_process = None
        else:
            # No process is ready, the CPU is idle
            timeline.append(f"Time {time}: Idle")
            last_process = None  # Reset last_process because we're in idle state

        time += 1

    return timeline


def print_to_output_file(process_count, scheduling_algo, run_for, quantum, processes, timeline, output_file):
    # Determine the name of the scheduling algorithm
    if scheduling_algo == 'fcfs':
        scheduling_algo_name = "First-Come First-Served"
    elif scheduling_algo == 'sjf':
        scheduling_algo_name = "preemptive Shortest Job First"
    elif scheduling_algo == 'rr':
        scheduling_algo_name = "Round-Robin"
    else:
        scheduling_algo_name = scheduling_algo  # Fallback, just print the given name if not one of the known ones

    with open(output_file, 'w') as f:
        # Print the summary header
        f.write(f"{process_count} processes\n")
        f.write(f"Using {scheduling_algo_name}\n") # JL: modified print statement to match the above conditional check.
        
        if scheduling_algo == 'rr':
            f.write(f"Quantum {quantum}\n")

        f.write('\n')
        
        # Print the timeline (arrival, selected, finished, idle)
        for event in timeline:
            f.write(event + '\n')

        # Print when the simulation finishes
        f.write(f"Finished at time {run_for}\n")

        # JL: Print newline.
        f.write('\n')

        # Print each process's wait, turnaround, and response times
        processes.sort(key=lambda p: p.name)
        for process in processes:
            if process.completed:
                f.write(f"{process.name} wait \t{process.wait_time} "
                        f"turnaround \t{process.turnaround_time} "
                        f"response \t{process.response_time}\n")
            else:
                f.write(f"{process.name} did not finish\n")

def main():
    # Check if the input file is provided
    if len(sys.argv) < 2:
        print("Usage: scheduler-get.py <input file>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Parse the input file
    process_count, run_for, scheduling_algo, quantum, processes = parse_input_file(input_file)

    # JL: I added in this conditional block of code to decide which algorithm to run.
    # Determine the name of the scheduling algorithm and run it
    if scheduling_algo == 'fcfs':
        scheduling_algo_name = "First-Come First-Served"
        completed_processes = fcfs_scheduling(processes, run_for)
    elif scheduling_algo == 'rr':
        scheduling_algo_name = "Round-Robin"
        completed_processes = round_robin_scheduling(processes, run_for, quantum)
    elif scheduling_algo == 'sjf':
        scheduling_algo_name = "preemptive Shortest Job First"
        completed_processes =sjf_scheduling(processes, run_for)    

    # Create output file name by replacing the input file's extension with '.out'
    output_file = os.path.splitext(input_file)[0] + '.out'

    # Write the output to the file
    # JL: I modified the call to bring it in line with the function definition.
    print_to_output_file(process_count, scheduling_algo, run_for, quantum, processes, completed_processes, output_file)

if __name__ == '__main__':
    main()
