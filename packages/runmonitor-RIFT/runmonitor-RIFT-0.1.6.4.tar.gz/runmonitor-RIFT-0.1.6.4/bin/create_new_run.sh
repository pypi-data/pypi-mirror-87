#!/usr/bin/env bash
#./create_new_run.sh event_sid run_path "run_description"

event_id=$1
shift
run_path=$1
shift
run_desc=$1
shift

if [ -z ${RUNMON_BASE} ]; then
  RUNMON_BASE=`pwd`
fi
if [ -z ${RUNMON_CLUSTER} ]; then
  RUNMON_CLUSTER=FAKE
fi

cd ${run_path}
condor_submit_dag marginalize_intrinsic_parameters_BasicIterationWorkflow.dag
cd ..
path_to_store=`pwd`

echo ${path_to_store} #this should avoid the issue of run_prefix being "rundir"

cd ${RUNMON_BASE}

store_rift_analysis.sh ${event_id} ${path_to_store} ${run_desc}
run_prefix=`echo ${path_to_store} | tr '/' ' ' | awk '{print $NF}' `

check_rift_analysis.sh ${event_id} ${RUNMON_CLUSTER} ${run_prefix}
touch ${event_id}/${RUNMON_CLUSTER}:${run_prefix}/job_status.txt