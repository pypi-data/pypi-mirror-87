#!/usr/bin/env bash

ERROR_FILE=$(python -c'from runmonitor import heal; heal.check_error()')

if [[ $ERROR_FILE = ILE.sub ]]; then
	ITERATION=$(ls posterior_samples-*.dat | wc -l)
	JOB_ID=$(python -c'from runmonitor import heal; heal.get_job_id()')
	echo $(python -c"from runmonitor import heal; heal.check_encodings_error($ITERATION, $JOB_ID)")
fi
