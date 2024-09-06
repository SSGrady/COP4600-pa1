#FCFS Implementation
import sys

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.remaining_burst = burst
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = -1
        self.start_time = None
        self.finish_time = None

def fifo_scheduler(processes, total_time):
    time = 0
    finished_processes = []
    events = []

    while time < total_time:
        idle_logged = False
        for process in processes:
            if process.arrival == time:
                events.append(f"Time {time:>4} : {process.name} arrived")

            if process.arrival <= time and process.start_time is None:
                process.start_time = time
                process.response_time = time - process.arrival
                process.wait_time = process.response_time
                process.finish_time = time + process.burst
                time = process.finish_time
                process.turnaround_time = process.finish_time - process.arrival
                finished_processes.append(process)
                events.append(f"Time {process.start_time:>4} : {process.name} selected (burst {process.burst:>4})")
                events.append(f"Time {process.finish_time:>4} : {process.name} finished")
                idle_logged = True
                break

        if not idle_logged:
            events.append(f"Time {time:>4} : Idle")
            time += 1

    return finished_processes, events

def calculate_metrics(processes):
    metrics = []
    for process in processes:
        metrics.append(f"{process.name} wait {process.wait_time:>4} turnaround {process.turnaround_time:>4} response {process.response_time:>4}")
    return metrics

def parse_input(input_file):
    processes = []
    with open(input_file, 'r') as file:
        lines = file.readlines()

        process_count = None
        total_time = None
        algorithm = None
        quantum = None

        for line in lines:
            parts = line.strip().split()
            if parts[0] == 'processcount':
                process_count = int(parts[1])
            elif parts[0] == 'runfor':
                total_time = int(parts[1])
            elif parts[0] == 'use':
                algorithm = parts[1]
            elif parts[0] == 'quantum':
                quantum = int(parts[1])
            elif parts[0] == 'process':
                name = parts[2]
                arrival = int(parts[4])
                burst = int(parts[6])
                processes.append(Process(name, arrival, burst))
            elif parts[0] == 'end':
                break

        # Error handling
        if algorithm == 'rr' and quantum is None:
            print("Error: Missing quantum parameter when use is 'rr'")
            exit(1)

        return processes, total_time, algorithm, quantum

def write_output(output_file, process_count, algorithm, quantum, events, processes, total_time):
    with open(output_file, 'w') as file:
        file.write(f"{process_count} processes\n")
        file.write(f"Using First-Come First-Served\n")

        for event in events:
            file.write(f"{event}\n")

        file.write(f"Finished at time  {total_time}\n")

        for process in processes:
            file.write(f"{process.name} wait {process.wait_time:>4} turnaround {process.turnaround_time:>4} response {process.response_time:>4}\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: scheduler-gpt.py <input file>")
        return

    input_file = sys.argv[1]
    if not input_file.endswith('.in'):
        print("Error: Invalid file extension. The input file must have a .in extension.")
        return

    base_name = input_file[:-3]
    output_file = base_name + '.out'

    processes, total_time, algorithm, quantum = parse_input(input_file)

    if algorithm == 'fcfs':
        finished_processes, events = fifo_scheduler(processes, total_time)
        metrics = calculate_metrics(finished_processes)
        write_output(output_file, len(processes), "First-Come First-Served", quantum, events, finished_processes, total_time)
    else:
        print("Error: Unsupported algorithm for this implementation")
        return

if __name__ == '__main__':
    main()
