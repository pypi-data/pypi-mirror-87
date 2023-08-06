#!/usr/bin/env bash

#This is for getting a list of run reports all from the same event. It needs an event ID and what cluster to access. If you pass in "no_header" as a third argument, it will report the same events without a header. It works by iterating through each directory to get the run name, and then calling get_report.sh on each run.

EVENT=$1
CLUSTER=$2
HEADER=$3

if [ $CLUSTER = $RUNMON_CLUSTER ]; then
	RUN_LIST=$(event_runs.sh $RUNMON_BASE $EVENT)
else
	CLUSTER_SSH=$(rmutil_getcluster.py --cluster $CLUSTER)
	RUN_LIST=$(gsissh -p 2222 $CLUSTER_SSH event_runs.sh $RUNMON_BASE $EVENT)
fi

if [ "$HEADER" != "no_header" ]; then
	echo -e "Time_of_Report\tEvent\tRun\tRun_Path\tDag_ID\tJob_Status\tIteration_Number\tConvergence\tLength_of_all.net\tDoes_Extrinsic_Exist\tNumber_of_Extrinsic_Points\tRun_Description" 
fi

for d in $RUN_LIST; do
	echo "$(get_report.sh $d $CLUSTER "no_header")"
done
