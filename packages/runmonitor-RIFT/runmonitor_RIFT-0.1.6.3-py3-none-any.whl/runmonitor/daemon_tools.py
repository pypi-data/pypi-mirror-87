#!/usr/bin/env python

 

import os
from runmonitor import environ_check
from runmonitor import check_tools as chu
from runmonitor import stat_tools as srd
from runmonitor import update_tools as upa
#import logging
import time
import daemon
import subprocess
from daemon import pidfile


# see: http://www.gavinj.net/2012/06/building-python-daemon-process.html, 
# https://stackoverflow.com/questions/13106221/how-do-i-set-up-a-daemon-with-python-daemon
# https://www.python.org/dev/peps/pep-3143/
# note per https://dpbl.wordpress.com/2017/02/12/a-tutorial-on-python-daemon/ the usage in the first link is deprecated --> trying DaemonContext instead
# https://linuxfollies.blogspot.com/2016/11/linux-daemon-using-python-daemon-with.html


class Main_Daemon():
    def __init__(self,rmdir,cluster="CIT",sender_email="runmonitor.rift.1@gmail.com",receiver=None,password=None,el=False,verbose=False,debug=False,attempt_healing=False):
        """
Inputs:
rmdir = the runmon directory

--------
Outputs:
sets up the daemon's attributes (currently not much to do)
        """  
        self.el = el
        self.rmdir = rmdir
        self.cluster = cluster
        self.receiver = receiver
        self.attempt_healing = attempt_healing 
        self.password = password
        self.sender_email = sender_email
        self.log = open(os.path.join(self.rmdir,"daemon/check_daemon.log"),'a')
        self.pidf=os.path.join(self.rmdir,"daemon/check_daemon.pid") 
        """
        using logging package was running into weird OS errors when in DaemonContext, so for now we'll us the inelegant method of just printing to stdout
        self.logger = logging.getLogger('check_daemon')
        self.logger.setLevel(logging.INFO) 
        self.logf = os.path.join(rmdir,"daemon/daemon.log")       
        fh = logging.FileHandler(self.logf)
        fh.setLevel(logging.INFO)
        formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(formatstr)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        """
  
    def summon(self):
        """
inputs:
---------
self

outputs:
---------
Periodically uses check_up.py on all of the public directories, skipping if extrinsic_exists is present or job_status == 0

        """
        #creating the information associated with the daemon
        context = daemon.DaemonContext(stdout = self.log,stderr=self.log,working_directory=self.rmdir,pidfile=pidfile.TimeoutPIDLockFile(self.pidf),umask=0o002)  
        #entering the daemon
        #all prints write to stdout now, and all errors go to stderr
        with context:       
           while True:   
                print("starting update cycle")
                #assuming base/event/run hierarchy, and skipping over the files we know are not events
                #RUNMON should be kept clean, or we should actually keep track of the events (a dedicated textfile maybe?)
                if self.el:
                    with open(os.path.join(self.rmdir,"event_list.txt")) as f:
                        events = [ob.strip("\n") for ob in f.readlines()]
                else:
                    events = [os.path.join(self.rmdir,obj) for obj in os.listdir(self.rmdir) if obj != 'daemon' and obj != 'archived_runs_microstatus.txt']
                runs = []
                #looping over runs
                for event in events:
                    runs = runs + [os.path.join(event,obj) for obj in os.listdir(event)]
                if self.receiver != None and self.password != None:
                    deltas = []
                    print(deltas)
                for run in runs:
                    #checking the time and the job status
                    now = time.asctime(time.gmtime(time.time()))
                    skip_run=False
                    if not os.path.exists(os.path.join(run,"job_status.txt")):
                      chu.update(run)
                    else:
                      lastline = subprocess.check_output(["tail","-n 1",os.path.join(run,"job_status.txt")],text=True).strip()
                      #if the exit was successful or extrinsic_exists exists, it moves on 
                      if lastline.split()[-1] == str(0) or 'extrinsic_exists.txt' in os.listdir(run):
                         print(now + "\t"+"found successful exit, will not update\t"+run)  
                         skip_run=True
                    #otherwise, it updates the logs with chu, and updates the archived_runs_microstatus with upa
                    if not skip_run:
                        print(now + "\t"+"updating logs\t"+run)
                        status = chu.update(run)
                        archive_orig = None
                        if self.receiver != None and self.password != None and os.path.exists(os.path.join(self.rmdir,"archived_runs_microstatus.txt")):
                            with open(os.path.join(self.rmdir,"archived_runs_microstatus.txt"),'r') as f:
                                archive_orig = f.readlines()
                        fullname = run.split("/")[-1]
                        lessername = fullname.split(":")[1]
                        cluster = fullname.split(":")[0]
                        eventname = run.split("/")[-2]
                        upa.update(lessername,eventname,self.rmdir,cluster)

                        if self.attempt_healing == True and ("Failed" in status):
                            direct_resubmit = False
                            forcepass_resubmit = False
                            rundir = chu.read_wocc(run)

                            from runmonitor import heal
                            from runmonitor import restore_tools as resto
                            error = heal.check_error(rd=rundir)
                            if error == "ILE.sub":
                                iteration = str(max([int(el.split("-")[1].split(".")[0]) for el in os.listdir(rundir) if "posterior_samples" in el and "extrinsic" not in el]))
                                job_id = heal.get_job_id(rd=rundir)
                                encoding_error = heal.check_encodings_error(iteration,job_id,rd=rundir)
                                if encoding_error:
                                    direct_resubmit= True
                            
                            env = resto.find_env(run)
                            if direct_resubmit:
                                 subprocess.Popen(["python","-c","'import restore_tools as resto; resto.resubmit(rundir="+rundir+")'"],text=True,env=env)

                        if self.receiver != None and self.password != None and archive_orig != None: 
                            with open(os.path.join(self.rmdir,"archived_runs_microstatus.txt"),'r') as f:
                                archive_now= f.readlines()
                            for i,line in enumerate(archive_now):
                                if line != archive_orig[i]:
                                    deltas += [line]
                            print(deltas)
                if self.receiver != None and self.password != None and deltas != []:
                    #TODO emailing
                    import smtplib, ssl
                    smtp_server = "smtp.gmail.com"
                    port = 587
                    email_context = ssl.create_default_context()
                    try:
                        server = smtplib.SMTP(smtp_server,port)
                        server.ehlo()
                        server.starttls(context=email_context)
                        server.ehlo()
                        server.login(self.sender_email,self.password)
                        message = "Subject: runmonitor-rift updates \n\n\n \
                        You are receiving an automated email from runmonitor regarding your current runs on "+self.cluster+". If you do not wish to receive these emails please, dis-instantiate this daemon. If you did not instatiate this daemon, please contact rudall@caltech.edu. The following lines were found to have changed in your archived_run_microstatus.txt, indicating a state change for the run:\n"+" \n".join(deltas)
                        server.sendmail(self.sender_email,self.receiver,message)
                        print("sent email to "+self.receiver)
                    except Exception as fail:
                        print("failed to send email")
                        print(fail) 
                      
                #finally, it waits 1 hour befor updating again
                time.sleep(3600)
