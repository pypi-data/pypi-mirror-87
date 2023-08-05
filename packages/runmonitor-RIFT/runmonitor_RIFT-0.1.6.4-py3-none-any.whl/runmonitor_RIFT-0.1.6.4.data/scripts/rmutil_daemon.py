#!python

import os
from runmonitor import daemon_tools as dae
import argparse

#a script wrapper for the daemon initialization - call without arguments to activate default daemon behavior

parser = argparse.ArgumentParser()
parser.add_argument("--rmdir",default=None,type=str,help="The run monitoring ddirectory, defaults to the contents of environment variable RUNMON_BASE")
parser.add_argument("--verbose",action="store_true")
parser.add_argument("--debug",action="store_true")
parser.add_argument("--sender-email",type=str,default="runmonitor.rift.1@gmail.com")
parser.add_argument("--receiver",type=str,default=None,help="the email that updates on runmon should be sent to")
parser.add_argument("--password",type=str,default=None,help="the password for the sender email; if using the default sender email, you can get this from the git.ligo.org wiki for runmonitor")
parser.add_argument("--event-list",action='store_true',help="pass to have the daemon run through a list of event directories labelled event_list.txt in the RUNMON_BASE, rather than trying to guess at them itself")
opts = parser.parse_args()
    
#can pass no arguments and it will pick up on your RUNMON_BASE env
if opts.rmdir == None:
    rmdir = os.environ["RUNMON_BASE"]
else:
    rmdir = opts.rmdir
print("starting daemon")  
          
#starting up the daemon
cdaemon = dae.Main_Daemon(rmdir,el=opts.event_list, verbose=True,debug=True,sender_email=opts.sender_email,receiver=opts.receiver,password=opts.password)
cdaemon.summon()
