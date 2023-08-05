import os 
import subprocess
import glob

def search_files(fname_key,contents_key,basedir=None,repsample=10):
    """
Inputs:
fname_key = a selector to only search for files satisfying a certain filenamecondition e.g. *.out files
contents_key = an error message keyword to search for
basedir = the base directory to be searching through (e.g. rundir/iteration_0_ile/logs/)
repsample = the size of a representative sample. You do not want to loop over every single ILE-*.out
---------------
Outputs:
a list repsample elements long, containing the name of the failed file
    """
    ocwd = os.getcwd()
    os.chdir(basedir)
    cmd = ["grep",f"{contents_key}"]
    cmd.extend(glob.glob(f"{basedir}/*{contents_key}*"))
    print(basedir)
    print(glob.glob(f"{basedir}/*{contents_key}*"))
    print(cmd)
    greppipe= subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    out,err = greppipe.communicate()
    os.chdir(ocwd)
    print(out)
    print(err)

search_files("py","i",basedir=os.getcwd())
