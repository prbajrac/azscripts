#!/usr/bin/python
import os
import subprocess
import json
import sys

rg = raw_input('Resource Group: ')
cluster = raw_input ('Cluster Name: ')
location = raw_input('Location: ')
nodecount = raw_input('Node count: ' )
#Enable Addon logic
getaddons = raw_input('Enable addons: ')
if getaddons == 'Y':
 whichAddon = raw_input('Which addon 1.Monitoring, 2.http_application_routing : ')
 if whichAddon == '1':
  addon = 'monitoring'
 elif whichAddon == '2':
  addon = 'http_application_routing' 
else:
 pass

#Advanced networking logic
# getadvnet = raw_input ('Advanced Networking ? Y or N')
# if getadvnet == 'Y':
#  existingvnet = raw_input('Are you using an existing Vnet? Y or N ')
#  if existingvnet == 'Y':
#    vnetrg = raw_input('what is your vnet rg ? ')
#    vent = raw_input('what is the vnet name ? ')
#  else existingvnet == 'N'
#   addon = 'http_application_routing' 
# else:
#  pass
# nodecount = raw_input('Node count: ')

nodesizeavailability = subprocess.check_output('az vm list-skus --location ' + location + ' -o table | awk \'{print $3}\'', shell=True)
print ('**************************************************************')
print ("""YOUR NODE SIZE AVAILIBILITY LIST""")
print ('**************************************************************')
print (nodesizeavailability)
nodevmsize = raw_input('Pick Node VM Size above: ')


print ('******************************************************************************************************************************************************************************')
print ("""Disclaimer: The sample scripts are not supported under any Microsoft standard support program or service. The sample scripts are provided AS IS without warranty of any kind.
Microsoft further disclaims all implied warranties including, without limitation, any implied warranties of merchantability or of fitness for a particular purpose.
The entire risk arising out of the use or performance of the sample scripts and documentation remains with you.
In no event shall Microsoft, its authors, or anyone else involved in the creation, production, or delivery of the scripts be liable for any damages whatsoever
(including, without limitation, damages for loss of business profits, business interruption, loss of business information, or other pecuniary loss) arising out of the use of or
inability to use the sample scripts or documentation, even if Microsoft has been advised of the possibility of such damages.""")
print ('******************************************************************************************************************************************************************************')

# Methods for various choices
def create_base():
 akscluster = subprocess.check_output('az aks create --resource-group ' + rg + ' --name ' + cluster + ' --node-count ' + nodecount + ' -s ' + nodevmsize + ' --generate-ssh-keys', shell=True)
 print (akscluster)
 return akscluster

def enable_addons():
 aksEnableAddons = subprocess.check_output('az aks create --resource-group ' + rg + ' --name ' + cluster + ' --node-count ' + nodecount +  ' -s ' + nodevmsize + ' -a ' + addon + ' --generate-ssh-keys', shell=True)
 print (aksEnableAddons)
 return aksEnableAddons

# def advanced_networking():
#  aksAdvNet = subprocess.check_output('az aks create --resource-group ' + rg + ' --name ' + cluster + ' --node-count ' + nodecount +  ' -s ' + nodevmsize + ' --network-plugin azure ' + '--docker-bridge-address 172.17.0.1/16 --dns-service-ip 10.0.0.10 --service-cidr 10.0.0.0/24 --generate-ssh-keys', shell=True)
#  print (aksAdvNet)
#  return aksAdvNet

ct = raw_input('Do you want to continue : ')
ct = ct.upper()
if ct == 'Y':
 print ('**************************************************************')
 print ('CREATING THE RESOURCE GROUP')
 print ('**************************************************************')
 rgroup = subprocess.check_output('az group create ' + '-n ' + rg +' --location ' + location, shell=True)
 print (rgroup)
 print ('**************************************************************')
 print ('CREATING THE CLUSTER')
 print ('**************************************************************')
 if getaddons == 'N':
  create_base()
 elif getaddons == 'Y':
  enable_addons()
 print ('**************************************************************')
 print ('GETTING ACCESS CREDENTIALS FOR THE MANAGED KUBERNETES CLUSTER')
 print ('**************************************************************')
 creds = subprocess.check_output('az aks get-credentials ' + '-g ' + rg +' -n ' + cluster, shell=True)
 print (creds)
else:
 sys.exit()
