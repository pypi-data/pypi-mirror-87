# runmonitor_RIFT

A dedicated repository for the RIFT run monitor code, previously kept at https://git.ligo.org/richard.udall/miscellaneous-scripts/-/tree/master/runmon

riables**; ``RUNMON_BASE`` (path to top level directory), ``RUNMON_CLUSTER`` (local short cluster name)

```
* File structure
 * Event ID (sid)
   *  cluster:run_path_prefix
     * dag_id.txt
        * convergence.txt  # iteration number, convergence, length of all.net.   See 'summarize-runs.sh
        * extrinsic_exists.txt # if present, it exists. Contents is length of file
        * where_on_current_cluster.txt # if present, this is on the CURRENT cluster. Provides path to the run directory
        * job_status.txt # complete, failed, stuck
        * run_description.txt # created at start, idea is to keep track of why this run was done

```


Tasks
* create_new_run : pathname  sid/cluster:path
* local_checkup
   * check up individual run
   * Loop over all files, if on current cluster, update status
* reporting
  * where_are_my_runs.txt  # list of clusters and paths and/or web directories.  One file for all users?
  * archived_run_microstatus.txt # non-authoritative copy of 'which runs exist' -- list of run paths and status. Can check to see if new runs needed, etc.
  * provide reports about runs -- probably weird mix of python and shell scripts
  * Script created to add a run to archived_runs_microstatus.txt, but the job status must be updated periodically. Maybe incorporate into checkup scripts?


# Pipeline Flow Sketch:

1. Initialize run monitoring directory:
    * Inputs: run directory, ...
    * Outputs: public directory with files: convergence.txt, extrinsic\_exists.txt, where\_on\_cluster.txt, job\_status.txt,run\_description.txt
2. Update mondir files with rundir information:
    * Inputs: monitoring directory --> run directory --> *\_samples.dat, *\_.sub, dag files, ...
    * Outputs: updates to files in 1.b.
3. Update metafiles:
    * Inputs: monitoring files from 1.b.
    * Outputs: updates to where\_are\_my\_runs.txt and archived\_run\_microstatus.txt
4. Repeat 2&3 at intervals

# Reporting Details:

1. Call get_report.sh:
    * Inputs: The run to look for and the cluster the run is on (CIT, LHO, LLO, etc...)
2. If the cluster the run is on is not the same as the current cluster, then get_cluster.py is called:
    * Inputs: The cluster the run is on
    * Outputs: The path that will be gsisshed into
3. Call report.py inside correct cluster:
    * Inputs: Run name, the path to the head of runmon, the current cluster
    * Outputs: A report with run path, job status, run description, convergence info, and extrinsic info

Additional information:
* update_archive.py: Updates archived_runs_microstatus.txt with a run
    * Inputs: Run name, event, runmon base, and current cluster
    * Outputs: No outputs, just adds new run to archived_runs_microstatus.txt


# Formatting Conventions and Code Key
## Formatting:
### convergence.txt
* Lines are appended at each run of the update code
* 4 tab delimited elements:
    * Time stamp (GMT ascii from time module)
    * Most recent iteration number
    * Convergence value
    * Number of points in all.net

### job\_status.txt
* Lines are appended at each run of the update code
* 2 tab delimited elements
    * Time stamp (GMT ascii from time module)
    * Condor report status (or other integer outputs, see below)

### extrinsic\_exists.txt
* Only one element, the number of extrinsic points
* If this file exists, the run has completed

### dag\_id.txt
* Only one element, the most recent dag id (obtained from marg...dagman.log)

## Integer (or Float) Keys:
### convergence.txt
* 10000000 --> No convergence information can be read
* Any other number is the actual convergence data (currently from test-*.out, could be js in the future)

### job\_status.txt
* 100000 --> still running
* 200000 --> *.dag.dagman.out unreadable
* 0 --> a success error code
* 1 --> job failure error code
* 2 --> job aborted code
* other numbers --> error codes from other cases



# Usage and Setup:
1. Create a public runmon directory (e.g. `~/public_html/RUNMON`) and set this as `RUNMON_BASE`, then also set `RUNMON_CLUSTER`
2. Create a directory in RUNMON_BASE named daemon
3. Run setup on the events of interest
* Currently whether one should use `create_new_run.sh` or `store_rift_analysis.sh` depends on a) the formatting of the rundir, with the prior being useful if it is `descriptive_name/rundir/*` and the latter being useful if it is just `descriptive_name/*` and b) whether one wishes to start the run as an integrated portion of creating the runmon directory
* We can hammer out this inconsistency later
4. If one wants to manually test the components used by the daemon, one can follow input instructions for `check_up.py` and `update_archive.py`
5. To start the daemon, one runs `python check_daemon.py --rmdir {RUNMON_BASE}`, and once per hour it will automatically a) update each run with check\_update.py, unless the run has completed and b) updates the archived\_runs\_microstatus.txt to reflect the current nature of the run.
* To specify which directories in RUNMON\_BASE are event directories, add the file event\_list.txt, containing the exact names of the desired directories, one per line, and then pass the option --event-list to check_daemon
# Reporting Instructions:
1. Make sure that report.py, event_runs.sh, list_events.sh, and get_cluster.py are present in RUNMON_BASE.
* For now the scripts rely on the runmon paths being the same across clusters.
* We can also add the copying of these scripts over to RUNMON_BASE in a script such as store_rift_analysis.sh.
2. If you want a report for a single event, call get_report.sh with the run name and the cluster it's on as arguments. It will gsissh into the correct cluster if necessary, and write to stdout the info with a header. Pass in "no_header" as a third argument if you wish to not have a header.
3. If you want a report for all the runs of a certain event, call event_report.sh with the event ID and the cluster it's on as arguments. It will first obtain a list of all the runs using event_runs.sh. It will then call get_report.sh on each event, writing the whole thing with a header to stdout. If a header isn't wanted, pass in "no_header" as a third argument.
* I currently have it set so that event_report.sh requires get_report sh to be in the same directory. If it is preferable, I can change it so that there is a copy of get_report.sh in RUNMON_BASE, and have event_report.sh use that instead.
4. If you want a report for all runs in a cluster, use full_report.sh. It will call list_events.sh first, and then call event_report.sh on each event, thus writing everything to stdout.
* This is set to have event_report.sh and get_report.sh in the same directory. I can make a similar change to event_report.sh if that would be preferable.


