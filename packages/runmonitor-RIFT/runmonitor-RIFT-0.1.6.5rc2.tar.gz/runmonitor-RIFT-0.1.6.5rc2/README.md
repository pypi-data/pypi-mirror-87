# RIFT run-monitor

A package providing utilities for monitoring and healing runs with [RIFT](https://pypi.org/project/RIFT/). Built from https://git.ligo.org/richard.udall/runmonitor_rift, with original work done at https://git.ligo.org/richard.udall/miscelleaneous-scripts/

Developed by Adhav Arulanandan, Grihith Manchanda, Richard O'Shaughnessy, and Richard Udall

## Installation
This package assumes the user is on an LDAS-like cluster.

To install, do the standard: pip install runmonitor\_rift

Configure environment variables:
* RUNMON\_BASE = a sub-directory in a public-facing directory (e.g. ~/public\_html/RUNMON/)
* RUNMON\_CLUSTER = a designator for a cluster (e.g. CIT)

Some functionality, especially for healing scripts, will work best if this is installed in an environment which also has RIFT installed, though overrides will usually be available.  

