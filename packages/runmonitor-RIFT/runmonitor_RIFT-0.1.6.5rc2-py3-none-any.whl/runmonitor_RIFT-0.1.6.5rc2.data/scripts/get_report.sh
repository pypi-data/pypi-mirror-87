#!/usr/bin/env bash

#Takes in a run and the cluster it's on, and then no matter what location or what cluster you're on, it will call the script to create a report of the run. It will gsissh into the correct cluster if not already there, and then run report.py and echo the output with a header. If a header isn't desired, simply pass in "no_header" as a third argument.

RUN=$1
CLUSTER=$2
HEADER=$3

if [ "$HEADER" != "no_header" ]; then
	echo -e "Time_of_Report\tEvent\tRun\tRun_Path\tDag_ID\tJob_Status\tIteration_Number\tConvergence\tLength_of_all.net\tDoes_Extrinsic_Exist\tNumber_of_Extrinsic_Points\tRun_Description"
fi

#If different cluster, run scripts in that cluster
if [ $CLUSTER = $RUNMON_CLUSTER ]; then
	echo "$(rmutil_report.py --run $RUN --base $RUNMON_BASE --cluster $RUNMON_CLUSTER)"
else #Relies on RUNMON_BASE being the same across clusters
	CLUSTER_SSH=$(rmutil_getcluster.py --cluster $CLUSTER)
	echo "$(gsissh -p 2222 $CLUSTER_SSH rmutil_report.py --run $RUN --base $RUNMON_BASE --cluster $CLUSTER)"
fi
