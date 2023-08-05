#!/usr/bin/env bash
#Small script to see what iteration the run is on. It's run in the run directory.

NUM=$(ls posterior_samples-*.dat | wc -l)

echo $NUM
