#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantRequest, LeaveChannelRequest
from telethon.tl.types import InputPeerEmpty
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl.functions.messages import GetDialogsRequest
import configparser
import os
import sys
import csv
import traceback
import time

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

def get_my_groups(client):
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

def display_groups(groups):
    print(gr + "[+] Your groups and channels:")
    for i, group in enumerate(groups):
        print(gr + f"[{i}] {group.title}")

def leave_group(client, group):
    try:
        client(GetParticipantRequest(channel=group, participant=client.get_me()))
        print(gr + f"[+] Leaving {group.title}...")
        client(LeaveChannelRequest(channel=group))
        time.sleep(2)  # Delay to avoid flood errors
        print(gr + f"[+] Successfully left {group.title}.")
    except FloodWaitError as e:
        print(re + f"[!] Flood wait error: {e}")
    except Exception as e:
        print(re + f"[!] Error leaving {group.title}: {e}")

def main():
    banner()
    api_id, api_hash, phone = load_config()
    client = connect_client(api_id, api_hash, phone)

    groups = get_my_groups(client)
    display_groups(groups)

    try:
        choices = input(gr + "[+] Enter group indices to leave (comma-separated): " + re)
        indices = list(map(int, choices.split(',')))

        for idx in indices:
            if idx < len(groups):
                leave_group(client, groups[idx])
            else:
                print(re + f"[!] Invalid index: {idx}. Skipping.")

        while True:
            action = input(gr + "\n[?] Do you want to leave more groups? (y/n): " + re).strip().lower()
            if action == 'y':
                choices = input(gr + "[+] Enter group indices to leave (comma-separated): " + re)
                indices = list(map(int, choices.split(',')))
                for idx in indices:
                    if idx < len(groups):
                        leave_group(client, groups[idx])
                    else:
                        print(re + f"[!] Invalid index: {idx}. Skipping.")
            elif action == 'n':
                print(gr + "[+] Exiting...")
                break
            else:
                print(re + "[!] Invalid choice. Please enter 'y' or 'n'.")

    except KeyboardInterrupt:
        print("\n" + re + "[!] User interrupted. Exiting...")

if __name__ == "__main__":
    main()
