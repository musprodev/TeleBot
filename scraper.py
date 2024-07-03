#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import InputPeerChannel

import configparser
import csv
import os
import sys

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
    print(gr + '[+] Choose a group to scrape members from')
    g_index = int(input(gr + "[+] Enter a Number: " + re))
    return groups[g_index]

def scrape_members(client, target_group, output_file):
    print(gr + '[+] Fetching members...')
    all_participants = []
    target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)
    all_participants = client.get_participants(target_group_entity, aggressive=True)

    with open(output_file, "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
        for user in all_participants:
            username = user.username if user.username else ""
            user_id = user.id
            access_hash = user.access_hash
            name = user.first_name
            if user.last_name:
                name += " " + user.last_name
            group = target_group.title
            group_id = target_group.id
            writer.writerow([username, user_id, access_hash, name, group, group_id])
    print(gr + '[+] Members scraped successfully.')

def main():
    banner()
    api_id, api_hash, phone = load_config()
    client = connect_client(api_id, api_hash, phone)

    groups = get_groups(client)
    target_group = select_group(groups)

    output_file = input(gr + "[+] Enter the output file name (e.g. members.csv): " + re)
    scrape_members(client, target_group, output_file)

if __name__ == "__main__":
    main()
