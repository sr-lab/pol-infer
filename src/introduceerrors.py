import pandas as pd
import sys


def print_usage(show_help_line=False):
    """ Prints the short help card for the program.
    Args:
        show_help_line (bool): If true, information on help flag `-h` will be printed.
    """
    print("Usage: python introduceerrors.py [-h] <dumpfile>")
    print("Introduces errors to a password dump formatted as a CSV file.")
    if show_help_line:
        print("For extended help use '-h' option.")


def print_help():
    """ Prints the full help card for the program.
    """
    print_usage()
    print('Arguments:')
    print('\tdumpfile: The file to introduce error into')
    print("Options:")
    print("\t-h: Show this help screen")
    print()
    print("Input file should be in CSV frequency distribution format:")
    print("\tpassword, frequency, ... <- Column headers")
    print("\t\"123456\", 1, ...")
    print("\t\"password\", 18, ...")
    print("\t\"matrix\", 14, ...")
    print("Output will be in CSV format to standard output.")
    print()
    print("Any passwords containing commas or spaces will be split into multiple records.")


# Read in CSV file.
df = pd.read_csv(sys.argv[-1], skipinitialspace=True)

# Print header.
print('password, frequency')

# For each row in dump.
for index, row in df.iterrows():
  fragments = row['password'].split(' ')
  fragments = list(map(lambda x: x.split(','), fragments)) # Split along spaces and commas.
  fragments = [item for sublist in fragments for item in sublist] # Flatten list.
  for fragment in fragments:
    print('"' + fragment.replace('"', '""') + '",', row['frequency']) # Output row.
