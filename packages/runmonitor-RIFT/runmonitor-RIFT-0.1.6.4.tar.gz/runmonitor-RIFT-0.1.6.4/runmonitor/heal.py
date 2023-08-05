#!/usr/bin/env python

import os
import glob

def check_error(rd=None):
	linelist = get_linelist(rd)

	error_file = linelist[8].split()[5].strip()
	print(error_file)
	return error_file

def get_job_id(rd=None):
	linelist = get_linelist(rd)

	job_id = linelist[7].split()[5].split(".")[0].strip("(").strip()
	print(job_id)
	return job_id

def get_linelist(rd=None):
	linelist = []

        if (rd == None):
		rd = os.getcwd()

	dagman = open(os.path.join(rd,"marginalize_intrinsic_parameters_BasicIterationWorkflow.dag.dagman.out"))
	dag_list = dagman.readlines()[::-1]
	dagman.close()

	for line in dag_list:
		linelist.append(line)
		if ("ERROR: the following job(s) failed" in line):
			break
		else:
			if (len(linelist) > 12):
			linelist.pop(0)

	linelist = linelist[::-1]
	return linelist

def check_effective_samples_error(iteration,rd=None):
	import glob
	import sys

	if rd == None:
		rd = os.getcwd()

	filename = glob.glob(rd+"/iteration_" + str(iteration) + "_cip/logs/cip*.err")[0]
	err = open(filename)
	err_lines = err.readlines()
	err.close()

	for item in err_lines[::-1]:
        	if ("Effective samples = nan" in item):
                	print(True)
                	return True
	print(False)
	return False

def get_ile_job(rd=None):
	check_error(rd)

def identify_slot(job_id,process_id)
	cmd = ["condor_history",cluster+"."+process,"-limit","1","-af","LastRemoteHost"]
	histpipe = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	out,err = histpipe.communicate()
	return out


def check_encodings_error(iteration, job_id,rd=None,check_node=False):
	import sys
	
	if rd == None:
		rd = os.getcwd()
             

	filenames = glob.glob(rd+"/iteration_" + str(iteration) + "_ile/logs/ILE*" + str(job_id) + "*.err")

	for fname in filenames:
		err = open(fname)
		err_lines = err.readlines()
		err.close()

		for item in err_lines[::-1]:
			if ("No module named 'encodings'" in item):
				print(True)
				if check_node:
					process = fname.split(".")[0].split("-")[-1]
					print(identify_slot(job_id,process))
				return True
	print(False)
	return False

	add_req(rd,slot)
