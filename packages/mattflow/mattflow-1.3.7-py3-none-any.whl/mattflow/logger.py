# logger.py is part of MattFlow
#
# MattFlow is free software; you may redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. You should have received a copy of the GNU
# General Public License along with this program. If not, see
# <https://www.gnu.org/licenses/>.
#
# (C) 2019 Athanasios Mattas
# ======================================================================
"""Handles the logging precess."""

from datetime import datetime, timedelta
import os

from mattflow import config as conf
from mattflow import __version__, __author__, __license__


file_name = str(datetime.now())[:19]
# Replace ':' with '-' for compatibility with windows file formating.
file_name = file_name.replace(':', '-').replace(' ', '_') + ".log"
version_msg = 'MattFlow v' + __version__
author_msg = 'Author: ' + __author__ + ', 2019'
license_msg = __license__


def log(state):
    """Appends a state-message at a new line of the log file.

    If a log file does not exist, it creates one, printing the simulation info.

    Args:
        state (str) : the string to be logged
    """
    if not conf.LOGGING_MODE:
        return
    open_log = find_open_log()

    if open_log:
        # Append the state.
        with open(open_log, 'a') as fa:
            fa.write(state + '\n')
        # Update log name with the current time.
        os.rename(open_log, file_name)
    else:
        fw = open(file_name, 'w')
        fw.write(
            version_msg + '\n' + author_msg + '\n' + license_msg + '\n'
            + len(license_msg) * '-' + '\n'
            + str(datetime.now())[:19] + '\n\n'
            + 'Configuration of the simulation' + '\n'
            + 31 * '-' + '\n'
            + 'Number of cells        : ' + str(conf.Nx * conf.Ny) + '\n'
            + 'Number of ghost cells  : ' + str(conf.Ng) + '\n'
            + 'Courant number         : ' + str(conf.COURANT) + '\n'
            + 'Simulation mode        : ' + str(conf.MODE) + '\n'
            + 'Boundary conditions    : ' + str(conf.BOUNDARY_CONDITIONS) + '\n'
            + 'Solver type            : ' + str(conf.SOLVER_TYPE) + '\n'
            + 'Plotting style         : ' + str(conf.PLOTTING_STYLE) + '\n\n')

        fw.write(state + '\n')
        fw.close()


def log_timestep(it, time):
    """Appends timestep info to the log file."""
    if not conf.LOGGING_MODE:
        return
    if (it == 1) | (it % 15 == 0):
        log("  iter     time")
    log(f"{it: >{6}d}    {time:0.3f}")


def find_open_log():
    """Returns the 1st encountered open log file (False if there isn't one).

    An open log file is a mattflow log that does not end with '_done.log'.
    """
    working_dir = os.getcwd()
    files_list = []
    files_list = [f for f in os.listdir(working_dir)
                  if f.endswith(".log") and is_open(f) and is_mattflow_log(f)]
    if files_list:
        return files_list[0]
    return False


def close():
    """Closes the log file, appending '_done' to the file name."""
    if not conf.LOGGING_MODE:
        return
    try:
        open_log = find_open_log()
        if open_log:
            # append blank line
            with open(open_log, 'a') as fa:
                fa.write('\n')
            # append '_done' at the file name
            os.rename(open_log, file_name[:-4] + '_done'
                      + file_name[-4:])
        else:
            fw = open(file_name, 'w')
            fw.write('Trying to close a log file that does not exist...\n\n')
            os.rename(open_log, file_name[:-4] + '_errored'
                      + file_name[-4:])
            fw.close()
    except TypeError:
        fw = open(file_name, 'w')
        fw.write('Trying to close a log file that does not exist...\n\n')
        os.rename(open_log, file_name[:-4] + '_errored'
                  + file_name[-4:])
        fw.close()


def is_open(log_file: str):
    """Checks whether a log file object is open or not."""
    if isinstance(log_file, str) and log_file[-9:] != '_done.log':
        return True
    return False


def is_mattflow_log(log_file: str):
    """Checks whether a log file was generated from MattFlow or not."""
    with open(log_file, 'r') as fr:
        first_word = fr.read(8)
    if first_word == 'MattFlow':
        return True
    return False


def log_duration(start, end, process):
    """Logs the duration of a process."""
    process_name = {
        "main": "Total",
        "simulate": "Solution",
        "createAnimation": "Post-processing"
    }
    if process in process_name:
        process = process_name[process]
    prefix = f"{process.capitalize()} duration"
    duration = timedelta(seconds=end - start)
    log(f"{prefix:-<30}{duration}"[:40])
