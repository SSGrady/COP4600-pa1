import sys
#!/usr/bin/env python3


class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.remaining_time = burst
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1


def read_input(filename):
    if not filename.endswith('.in'):
        raise ValueError("Input file must have a .in extension.")
    
    with open(filename, 'r') as file:
        lines = file.readlines()

    process_count = int(lines[0].split()[1])
    run_for = int(lines[1].split()[1])
    algorithm = lines[2].split()[1].lower()

    processes = []
    for line in lines[3:]:
        if line.startswith('process'):
            parts = line.split()
            name = parts[2]
            arrival = int(parts[4])
            burst = int(parts[6])
            processes.append(Process(name, arrival, burst))
        elif line.strip() == "end":
            break

    return process_count, run_for, algorithm, processes


def fifo_scheduling(processes, run_for):
    processes.sort(key=lambda p: p.arrival)
    current_time = 0
    timeline = []
    completed_processes = []
    process_queue = []

    # Set to keep track of processes already arrived
    arrived_processes = set()

    while current_time < run_for:
        # Check for arriving processes at the current time
        arriving_processes = [p for p in processes if p.arrival == current_time and p.name not in arrived_processes]
        for p in arriving_processes:
            timeline.append((current_time, f"{p.name} arrived"))
            process_queue.append(p)
            arrived_processes.add(p.name)  # Mark process as arrived

        # If there are processes in the queue, schedule the next one
        if process_queue:
            current_process = process_queue.pop(0)
            if current_process.response_time == -1:
                current_process.response_time = current_time - current_process.arrival
            timeline.append((current_time, f"{current_process.name} selected (burst {current_process.burst})"))

            # Run the process for its burst duration
            for _ in range(current_process.burst):
                current_time += 1

                # Check for additional arriving processes during the burst
                arriving_processes = [p for p in processes if p.arrival == current_time and p.name not in arrived_processes]
                for p in arriving_processes:
                    timeline.append((current_time, f"{p.name} arrived"))
                    process_queue.append(p)
                    arrived_processes.add(p.name)  # Mark process as arrived

                if current_time >= run_for:
                    break

            # Process finishes
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival
            current_process.waiting_time = current_process.turnaround_time - current_process.burst
            completed_processes.append(current_process)
            timeline.append((current_time, f"{current_process.name} finished"))

        else:
            # No process in the queue, system is idle
            timeline.append((current_time, "Idle"))
            current_time += 1

    return timeline, completed_processes


def write_output(filename, timeline, completed_processes, run_for):
    with open(filename, 'w') as file:
        file.write(f"{len(completed_processes)} processes\n")
        file.write("Using First Come First Served\n")
        for time, event in timeline:
            file.write(f"Time {time:3} : {event}\n")
        file.write(f"Finished at time {run_for}\n\n")

        # Sort processes by name before writing their stats
        for process in sorted(completed_processes, key=lambda p: p.name):
            file.write(f"{process.name} wait {process.waiting_time} "
                       f"turnaround {process.turnaround_time} "
                       f"response {process.response_time}\n")


def main():
    if len(sys.argv) < 2:
        print("Please provide the input file name ending with .in")
        return

    input_filename = sys.argv[1]

    if not input_filename.endswith('.in'):
        print("Invalid input file. The file name must end with .in")
        return

    output_filename = input_filename.replace('.in', '.out')

    process_count, run_for, algorithm, processes = read_input(input_filename)

    if algorithm == 'fcfs':
        timeline, completed_processes = fifo_scheduling(processes, run_for)
        write_output(output_filename, timeline, completed_processes, run_for)
    else:
        print("Unsupported algorithm. This program only supports FIFO (FCFS) scheduling.")


if __name__ == "__main__":
    main()
