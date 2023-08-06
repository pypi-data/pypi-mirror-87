#! /bin/bash
#
# ARGUMENTS:  event_id run_path optional_run_desc.txt
#
# ENVIRONMENT VARIABLES:
#      RUNMON_BASE  : path to base of directory tree. Default is ''
#      RUNMON_CLUSTER:  short name of cluster (CIT,LHO,LLO, ...). Default is 'FAKE'


# Set default variable
if [ -z ${RUNMON_BASE} ]; then
  RUNMON_BASE=`pwd`
fi
if [ -z ${RUNMON_CLUSTER} ]; then
  RUNMON_CLUSTER=FAKE
fi


event_sid=$1
shift
path_to_store=$1
shift
optional_desc=$1  # could be empty

run_prefix=`echo ${path_to_store} | tr '/' ' ' | awk '{print $NF}' `  # may  be bad idea if last directory name is 'rundir' 


cd ${RUNMON_BASE}
mkdir ${event_sid}; cd ${event_sid}
mkdir ${RUNMON_CLUSTER}:${run_prefix}; cd ${RUNMON_CLUSTER}:${run_prefix}
echo ${path_to_store} > where_on_current_cluster.txt
if [ ! -z ${optional_desc} ]; then
  cat ${optional_desc} > run_description.txt
fi

# File structure
#  - where_on_current_cluster.txt 
#  - run_description.txt
#  - dag_id.txt
#  - convergence.txt
#  - extrinsic_exists.txt
