#!/usr/bin/env python3

#Name: Sabeer Sekhon
#Course: OPS445

import argparse
import subprocess
import sys

def parse_command_args():
    """
    Parses command-line arguments using argparse.
    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="DU Improved -- See Disk Usage Report with bar charts",
        epilog="Copyright 2023"
    )
    
    parser.add_argument("-H", "--human-readable", action="store_true", help="Print sizes in human readable format (e.g., 1K 23M 2G)")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    parser.add_argument("target", type=str, nargs='?', default='.', help="The directory to scan.")

    return parser.parse_args()

def call_du_sub(target: str) -> list:
    """
    Executes the 'du' command for the target directory with a max depth of 1.
    Args:
        target (str): The directory to scan with 'du'.
    Returns:
        list: A list of strings representing the output of 'du'.
    """
    try:
        result = subprocess.run(['du', '-d', '1', target], stdout=subprocess.PIPE, text=True, check=True)
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        print(f"Error running 'du' on {target}: {e}", file=sys.stderr)
        return []

def percent_to_graph(percent: float, length: int = 20) -> str:
    """
    Converts a percentage (0.0 - 100.0) to a bar graph string of specified length.
    Args:
        percent (float): The percentage to convert, expected between 0.0 and 100.0.
        length (int): The total number of characters in the bar graph.
    Returns:
        str: The bar graph as a string of equal signs and spaces.
    """
    if percent < 0.0 or percent > 100.0:
        raise ValueError("Percent must be between 0.0 and 100.0")
    
    num_equals = int(round((percent / 100) * length))
    num_spaces = length - num_equals
    
    return '=' * num_equals + ' ' * num_spaces

def create_dir_dict(du_output: list) -> dict:
    """
    Converts the output from 'du' into a dictionary with directory paths as keys
    and their respective sizes in bytes as values.
    Args:
        du_output (list): A list of strings, where each string is formatted as "size\tpath".
    Returns:
        dict: A dictionary with paths as keys and sizes as integer values.
    """
    dir_dict = {}
    for entry in du_output:
        size, path = entry.split('\t')
        dir_dict[path] = int(size)
    return dir_dict

def bytes_to_human_readable(size_in_bytes: int) -> str:
    """
    Converts bytes to a human-readable format (e.g., KiB, MiB, GiB).
    Args:
        size_in_bytes (int): The size in bytes.
    Returns:
        str: The human-readable size string.
    """
    suffixes = ['B', 'KiB', 'MiB', 'GiB', 'TiB']
    size = size_in_bytes
    for suffix in suffixes:
        if size < 1024:
            return f"{size:.2f} {suffix}"
        size /= 1024
    return f"{size:.2f} PiB"

if __name__ == "__main__":
    args = parse_command_args()
    
    if not args.target:
        print("Error: Target directory not specified.")
        sys.exit(1)
    
    du_output = call_du_sub(args.target)
    if not du_output:
        print(f"Error: Failed to retrieve disk usage information for {args.target}.")
        sys.exit(1)

    dir_dict = create_dir_dict(du_output)
    total_size = sum(dir_dict.values())

    for path, size in dir_dict.items():
        percent = (size / total_size) * 100 if total_size > 0 else 0
        graph = percent_to_graph(percent, args.length)

        if args.human_readable:
            size_str = bytes_to_human_readable(size)
            total_str = bytes_to_human_readable(total_size)
        else:
            size_str = f"{size} B"
            total_str = f"{total_size} B"

        print(f"{percent:>3.0f}% [{graph}] {size_str}\t{path}")

    print(f"Total: {total_str}   {args.target}")
