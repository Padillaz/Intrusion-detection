#!/usr/bin/python3
import os
import re
import sys
import sqlite3


def unlink(filename):
    if os.path.isfile(filename):
        os.remove(filename)
    return


if len(sys.argv) < 3:
    print("Syntax\n\t./TrustedDevices.py <database> <devices.mac> [--flush]")
else:
    conn = sqlite3.connect(sys.argv[1])
    if conn:
        if len(sys.argv) == 4:
            if sys.argv[3] == "--flush":
                print("- Flushing whitelist")
                conn.execute('drop table whitelist;')
                conn.commit()
                conn.execute('vacuum;')

        print("- Creating table (if needed)")

        conn.execute('CREATE TABLE IF NONE EXISTS whitelist  (mac text, description text, primary key (mac));')

        f = open(sys.argv[2], "r")
        if f:
            print("- processing whitelist")
            for r in f:
                r = r.strip()
                m = re.split("\\|", r)
                if m:
                    sql = "insert or ignore into whitelist values (\"%s\",\"%s\");" % (m[0], m[1])
                    conn.execute(sql)
            f.close()

        conn.commit()
        conn.close()
    else:
        print("Error creating/accessing the database")
