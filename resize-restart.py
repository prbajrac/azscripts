#!/usr/bin/python
import os
import subprocess
import json
import sys

rg = raw_input('Resource Group: ')
cluster = raw_input ('Cluster Name: ')

resize = raw_input('Resize VM OsDisk ? Y or N ')
resize = resize.upper()
if resize == 'Y':
 osDiskSize = raw_input ('New OsDisk Size in Gb: ')
 print ('Script will resize the VM to ' + osDiskSize)
else:
 print('Your OS Disk size will not be altered')
print ('**************************************************************')
print ("""Disclaimer: The sample scripts are not supported under any Microsoft standard support program or service. The sample scripts are provided AS IS without warranty of any kind.
Microsoft further disclaims all implied warranties including, without limitation, any implied warranties of merchantability or of fitness for a particular purpose.
The entire risk arising out of the use or performance of the sample scripts and documentation remains with you. 
In no event shall Microsoft, its authors, or aelse involved in the creation, production, or delivery of the scripts be liable for any damages whatsoever
(including, without limitation, damages for loss of business profits, business interruption, loss of business information, or other pecuniary loss) arising out of the use of or
inability to use the sample scripts or documentation, even if Microsoft has been advised of the possibility of such damages.""")
print ('**************************************************************')

ct = raw_input('Do you want to continue : ')
ct = ct.upper()
if ct == 'Y':
 print ('**************************************************************')
 print ('GETTING ACCESS CREDENTIALS FOR THE MANAGED KUBERNETES CLUSTER')
 print ('**************************************************************')
 creds = subprocess.check_output('az aks get-credentials ' + '-g ' + rg +' -n ' + cluster, shell=True)
 print (creds)
 
 aksCluster = subprocess.check_output('az aks show -g '+ rg + ' -n ' + cluster, shell=True)
 print (aksCluster)
 
 print ('**************************************************************')
 print ('GETTING NODE RESOURCE GROUP')
 print ('**************************************************************')
 y = json.loads(aksCluster)

 nrg = (y['nodeResourceGroup'])
 print ('NodeResourceGroup: ' + nrg)

 print ('**************************************************************')
 print ('LISTING VM ON THE NODE RESOURCE GROUP')
 print ('**************************************************************')
 clusterVm = subprocess.check_output('az vm list -g ' + nrg, shell=True)
 clusterVmtb = subprocess.check_output('az vm list -g ' + nrg + ' -o table', shell=True)
 print (clusterVmtb)
 
 print ('**************************************************************')
 print ('GET NODES')
 print ('**************************************************************')
 getNodes = subprocess.check_output('kubectl get nodes -o wide', shell=True)
 print (getNodes)

 y = json.loads(clusterVm)

 for i in y:
  osDiskName = (i['storageProfile']['osDisk']['name'])
  print  ('OSDiskName: '+ osDiskName)
  nodeName = (i['name'])
  print ('NodeName: ' + nodeName)
  
  print ('**************************************************************')
  print ('DRANINIG NODE')
  print ('**************************************************************')
  print(subprocess.check_output('kubectl drain ' + nodeName + ' --ignore-daemonsets',shell=True))
  
  print ('**************************************************************')
  print ('DEALLOCATING VM')
  print ('**************************************************************')
 
  print(subprocess.check_output('az vm deallocate -g '+ nrg + ' -n ' + nodeName, shell=True))
  if resize == 'Y':
   print ('**************************************************************')
   print ('UPDATING DISK SIZE')
   print ('**************************************************************')
   print(subprocess.check_output('az disk update -g ' + nrg + ' -n ' + osDiskName + ' --size-gb '+ osDiskSize, shell=True))
  else:
   pass
  print ('**************************************************************')
  print ('STARTING VM')
  print ('**************************************************************')
 
  print (subprocess.check_output('az vm start -g '  + nrg + ' -n ' + nodeName, shell=True))
  
  print ('**************************************************************')
  print ('UNCORDON NODE')
  print ('**************************************************************')
  print(subprocess.check_output('kubectl uncordon ' + nodeName, shell=True))
  print (getNodes)
else:
 sys.exit()

