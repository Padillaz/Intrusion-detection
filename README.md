# Intrusion-detection

The purpose of this script is to give you the ability to find all of the devices or users connected to your network. If found, it will alert you of the untrusted ones. It could help you find out which users are connecting to the network. It only takes a few seconds to run. You have the added capability of running this at 5-minute intervals or as you see fit to your needs.

This script will scan the network of your choice and will alert you of any devices not present in the whitelist. The whitelist is a list of MAC address that YOU add to it. The first time you run the script, the whitelist will be empty. You will need to configure the whitelist manualy so it's up to you to add your trusted devices to it. 

See the whitelist section for more information.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Software package: **python3** and **nmon**

**Ubuntu / Debian**

```
sudo apt install python3 nmon
```

## Whitelist
Every time you run the detection script, a list of all detected devices will be written in the file 'devices.mac'. 

If you trust all these devices, you can import them with the following command:

```
sudo ./trust-devices.py  data.db devices.mac
```

If you don't trust all of them, you can erase the one that you don't want and still import the file.

The following command will flush the current whitelist and import the entries in devices.mac

```
sudo ./trust-devices.py  data.db devices.mac
```

### Installing

Download and unzip, then make sure you have installed the **Prerequisites**

Things to do:

- The folder should be writable because a devices.mac file is generated every time you launch the detect.py script
- Don't forget to mark the python scripts as 'executables'

```
sudo chmod +x *.py
```

## Running

The database filename can be anything, it will be created if absent. The network must be specified in the **network/mask** notation.

example of valid networks:

- 192.168.0.0/24
- 192.168.1.0/24
- 192.168.2.0/24

you should launch both programs with sudo:

- detect.py : nmon requires root privileges to get the MAC addresses
- trust-devices.py : requires root privileges because the database will be created with root. If you modify the database so that it's writable for someone else, you won't need sudo anymore.


```
Syntax:
	sudo ./detect.py  network_range  database

example: 
sudo ./detect.py 192.168.2.0/24 data.db
```

on the first run, all devices should be listed as untrusted, read the whitelist section. You need to run other script to import your trusted devices list.


## Built With

* [Visual studio code](https://code.visualstudio.com/) - Editor

## Built on
* [Kali](https://Kali.org/) - Kali


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

