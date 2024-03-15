# PPMS and Keithley Transport Measurements

This codebase includes a number of scripts using MultiPyVu and PyMeasure to automate transport measurements using a Quantum Deisgn Physical Properties Measurement System and a Keithley 2400 sourcemeter. The scripts assume a hallbar test structure has been fabricated on the material. The Keithley is used to control a top gate voltage and the resistivity tensor is measured using the built-in V+, V-, I+, I- contacts of 2 PPMS channels. A Quantum Design multi-function probe is used to allow for the extra DC line running from the Keithley (at room temperature) to the device (as low as 1.8 K).

## Running

To run the code we need to have the following installed on the control computer: Python, MultiVu, MultiPYVu, PyMeasure, PyVISA. MultiVu must be running. We must start the server by running either `run_server.py` or the MultiPyVu GUI. The channels used in the scripts must match those wired to the hallbar device in the PPMS and the GPIB address of the Keithley must match that of the actual 2400. Then we may run our client script, one of the experiments in this repo.

## Testing

To test the code we make use of MultiVu's simulation mode. The MultiVu executable may be started in simulation mode with the appropriate flags.
