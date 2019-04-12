import sys
import os
import json

import pandas as pd

from model.PasswordSetCharacteristics import PasswordSetCharacteristics

from args import is_arg_passed


def print_usage(show_help_line=False):
    """ Prints the short help card for the program.
    Args:
        show_help_line (bool): If true, information on help flag `-h` will be printed.
    """
    print("Usage: python extractfeatures.py [-h] <dumpfile>")
    print("Extracts features from a password dump formatted as a CSV file.")
    if show_help_line:
        print("For extended help use '-h' option.")


def print_help():
    """ Prints the full help card for the program.
    """
    print_usage()
    print("Options:")
    print("\t-h: Show this help screen")
    print()
    print("Input file should be in format:")
    print("\tpassword, frequency, ... <- Column headers")
    print("\t\"123456\", 1, ...")
    print("\t\"password\", 18, ...")
    print("\t\"matrix\", 14, ...")
    print("Output will be in JSON format to standard output.")


# If no options specified, print usage and exit.
if len(sys.argv) == 1:
    print_usage(True)
    exit(0)

# If help flag specified, print help and exit.
if is_arg_passed('h'):
    print_help()
    exit(0)

# Last parameter is the raw filename.
raw_file = sys.argv[-1]
if not os.path.isfile(raw_file):
    emit_err('Raw data file not found.')
    sys.exit(1)

# Load CSV file.
csv = pd.read_csv(raw_file, error_bad_lines=False, skipinitialspace=True)

# Initialise new characteristics object.
characteristics = PasswordSetCharacteristics()

# Load passwords into characteristics object.
for ind, row in csv.iterrows():
    characteristics.load(str(row['password']), int(row['frequency']))

# Print results as JSON.
print(json.dumps(characteristics.dict()))
