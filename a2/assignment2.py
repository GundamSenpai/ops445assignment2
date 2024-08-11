#!/usr/bin/env python3

#Name : Sabeer Sekhon
#Course: OPS445


import argparse
import os
import sys

def parse_command_args() -> object:
    """
    Set up argparse here. Call this function inside main.
    Returns:
    argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Memory Visualiser -- See Memory Usage Report with bar charts",
        epilog="Copyright 2023"
    )
    
    parser.add_argument("-H", "--human-readable", action="store_true", help="Prints sizes in human readable format")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    parser.add_argument("program", type=str, nargs='?', help="If a program is specified, show memory use of all associated processes. Show only total use if not.")

    args = parser.parse_args()

    return args

def percent_to_graph(percent: float, length: int = 20) -> str:
    """
    Converts a percentage (0.0 - 1.0) to a bar graph string of specified length.

    Args:
    percent (float): The percentage to convert, should be between 0.0 and 1.0.
    length (int): The total number of characters in the bar graph.

    Returns:
    str: The bar graph as a string of hashes and spaces.
    """
    # Placeholder logic to be refined
    num_hashes = int(percent * length)
    num_spaces = length - num_hashes
    return '#' * num_hashes + ' ' * num_spaces

def get_sys_mem() -> int:
    """
    Returns the total system memory in kilobytes by reading /proc/meminfo.
    """
    with open('/proc/meminfo', 'r') as file:
        for line in file:
            if line.startswith('MemTotal:'):
                return int(line.split()[1])
    return 0  # Temporary return for draft stage

def get_avail_mem() -> int:
    """
    Returns the available memory in kilobytes by reading /proc/meminfo.
    """
    with open('/proc/meminfo', 'r') as file:
        for line in file:
            if line.startswith('MemAvailable:'):
                return int(line.split()[1])
    return 0  # Temporary return for draft stage

def pids_of_prog(app_name: str) -> list:
    """
    Returns a list of process IDs (PIDs) for a given program name using pidof.
    """
    # Placeholder implementation
    try:
        pids = os.popen(f'pidof {app_name}').read().strip()
        return [int(pid) for pid in pids.split()]
    except:
        return []

def rss_mem_of_pid(proc_id: str) -> int:
    """
    Returns the total RSS memory used by a process with a given PID by reading /proc/<pid>/smaps.
    """
    total_rss = 0
    try:
        with open(f'/proc/{proc_id}/smaps', 'r') as file:
            for line in file:
                if line.startswith('Rss:'):
                    total_rss += int(line.split()[1])
    except:
        pass  # Placeholder exception handling
    return total_rss

def bytes_to_human_r(kibibytes: int, decimal_places: int = 2) -> str:
    """
    Converts kilobytes to a human-readable format (KiB, MiB, GiB, etc.).
    """
    # Rough implementation to be refined
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']
    suf_count = 0
    result = kibibytes

    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1

    return f"{result:.{decimal_places}f} {suffixes[suf_count]}"

if __name__ == "__main__":
    args = parse_command_args()

    if not args.program:  # When no program is specified, show total memory usage
        total_memory = get_sys_mem()
        available_memory = get_avail_mem()
        used_memory = total_memory - available_memory

        # Placeholder print statement
        print(f"Memory         [{percent_to_graph(used_memory / total_memory, args.length)}| {used_memory / total_memory:.0%}] {used_memory}/{total_memory}")
    
    else:  # When a program is specified, show memory usage for each process
        pids = pids_of_prog(args.program)
        if not pids:
            print(f"{args.program} not found.")
            sys.exit(1)
        
        for pid in pids:
            rss_memory = rss_mem_of_pid(str(pid))
            # Placeholder print statement
            print(f"{pid:<10} [{percent_to_graph(rss_memory / get_sys_mem(), args.length)}| {rss_memory / get_sys_mem():.0%}] {rss_memory}/{get_sys_mem()}")

        # Summarize total RSS memory for the program
        total_rss_memory = sum(rss_mem_of_pid(str(pid)) for pid in pids)
        # Placeholder print statement
        print(f"{args.program:<10} [{percent_to_graph(total_rss_memory / get_sys_mem(), args.length)}| {total_rss_memory / get_sys_mem():.0%}] {total_rss_memory}/{get_sys_mem()}")
