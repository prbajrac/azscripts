#!/usr/bin/python
import os
import subprocess
import json
import sys

rg = raw_input('Resource Group: ')
cluster = raw_input ('Cluster Name: ')
location = raw_input('Location: ')
nodecount = raw_input('Node count: ')

#resize = raw_input('Resize VM OsDisk ? Y or N ')
#resize = resize.upper()
#if resize == 'Y':
 #osDiskSize = raw_input ('New OsDisk Size in Gb: ')
 #print ('Script will resize the VM to ' + osDiskSize)
#else:
 #print('Your OS Disk size will not be altered')
print ('**************************************************************')
print ("""Disclaimer The sample scripts are not supported under any Microsoft standard support program or service. The sample scripts are provided AS IS without warranty of any kind.
Microsoft further disclaims all implied warranties including, without limitation, any implied warranties of merchantability or of fitness for a particular purpose.
The entire risk arising out of the use or performance of the sample scripts and documentation remains with you. 
In no event shall Microsoft, its authors, or anyone else involved in the creation, production, or delivery of the scripts be liable for any damages whatsoever
(including, without limitation, damages for loss of business profits, business interruption, loss of business information, or other pecuniary loss) arising out of the use of or
inability to use the sample scripts or documentation, even if Microsoft has been advised of the possibility of such damages.""")
print ('**************************************************************')

ct = raw_input('Do you want to continue : ')
ct = ct.upper()
if ct == 'Y':
 print ('**************************************************************')
 print ('CREATING THE RESOURCE GROUP')
 print ('**************************************************************')
 rgroup = subprocess.check_output('az aks create ' + '-g ' + rg +' --location ' + location, shell=True)
 print ('**************************************************************')
 print ('CREATING THE CLUSTER')
 print ('**************************************************************')
 rgroup = subprocess.check_output('az aks create --resource-group ' + rg + ' --name ' + cluster + ' --node-count ' + nodecount + ' --generate-ssh-keys', shell=True)
 print ('**************************************************************')
 print ('GETTING ACCESS CREDENTIALS FOR THE MANAGED KUBERNETES CLUSTER')
 print ('**************************************************************')
 creds = subprocess.check_output('az aks get-credentials ' + '-g ' + rg +' -n ' + cluster, shell=True)
 print creds
else:
 sys.exit()
