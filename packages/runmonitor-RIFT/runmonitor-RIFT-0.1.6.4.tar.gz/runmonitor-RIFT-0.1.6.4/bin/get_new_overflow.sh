#!/usr/bin/env bash

MAX_COL=$(cat all.net | sort -k10 -n | tail -n 1)
MAX_COL_ARRAY=($MAX_COL)
NUM_DECREASE=50
MAX_VAL=$(echo "${MAX_COL_ARRAY[9]}-$NUM_DECREASE" | bc)
echo $MAX_VAL
