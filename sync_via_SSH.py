#! /usr/bin/python3

#	This script synchronize client with server via rsync.
#	Config file placed here:
#		.sync_via_SSH.cfg

import subprocess, os, os.path
import configparser

#INPUT DATA
configFileName=".sync_via_SSH.cfg"


#read  property file
settings =  configparser.ConfigParser()
settings.read(configFileName)

host = settings.get("Server","host")
username = settings.get("Server","username")
key = settings.get("Server","key")



#synchronizate data
print("\nSYNCHRONIZATION PROCESS \n")
syncDests = settings.items("SynchDestinations")
for dest in syncDests:
      
        resultOfSync = subprocess.call("rsync -rv --progress --delete-before --update -e \"ssh  -p 2222\" {1}@{2}:{3}".format(key, username, host, dest[1]),shell=True)

        if (resultOfSync == 0):
            print("files {0} have synchronyze successfully".format(os.path.basename(dest[1])))
        else: 
            print("something bad happen")
		



