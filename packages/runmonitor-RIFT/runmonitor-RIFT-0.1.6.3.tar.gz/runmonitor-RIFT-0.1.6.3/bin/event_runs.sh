#!/usr/bin/env bash

#This is a simple script that simply returns all the events in the runmon directory, used by event_report.sh

BASE=$1
EVENT=$2

cd $BASE/$EVENT

for d in */; do
	temp=${d#*:}
	echo ${temp%?}
done
