#!/usr/bin/env bash

#This script gives a report with a header of every run on a cluster. It works by iterating through all the events, and calling event_report.sh on it.

CLUSTER=$1

if [ $CLUSTER = $RUNMON_CLUSTER ]; then
	EVENT_LIST=$(rmutil_getevents.py --base $RUNMON_BASE)
else
	CLUSTER_SSH=$(rmutil_getcluster.py --cluster $CLUSTER)
	EVENT_LIST=$(gsissh -p 2222 $CLUSTER_SSH rmutil_getevents.py --base $RUNMON_BASE)
fi

echo -e "Time_of_Report\tEvent\tRun\tRun_Path\tDag_ID\tJob_Status\tIteration_Number\tConvergence\tLength_of_all.net\tDoes_Extrinsic_Exist\tNumber_of_Extrinsic_Points\tRun_Description"

for EVENT in $EVENT_LIST; do
	echo "$(event_report.sh $EVENT $CLUSTER "no_header")"
done
