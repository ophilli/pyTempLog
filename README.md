# pyTempLog

This is a collection of scripts that I am using to administer the Octoprint based printers in the Clemson Makerspace.
They are also an opportunity for me to explore utilizing RESTful APIs in real-world applications with Python.

tempGet.py connects to the database referenced in secrets.cfg and stores the temperature data from all of the printers listed in hosts.
This could be very useful for diagnosing thermistor failure, or other temperature anomalies. Eventually I plan to write a script that graphs all of this data - but that's a project for another day.

The rest of the scripts contained in this repo are used to issue specific tool commands to the printers. These commands can be very useful when trying to do normal maintenance tasks.
