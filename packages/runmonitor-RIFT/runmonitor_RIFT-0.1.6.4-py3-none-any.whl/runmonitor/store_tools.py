#!/usr/bin/env python
import os
import shutil
import sys
from runmonitor import environ_check

def create_envinfo():
    binpath = os.path.join(*sys.executable.split("/")[:-1])
    activatepath = os.path.join(binpath,"activate")
    accounting = os.environ["LIGO_ACCOUNTING"]
    username = os.environ["LIGO_USER_NAME"]
    laldatapath = os.environ["LAL_DATA_PATH"]
    if laldatapath=="":
        laldatapath="''"
    gwsurrogate = os.environ["GW_SURROGATE"]
    if gwsurrogate=="":
        gwsurrogate="''"
    with open("envinfo.sh",'w') as f:
        f.write("source "+activatepath+"\n")
        f.write("export LIGO_ACCOUNTING="+accounting+"\n")
        f.write("export LIGO_USER_NAME="+username+"\n")
        f.write("export LAL_DATA_PATH="+laldatapath+"\n")
        f.write("export GWSURROGATE="+gwsurrogate+"\n")

def store(event,rundir,level=1,rmbase=None,cluster=None,envsh=None):
    if rmbase == None:
        rmbase = os.environ['RUNMON_BASE']
    if cluster == None:
        cluster = os.environ['RUNMON_CLUSTER']
    print(rundir.strip("/").split("/"))
    name = rundir.strip("/").split("/")[-1*level]
    if event not in os.listdir(rmbase):
        os.mkdir(os.path.join(rmbase,event))
    rmdir = os.path.join(rmbase,event,cluster+":"+name)
    try:
        os.mkdir(rmdir)
        with open(os.path.join(rmdir,"where_on_current_cluster.txt"),'w') as f:
            f.write(rundir)
        if envsh != None:
            shutil.copy(envsh,os.path.join(rmdir,"envinfo.sh"))
        elif envsh == "generate":
            create_envinfo() 

    except Exception as fail:
        print("unable to initialize runmon directory:")
        print(fail)

