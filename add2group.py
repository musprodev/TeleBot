#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os
import sys
import csv
import traceback
import time
import random

# ANSI color codes for terminal output
re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"

def banner():
    print(f"""
{re}╔╦╗{cy}┌─┐┬  ┌─┐   ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
{re} ║ {cy}├┤ │  ├┤    ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
{re} ╩ {cy}└─┘┴─┘└─┘   ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─
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

def get_groups(client):
    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup:
                groups.append(chat)
        except:
            continue

    return groups

def select_group(groups):
    for i, group in enumerate(groups):
        print(gr + '[' + cy + str(i) + gr + ']' + cy + ' - ' + group.title)
    print(gr + '[+] Choose a group to add members')
    g_index = int(input(gr + "[+] Enter a Number: " + re))
    return groups[g_index]

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

def add_members(client, target_group_entity, users, mode):
    for n, user in enumerate(users, start=1):
        if n % 50 == 0:
            time.sleep(1)
        try:
            print(f"Adding {user['id']}")
            if mode == 1 and user['username']:
                user_to_add = client.get_input_entity(user['username'])
            elif mode == 2:
                user_to_add = InputPeerUser(user['id'], user['access_hash'])
            else:
                print(re + "[!] Invalid Mode Selected. Please Try Again.")
                sys.exit(1)
            client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            print(gr + "[+] Waiting for 5-10 Seconds...")
            time.sleep(random.randint(5, 10))
        except PeerFloodError:
            print(re + "[!] Getting Flood Error from Telegram. Script is stopping now. Please try again after some time.")
            break
        except UserPrivacyRestrictedError:
            print(re + "[!] User's privacy settings do not allow adding. Skipping.")
        except Exception:
            traceback.print_exc()
            print(re + "[!] Unexpected Error")
            continue

def main():
    banner()
    api_id, api_hash, phone = load_config()
    client = connect_client(api_id, api_hash, phone)

    input_file = sys.argv[1]
    users = load_users(input_file)

    groups = get_groups(client)
    target_group = select_group(groups)
    target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

    print(gr + "[1] Add member by user ID\n[2] Add member by username")
    mode = int(input(gr + "Input: " + re))

    add_members(client, target_group_entity, users, mode)

if __name__ == "__main__":
    main()
