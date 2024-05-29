from hdwallet import HDWallet
from hdwallet.symbols import BTC as SYMBOL
from hdwallet.utils import generate_mnemonic
from typing import Optional
from colorama import Fore
import json, requests, os
from datetime import datetime
from time import sleep
import random

def clear():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

if not os.path.isfile('config.json'):
    clear()
    print(f"{Fore.RED}The config.json file is missing or it's not in the same path!{Fore.RESET}")
    input("Press enter to exit...")
    exit()

with open('config.json') as config_file:
    data = json.load(config_file)
    b_config_strenght = data["settings"]["bruteforcer"]["strenght"]
    b_config_language = data["settings"]["bruteforcer"]["language"]
    b_config_passphere = data["settings"]["bruteforcer"]["passphere"]
    c_config_file_name = data["settings"]["checker"]["filename"]
    config_failed = data["settings"]["general"]["failed"]
    config_success = data["settings"]["general"]["success"]
    config_address = data["settings"]["general"]["addresstype"]
    api_url = data["settings"]["general"]["api"]["api_url"]

def center(var: str, space: int = None):
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) // 2
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())

def ui():
    clear()
    font = """
                ▄▄▄▄   ▄▄▄█████▓ ▄████▄    █████▒▒█████   ██▀███   ▄████▄  ▓█████  ██▀███  
                ▓█████▄ ▓  ██▒ ▓▒▒██▀ ▀█  ▓██   ▒▒██▒  ██▒▓██ ▒ ██▒▒██▀ ▀█  ▓█   ▀ ▓██ ▒ ██▒
                ▒██▒ ▄██▒ ▓██░ ▒░▒▓█    ▄ ▒████ ░▒██░  ██▒▓██ ░▄█ ▒▒▓█    ▄ ▒███   ▓██ ░▄█ ▒
                ▒██░█▀  ░ ▓██▓ ░ ▒▓▓▄ ▄██▒░▓█▒  ░▒██   ██░▒██▀▀█▄  ▒▓▓▄ ▄██▒▒▓█  ▄ ▒██▀▀█▄  
                ░▓█  ▀█▓  ▒██▒ ░ ▒ ▓███▀ ░░▒█░   ░ ████▓▒░░██▓ ▒██▒▒ ▓███▀ ░░▒████▒░██▓ ▒██▒
                ░▒▓███▀▒  ▒ ░░   ░ ░▒ ▒  ░ ▒ ░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░ ░▒ ▒  ░░░ ▒░ ░░ ▒▓ ░▒▓░
                ▒░▒   ░     ░      ░  ▒    ░       ░ ▒ ▒░   ░▒ ░ ▒░  ░  ▒    ░ ░  ░  ░▒ ░ ▒░
                ░    ░   ░      ░         ░ ░   ░ ░ ░ ▒    ░░   ░ ░           ░     ░░   ░ 
                ░               ░ ░                 ░ ░     ░     ░ ░         ░  ░   ░     
                    ░          ░                                 ░                        """
    faded = ''
    red = 0
    for line in font.splitlines():
        faded += (f"\033[38;2;{red};10;230m{line}\033[0m\n")
        if red < 255:
            red += 10
            if red > 110:
                red = 255
    print(center(faded))
    print(center(f'{Fore.LIGHTYELLOW_EX}\ngithub.com/LizardX2 Version 1.0 | Telegram: @LizardX2\n{Fore.RESET}'))

def errorfile():
    clear()
    print(f"{Fore.RED}[!] FATAL ERROR! A text file in the directory is missing, please make sure the files: {config_failed} | {config_success} | {c_config_file_name} are there, or are in the same path! {Fore.RESET}")
    input(f"{Fore.LIGHTRED_EX}[!] Press enter to exit... {Fore.RESET}")
    exit()

ui()
settings = input(f"{Fore.YELLOW}[?]{Fore.RESET} {Fore.LIGHTWHITE_EX}Make a choice between Checker and Bruteforcer [C] - [B] > {Fore.RESET}")

def main():
    if settings.lower() == "b":
        if not (os.path.isfile(config_failed) and os.path.isfile(config_success) and os.path.isfile(c_config_file_name)):
            errorfile()
        print(f"\n{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}Saving failed seeds on >> {Fore.LIGHTYELLOW_EX}{config_failed}{Fore.RESET}")
        print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}Saving successful seeds on >> {Fore.LIGHTYELLOW_EX}{config_success}{Fore.RESET}")
        print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}Type of addresses >> {Fore.LIGHTYELLOW_EX}{config_address}{Fore.RESET}")
        print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}Language >> {Fore.LIGHTYELLOW_EX}{b_config_language}{Fore.RESET}")
        print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}Strength >> {Fore.LIGHTYELLOW_EX}{b_config_strenght}{Fore.RESET}")
        sleep(2)
        print("\n")
        STRENGTH = b_config_strenght
        LANGUAGE = b_config_language
        PASSPHRASE = None if b_config_passphere == "None" else b_config_passphere
        s = requests.Session()
        while True:
            now_time = datetime.now()
            current = now_time.strftime("%H:%M:%S")
            MNEMONIC = generate_mnemonic(language=LANGUAGE, strength=STRENGTH)
            hdwallet = HDWallet(symbol=SYMBOL, use_default_path=False)
            hdwallet.from_mnemonic(mnemonic=MNEMONIC, language=LANGUAGE, passphrase=PASSPHRASE)
            btc_address = hdwallet.p2pkh_address()
            btc_wif = hdwallet.dumps()['wif']
            btc_seed = hdwallet.dumps()['mnemonic']
            btc_entropy = hdwallet.dumps()['entropy']
            btc_privatekey = hdwallet.dumps()['private_key']
            response = s.get(f"{api_url}/{btc_address}")
            if response.status_code == 404:
                print(f"Error: Received 404 status code for URL {response.url}")
                print("The API endpoint might be incorrect or the address may not exist.")
                continue
            elif response.status_code != 200:
                print(f"Error: Received {response.status_code} status code for URL {response.url}")
                print(f"Response content: {response.text}")
                continue
            try:
                get_info = response.json()
            except json.decoder.JSONDecodeError:
                print(f"Error parsing JSON response: {response.text}")
                continue
            balance = get_info.get('chain_stats', {}).get('funded_txo_sum', 0)
            all_time_balance = get_info.get('chain_stats', {}).get('spent_txo_sum', 0)
            if str(balance) == "0" or str(all_time_balance) == "0":
                with open(config_failed, "a") as fail:
                    fail.write(f"{btc_address} | {balance}$ | {all_time_balance}$ | {btc_seed} | {btc_privatekey} | {btc_entropy} | {btc_wif} \n")
            else:
                with open(config_success, "a") as valid:
                    valid.write(f"{btc_address} | {balance}$ | {all_time_balance}$ | {btc_seed} | {btc_privatekey} | {btc_entropy} | {btc_wif} \n")
            print(f"{Fore.LIGHTBLACK_EX}[{current}]{Fore.RESET} {Fore.YELLOW}{btc_address}{Fore.RESET} {Fore.LIGHTBLACK_EX}|{Fore.RESET} {Fore.LIGHTGREEN_EX}BAL: {balance}${Fore.RESET} {Fore.LIGHTBLACK_EX}|{Fore.RESET} {Fore.LIGHTWHITE_EX}SEED: {btc_seed}{Fore.RESET} {Fore.LIGHTBLACK_EX}|{Fore.RESET} {Fore.LIGHTRED_EX}PRIV: {btc_privatekey}{Fore.RESET} {Fore.LIGHTBLACK_EX}| {Fore.RESET}{Fore.BLUE}{b_config_strenght}{Fore.RESET}")
    elif settings.lower() == "c":
        if not (os.path.isfile(config_failed) and os.path.isfile(config_success) and os.path.isfile(c_config_file_name)):
            errorfile()
        print(f"\n{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}Saving failed seeds on >> {Fore.LIGHTYELLOW_EX}{config_failed}{Fore.RESET}")
        print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}Saving successful seeds on >> {Fore.LIGHTYELLOW_EX}{config_success}{Fore.RESET}")
        print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}Type of addresses >> {Fore.LIGHTYELLOW_EX}{config_address}{Fore.RESET}")
        sleep(2)
        print("\n")
        with open(c_config_file_name, "r") as z:
            c_config_file = [x.strip() for x in z.readlines()]
        s = requests.Session()
        for line in c_config_file:
            now_time = datetime.now()
            current = now_time.strftime("%H:%M:%S")
            mnemonic = line.split("|")[0].strip()
            hdwallet = HDWallet(symbol=SYMBOL, use_default_path=False)
            hdwallet.from_mnemonic(mnemonic=mnemonic, passphrase=None)
            btc_address = hdwallet.p2pkh_address()
            btc_wif = hdwallet.dumps()['wif']
            btc_seed = hdwallet.dumps()['mnemonic']
            btc_entropy = hdwallet.dumps()['entropy']
            btc_privatekey = hdwallet.dumps()['private_key']
            response = s.get(f"{api_url}/{btc_address}")
            if response.status_code == 404:
                print(f"Error: Received 404 status code for URL {response.url}")
                print("The API endpoint might be incorrect or the address may not exist.")
                continue
            elif response.status_code != 200:
                print(f"Error: Received {response.status_code} status code for URL {response.url}")
                print(f"Response content: {response.text}")
                continue
            try:
                get_info = response.json()
            except json.decoder.JSONDecodeError:
                print(f"Error parsing JSON response: {response.text}")
                continue
            balance = get_info.get('chain_stats', {}).get('funded_txo_sum', 0)
            all_time_balance = get_info.get('chain_stats', {}).get('spent_txo_sum', 0)
            if str(balance) == "0" or str(all_time_balance) == "0":
                with open(config_failed, "a") as fail:
                    fail.write(f"{btc_address} | {balance}$ | {all_time_balance}$ | {btc_seed} | {btc_privatekey} | {btc_entropy} | {btc_wif} \n")
            else:
                with open(config_success, "a") as valid:
                    valid.write(f"{btc_address} | {balance}$ | {all_time_balance}$ | {btc_seed} | {btc_privatekey} | {btc_entropy} | {btc_wif} \n")
            print(f"{Fore.LIGHTBLACK_EX}[{current}]{Fore.RESET} {Fore.YELLOW}{btc_address}{Fore.RESET} {Fore.LIGHTBLACK_EX}|{Fore.RESET} {Fore.LIGHTGREEN_EX}BAL: {balance}${Fore.RESET} {Fore.LIGHTBLACK_EX}|{Fore.RESET} {Fore.LIGHTWHITE_EX}SEED: {btc_seed}{Fore.RESET} {Fore.LIGHTBLACK_EX}|{Fore.RESET} {Fore.LIGHTRED_EX}PRIV: {btc_privatekey}{Fore.RESET} {Fore.LIGHTBLACK_EX}| {Fore.RESET}{Fore.BLUE}{b_config_strenght}{Fore.RESET}")

main()
