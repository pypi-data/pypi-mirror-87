
The ``pyPM.ca`` population modeller (www.pyPM.ca) describes connected systems with
discrete-time difference equations. It was developed specifically
to understand and characterize the CoViD-19 epidemic.

A ``pyPM.ca`` model is built by connecting a set of population objects with
connector objects. The connectors represent either a transfer that occurs
immediately at the next time step
or one which is delayed and distributed in time. Each
population object retains a record of its size at each time step, and also
maintains a list of future contributions, arising from delayed transfers
from other populations.
Calculations of population size are done either in terms of expectation values 
or simulated data,
allowing the model to be used for both analysis and simulation.


