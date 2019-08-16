import sys
import os
import json

import pandas as pd

from args import is_arg_passed, get_valued_arg


def print_usage(show_help_line=False):
    """ Prints the short help card for the program.
    Args:
        show_help_line (bool): If true, information on help flag `-h` will be printed.
    """
    print("Usage: python combine.py [-h] [-o <outfile>] <infile1> <infile2>")
    print("Combines two password data dumps together.")
    if show_help_line:
        print("For extended help use '-h' option.")


def print_help():
    """ Prints the full help card for the program.
    """
    print_usage()
    print("Options:")
    print("\t-h: Show this help screen")
    print('\t-o <str>: The file in which to place output')
    print()
    print("Input files should be in format:")
    print("\tpassword, frequency, ... <- Column headers")
    print("\t\"123456\", 1, ...")
    print("\t\"password\", 18, ...")
    print("\t\"matrix\", 14, ...")
    print("Output will be in CSV format.")


# If no options specified, print usage and exit.
if len(sys.argv) == 1:
    print_usage(True)
    exit(0)

# If help flag specified, print help and exit.
if is_arg_passed('h'):
    print_help()
    exit(0)

# Get output path if one was specified.
out = get_valued_arg('o')

# Last parameter is the raw filename.
raw_file_1 = sys.argv[-1]
raw_file_2 = sys.argv[-2]
if not os.path.isfile(raw_file_1) or not os.path.isfile(raw_file_2):
    emit_err('Input file not found.')
    sys.exit(1)

# Load CSV file.
csv_1 = pd.read_csv(raw_file_1, error_bad_lines=False, skipinitialspace=True)

# Buffer one set of passwords.
buffer = {}
for ind, row in csv_1.iterrows():
    buffer[str(row['password'])] = int(row['frequency'])

def merge_buffer (row):
    """ Merges a password frequency distribution dataframe with the contents of the buffer.

    Args:
        row (Series): The series representing the row to merge.
    Returns:
        Series: The modified series.
    """
    pwd = str(row['password'])
    if pwd in buffer:
        row['frequency'] = int(row['frequency']) + buffer[pwd] # Add to frequency if appropriate.
        buffer.pop(pwd, None) # Remove password from buffer.
    return row

# Load CSV file.
csv_2 = pd.read_csv(raw_file_2, error_bad_lines=False, skipinitialspace=True)
csv_2 = csv_2.apply(merge_buffer, axis=1)

# Append passwords still left in buffer.
for pwd, freq in buffer.items():
    csv_2 = csv_2.append({'password': str(pwd), 'frequency': int(freq)}, ignore_index=True)

# Print data frame.
csv_2.to_csv(out if not out is None else sys.stdout, index=False)
