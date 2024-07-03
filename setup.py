#!/bin/env python3
import configparser
import os

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"

def banner():
    print(f"""
{re}╔╦╗{cy}┌─┐┬  ┌─┐{re}╔═╗  ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
{re} ║ {cy}├┤ │  ├┤ {re}║ ╦  ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
{re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝  ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─
    """)

def main():
    banner()
    cpass = configparser.RawConfigParser()
    cpass.add_section('cred')
    xid = input(gr + "[+] Enter API ID: " + re)
    xhash = input(gr + "[+] Enter API Hash: " + re)
    xphone = input(gr + "[+] Enter Phone Number: " + re)
    
    cpass.set('cred', 'id', xid)
    cpass.set('cred', 'hash', xhash)
    cpass.set('cred', 'phone', xphone)

    with open('config.data', 'w') as configfile:
        cpass.write(configfile)

    print(gr + "[+] Setup Complete")

if __name__ == "__main__":
    main()
