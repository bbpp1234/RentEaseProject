# File: timestamp.py
# Group members: rivenl, leylal, chengkac, bangminp

# This file provides a utility function to generate a current timestamp string.
# The timestamp is formatted to include year, month, day, hours, minutes, seconds, and milliseconds.
# No external modules are imported, but it imports the `datetime` module from Python’s standard library.
# This module is used by other scripts to generate timestamps for logging or saving files with unique names.

from datetime import datetime

def generate_timestamp():
    """
    Generate a timestamp in the format yyyy-mm-dd hh:mm:ss
    Return: A string representing the current timestamp without milliseconds.
    """
    # Get the current date and time, formatted as specified, but without milliseconds.
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp without milliseconds

# %%
