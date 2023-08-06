#!/usr/bin/env bash

#It's a simple script used to find all the event IDs in the runmon base. It's used by full_report.sh.

BASE=$1

cd $BASE

for d in */; do
	if [ "$d" != "daemon/" ]; then
		echo ${d:0:-1}
	fi
done
