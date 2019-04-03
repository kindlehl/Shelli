"""
Module for logging output. Supports nice colors.
"""

import sys
import copy
from termcolor import colored, cprint

LOGGER_FILL_SIZE = 0

# This array contains all colors
ORIGINAL_COLORS = [
    'red',
    'cyan',
    'green',
    'blue',
    'magenta',
    'yellow',
    'white',
]

# Increases every time a new color is allocated. Used to index into color array
COLORS_TAKEN = 0

# Contains {datum: color}
COLOR_MAP = {}

# Cycle colors so everyone gets a unique color :)
def allocate_color(datum):
    global ORIGINAL_COLORS
    return ORIGINAL_COLORS[hash(datum) % len(ORIGINAL_COLORS)]

# Gets color for item 'datum'. For example, datum is the hostname
# when printing a command when being run on a given host.
def get_color(datum):
    if datum not in COLOR_MAP.keys():
        COLOR_MAP[datum] = allocate_color(datum)
    return COLOR_MAP[datum]

def report(hostname, message):
    global LOGGER_FILL_SIZE
    # Print message at left margin in brackets
    prompt_header = "[{}]".format(hostname)

    # Set fill size and left alignment
    format_string = "{: <" + str(LOGGER_FILL_SIZE + 4) + "}"
    prompt_header = format_string.format(prompt_header)
    prompt = prompt_header + message + '\n'
    logline = colored(prompt, get_color(hostname))
    sys.stderr.write(logline)
    
def configure_from_target(target):
    global LOGGER_FILL_SIZE

    hostgroups = target.hostgroups
    for group in hostgroups.values():
        for host in group.hosts.values():
            if len(str(host)) > LOGGER_FILL_SIZE:
                LOGGER_FILL_SIZE = len(str(host))
