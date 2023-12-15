# SNMP Monitor

Console Application for network monitoring 

## Requirements
 
1) pysnmp == 0.7.1
2) python-nmap == 2.0.16  
3) netifaces == 0.11.0
4) art == 6.1

## Setup 
### Configure SNMP
Install SNMP packages
```console
sudo apt update
sudo apt install snmp
```

Edit SNMP daemon config file   
Set ```community string``` and ```agent address```
```console
sudo nano /etc/snmp/snmpd.conf
```

Restart SNMP service
```console
sudo systemctl restart snmpd
```

### Configure python project

Clone this repo in your work directory and install dependencies
```console
git clone https://gitlab.com/todo-lr/football.git
pip install -r requirements.txt
```


## Run
Move to local repository and run ```main.py```
```console
cd Path/To/Repo/snmp_monitor
python3 -m main
```
