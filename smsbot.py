#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import configparser
import os
import sys
import csv
import random
import time

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"
SLEEP_TIME = 30

def banner():
    print(f"""
{re}╔╦╗{cy}┌─┐┬  ┌─┐{re}╔═╗  ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
{re} ║ {cy}├┤ │  ├┤ {re}║ ╦  ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
{re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝  ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─
    """)

def load_config():
    cpass = configparser.RawConfigParser()
    cpass.read('config.data')
    try:
        api_id = cpass['cred']['id']
        api_hash = cpass['cred']['hash']
        phone = cpass['cred']['phone']
        return api_id, api_hash, phone
    except KeyError:
        os.system('clear')
        banner()
        print(re + "[!] Run python3 setup.py first!\n")
        sys.exit(1)

def connect_client(api_id, api_hash, phone):
    client = TelegramClient(phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        os.system('clear')
        banner()
        client.sign_in(phone, input(gr + '[+] Enter the code: ' + re))
    return client

def load_users(input_file):
    users = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {
                'username': row[0],
                'id': int(row[1]),
                'access_hash': int(row[2]),
                'name': row[3]
            }
            users.append(user)
    return users

def send_messages(client, users, mode, message):
    for user in users:
        try:
            if mode == 1 and user['username']:
                receiver = client.get_input_entity(user['username'])
            elif mode == 2:
                receiver = InputPeerUser(user['id'], user['access_hash'])
            else:
                print(re + "[!] Invalid Mode. Exiting.")
                client.disconnect()
                sys.exit(1)
            print(gr + "[+] Sending Message to:", user['name'])
            client.send_message(receiver, message.format(user['name']))
            print(gr + "[+] Waiting {} seconds".format(SLEEP_TIME))
            time.sleep(SLEEP_TIME)
        except PeerFloodError:
            print(re + "[!] Getting Flood Error from Telegram. Script is stopping now. Please try again after some time.")
            client.disconnect()
            sys.exit(1)
        except Exception as e:
            print(re + "[!] Error:", e)
            print(re + "[!] Trying to continue...")
            continue
    client.disconnect()
    print(gr + "Done. Message sent to all users.")

def main():
    banner()
    api_id, api_hash, phone = load_config()
    client = connect_client(api_id, api_hash, phone)

    input_file = sys.argv[1]
    users = load_users(input_file)

    print(gr + "[1] Send message by user ID\n[2] Send message by username")
    mode = int(input(gr + "Input: " + re))

    message = input(gr + "[+] Enter Your Message: " + re)
    
    send_messages(client, users, mode, message)

if __name__ == "__main__":
    main()
