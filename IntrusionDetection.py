#!/usr/bin/env python
import os
import subprocess
import xml.etree.ElementTree as ET
import re
import datetime
import sys
import sqlite3
def unlink(filename):
    if os.path.isfile(filename):
        os.remove(filename)
    return

def getNmapScan(range):
    """This function will launch NMAP and scan the network mask you provided."""
    filename = "/tmp/scanlog.xml"
    unlink(filename)
    unlink("devices.mac")
    f = open("devices.mac", "w")
    output = subprocess.run(["sudo", "nmap", "-v", "-sn", range, "-oX", filename], capture_output=True)
    if output.returncode == 0:
        tree = ET.parse(filename)
        root = tree.getroot()
        hosts = root.findall("./host")
        if hosts:
            state = mac = ip = vendor = ""
            for child in hosts:
                for attrib in child:
                    if attrib.tag == "status":
                        state = attrib.attrib["state"]
                    if attrib.tag == "address":
                        if attrib.attrib["addrtype"] == "mac":
                            mac = attrib.attrib["addr"]
                        if attrib.attrib["addrtype"] == "ipv4":
                            ip = attrib.attrib["addr"]
                        if "vendor" in attrib.attrib:
                            vendor = attrib.attrib["vendor"]
                if state == "down":
                    continue
                data = "%s|%s\n" % (mac, vendor)
                f.write(data)
                data = "insert or ignore into scans values (\"%s\",\"%s\",\"%s\",\"%s\"); " % (SCANID, ip, mac, vendor)
                conn.execute(data)
    f.close()
    return

def validateHost():
    """This function will check the last scan for any devices that are not listed in the whitelist."""
    c = conn.cursor()
    # GET LAST SCAN ID
    c.execute("select distinct id from scans order by 1 desc limit 1;")
    row = c.fetchone()
    count = 0
    if row:
        c.execute("select * from scans where id = "+str(row[0])+" and mac not in (select mac from whitelist);")
        rows = c.fetchall()
        for row in rows:
            print("Intruder detected in scan [%d] IP:[%s] MAC:[%s] VENDOR:[%s]" % (row[0], row[1], row[2], row[3]))
            count = count+1
    return count


if len(sys.argv) != 3:
    print("Syntax\n\t./IntrusionDetection.py <network>/<mask> <database>")
    
else:
    SCANID = datetime.datetime.now().strftime("%Y%m%d%H%M")
    conn = sqlite3.connect(sys.argv[2])
    if conn:

        conn.execute('CREATE TABLE IF NOT EXISTS scans (id integer, ip text, mac text, vendor text, PRIMARY KEY (id, ip));')
        conn.execute('CREATE TABLE IF NOT EXISTS whitelist (mac text, description text, primary key (mac));')
        # SCAN NETWORK
        getNmapScan(sys.argv[1])
        count = validateHost()
        conn.commit()
        conn.close()
        if count > 0:
            exit(1)
        exit(0)
    else:
        print("Error creating/accessing the database")
        exit(128)
exit(256)