import sys
import json
import math
from functools import reduce

import matplotlib.pyplot as plt

from args import get_valued_arg, is_arg_passed, get_int_valued_arg


def max_key(dict):
    """ Returns the maximum key in an integer-keyed dictionary.

    Args:
        dict (dict): The integer-keyed dictionary.
    Returns:
        int: The maximum key.
    """
    output = 0
    for key, value in dict.items():
        output = max(output, int(key))
    return output


def to_points(dict):
    """ Turns a dictionary of lengths into coordinate pairs.

    Args:
        dict (dict): The length frequency dictionary.
    Returns:
        list of tuple: The coordinate pairs.
    """
    points = []
    for i in range(0, max_key(dict) + 1):
        key = str(i)
        if key in dict:
            points.append((i, dict[key]))
        else:
            points.append((i, 0))
    return points


def print_usage(show_help_line=False):
    """ Prints the short help card for the program.
    Args:
        show_help_line (bool): If true, information on help flag `-h` will be printed.
    """
    print("Usage: python polinfer.py [-hkblutxyos] <features_file>")
    print("Features file produced by extractfeatures.py expected.")
    if show_help_line:
        print("For extended help use '-h' option.")


def print_help():
    """ Prints the full help card for the program.
    """
    print_usage()
    print("Options:")
    print("\t-h: Show this help screen")
    print("\t-k <key>: The key of the feature to use (default: lengthsAccum)")
    print("\t-b <limit>: The threshold to use for outlier detection")
    print("\t-l <limit>: The lower limit of the feature to use (default: 1)")
    print("\t-u <limit>: The upper limit of the feature to use (default: 20)")
    print("\t-t <title>: The chart title")
    print("\t-x <label>: The chart x-axis label")
    print("\t-y <label>: The chart y-axis label")
    print("\t-o <path>: The file in which to place output figure")
    print("\t-s: Suppress chart output")


# If no options specified, print usage and exit.
if len(sys.argv) == 1:
    print_usage(True)
    exit(0)

# If help flag specified, print help and exit.
if is_arg_passed('h'):
    print_help()
    exit(0)

# Get key to use to get dictionary.
key = get_valued_arg('k')
if key is None:
    key = 'lengthsAccum' # Lengths (cumulative) by default.

# Load data file.
raw = {}
with open(sys.argv[-1]) as f:
    raw = json.load(f)[key]

# Read in outlier threshold, if passed.
outlier_threshold = get_int_valued_arg('b')
if outlier_threshold is None:
    outlier_threshold = 2 # Default outlier threshold.

# Read in lower and upper histogram limits, if passed.
low_lim = get_int_valued_arg('l')
if low_lim is None:
    low_lim = 1 # Default lower length limit.
high_lim = get_int_valued_arg('u')
if high_lim is None:
    high_lim = 20 # Default upper length limit.

# Get title/labels.
title = get_valued_arg('t')
if not title is None:
    plt.title(title)
x_label = get_valued_arg('x')
if not x_label is None:
    plt.xlabel(x_label)
y_label = get_valued_arg('y')
if not y_label is None:
    plt.ylabel(y_label)

# Check descent mode.
descent_mode = is_arg_passed('d')

# Convert to points.
points = to_points(raw)
points = list(filter(lambda p: p[0] >= low_lim and p[0] <= high_lim, points)) # Enforce limits.
print('Pulled points:', points)

# Specify offset of critical number.
offset = 1
term = 'Lower'

# Reverse points and invert critical number if in descent mode.
if descent_mode:
    offset = 0
    term = 'Upper'

# Convert to deltas.
deltas = []
for i in range(0, len(points) - 1):
    j = points[i]
    k = points[i + 1]
    if descent_mode:
        mult = math.inf if k[1] == 0 else j[1] / k[1]
    else:
        mult = math.inf if j[1] == 0 else k[1] / j[1]
    deltas.append((j[0], mult))
print('Computed deltas:', deltas)

# Print result.
largest = reduce(lambda i, j: i if i[1] > j[1] else j, deltas)
if largest[1] < outlier_threshold:
    print(f'{term} constraint on', key, 'unlikely to be present in policy.')
else:
    print(f'{term} constraint on', key, 'inferred as', largest[0] + offset)

# Unpack deltas into arrays.
x = [j for j,k in deltas]
y = [k for j,k in deltas]

# Plot scatter diagram.
plt.scatter(x, y, marker='x')

# Remove scientific-format labels.
plt.ticklabel_format(style='plain')
plt.xticks(range(low_lim, high_lim + 1, 2))

# Get output path if one was specified and save file if asked to.
out = get_valued_arg('o')
if out is not None:
    plt.savefig(out)

# Show plot.
if not is_arg_passed('s'):
    plt.show()
