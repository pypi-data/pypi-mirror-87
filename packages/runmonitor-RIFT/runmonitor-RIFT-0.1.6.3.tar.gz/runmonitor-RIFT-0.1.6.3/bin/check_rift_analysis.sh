#! /bin/bash
#
# ARGUMENTS:  event cluster path 
#
# ENVIRONMENT VARIABLES:
#      RUNMON_BASE  : path to base of directory tree. Default is ''
#      RUNMON_CLUSTER:  short name of cluster (CIT,LHO,LLO, ...). Default is 'FAKE'


# Set default variable
if [ -z ${RUNMON_BASE} ]; then
  RUNMON_BASE=`pwd`
fi


event_sid=$1; shift
cluster=$1; shift
my_prefix=$1; shift

name_dir= ${event_sid}/${cluster}:${my_prefix}
if [ ! -d ${name_dir} ]; then
  exit 1
fi
cd ${name_dir}

# If not on current cluster, need *remote* update, not yet implemented
if [ ! -e where_on_current_cluster.txt ]; then
  exit 0
fi

HERE=`pwd`
cd `cat where_on_current_cluster.txt`

# DAG id
dag_job_id=`tail -n 100 marginalize_intrinsic_parameters_BasicIterationWorkflow.dag.dagman.log | grep Job | awk '{print $2}' | tr '(' ' ' | tr '.' ' ' | awk {print $1}`
echo ${dag_job_id} > ${HERE}/dag_id.txt

# convergence status
echo `ls posterior_samples*.dat` `cat iter*test/logs/*.out | tail -n 1`  `wc -l all.net`  > ${HERE}/convergence.txt

JOB_STATUS=unknown

if [ -e extrinsic_posterior_samples.dat ]; then
  touch ${HERE}/extrinsic_exists.txt
  JOB_STATUS=done
fi
