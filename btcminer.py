from hdwallet import HDWallet
from hdwallet.symbols import BTC as BTC_SYMBOL
from hdwallet.symbols import LTC as LTC_SYMBOL
from hdwallet.symbols import ETH as ETH_SYMBOL
from hdwallet.symbols import DOGE as DOGE_SYMBOL
from hdwallet.utils import generate_mnemonic
from typing import Optional
from colorama import Fore
import json, requests, os
from datetime import datetime
from time import sleep

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
    api_urls = data["settings"]["general"]["api"]

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

def check_balance(symbol, address, api_urls):
    api_url = api_urls.get(symbol.lower())
    if not api_url:
        print(f"API URL for {symbol} is not configured.")
        return 0, 0

    response = requests.get(f"{api_url}/{address}")
    if response.status_code == 404:
        print(f"Error: Received 404 status code for URL {response.url}")
        print("The API endpoint might be incorrect or the address may not exist.")
        return 0, 0
    elif response.status_code != 200:
        print(f"Error: Received {response.status_code} status code for URL {response.url}")
        print(f"Response content: {response.text}")
        return 0, 0
    try:
        get_info = response.json()
    except json.decoder.JSONDecodeError:
        print(f"Error parsing JSON response: {response.text}")
        return 0, 0

    if symbol == "BTC":
        balance = get_info.get('chain_stats', {}).get('funded_txo_sum', 0)
        all_time_balance = get_info.get('chain_stats', {}).get('spent_txo_sum', 0)
    elif symbol == "LTC":
        balance = get_info.get('balance', 0)
        all_time_balance = get_info.get('total_received', 0)
    elif symbol == "DOGE":
        balance = get_info.get('balance', 0)
        all_time_balance = get_info.get('received', 0)
    elif symbol == "ETH":
        balance = get_info.get('balance', 0) / 1e18  # Convert wei to ETH
        all_time_balance = get_info.get('total_received', 0) / 1e18  # Convert wei to ETH
    else:
        balance = 0
        all_time_balance = 0

    return balance, all_time_balance

ui()
settings = input(f"{Fore.YELLOW}[?]{Fore.RESET} {Fore.LIGHTWHITE_EX}Make a choice between Checker and Bruteforcer [C] - [B] > {Fore.RESET}")

def main():
    import os
    print("Current Working Directory:", os.getcwd())
    print("Checking if files exist in the directory:")
    print("failed_seeds.txt exists:", os.path.isfile(config_failed))
    print("successful_seeds.txt exists:", os.path.isfile(config_success))
    print("seeds_to_check.txt exists:", os.path.isfile(c_config_file_name))

    if settings.lower() == "b":
        if not (os.path.isfile(config_failed) and os.path.isfile(config_success) and os.path.isfile(c_config_file_name)):
            errorfile()
        print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}Starting bruteforcer...{Fore.RESET}")
        while True:
            hdwallet = HDWallet(symbol=BTC_SYMBOL, use_default_path=False)
            MNEMONIC: str = generate_mnemonic(language=b_config_language, strength=b_config_strenght)
            LANGUAGE: str = b_config_language
            PASSPHRASE: Optional[str] = b_config_passphere

            hdwallet.from_mnemonic(mnemonic=MNEMONIC, language=LANGUAGE, passphrase=PASSPHRASE)
            btc_address = hdwallet.p2pkh_address()
            hdwallet.from_mnemonic(mnemonic=MNEMONIC, language=LANGUAGE, passphrase=PASSPHRASE)
            hdwallet.symbol = LTC_SYMBOL
            ltc_address = hdwallet.p2pkh_address()
            hdwallet.from_mnemonic(mnemonic=MNEMONIC, language=LANGUAGE, passphrase=PASSPHRASE)
            hdwallet.symbol = DOGE_SYMBOL
            doge_address = hdwallet.p2pkh_address()
            hdwallet.from_mnemonic(mnemonic=MNEMONIC, language=LANGUAGE, passphrase=PASSPHRASE)
            hdwallet.symbol = ETH_SYMBOL
            eth_address = hdwallet.p2pkh_address()

            btc_balance, btc_all_time_balance = check_balance("BTC", btc_address, api_urls)
            ltc_balance, ltc_all_time_balance = check_balance("LTC", ltc_address, api_urls)
            doge_balance, doge_all_time_balance = check_balance("DOGE", doge_address, api_urls)
            eth_balance, eth_all_time_balance = check_balance("ETH", eth_address, api_urls)

            total_balance = btc_balance + ltc_balance + doge_balance + eth_balance
            total_all_time_balance = btc_all_time_balance + ltc_all_time_balance + doge_all_time_balance + eth_all_time_balance

            print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}Generated Mnemonic: {Fore.LIGHTYELLOW_EX}{MNEMONIC}{Fore.RESET}")
            print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}BTC Address: {Fore.LIGHTYELLOW_EX}{btc_address}{Fore.RESET} | Balance: {btc_balance}")
            print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}LTC Address: {Fore.LIGHTYELLOW_EX}{ltc_address}{Fore.RESET} | Balance: {ltc_balance}")
            print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}DOGE Address: {Fore.LIGHTYELLOW_EX}{doge_address}{Fore.RESET} | Balance: {doge_balance}")
            print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}ETH Address: {Fore.LIGHTYELLOW_EX}{eth_address}{Fore.RESET} | Balance: {eth_balance}")

            if total_balance > 0:
                with open(config_success, "a") as success_file:
                    success_file.write(f"{MNEMONIC} | BTC: {btc_balance}, LTC: {ltc_balance}, DOGE: {doge_balance}, ETH: {eth_balance}\n")
                print(f"{Fore.GREEN}[+]{Fore.RESET} {Fore.LIGHTWHITE_EX}Successful Mnemonic: {Fore.LIGHTYELLOW_EX}{MNEMONIC}{Fore.RESET}")
            else:
                with open(config_failed, "a") as failed_file:
                    failed_file.write(f"{MNEMONIC}\n")

            sleep(1)

    elif settings.lower() == "c":
        if not (os.path.isfile(config_failed) and os.path.isfile(config_success) and os.path.isfile(c_config_file_name)):
            errorfile()
        print(f"\n{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}Checking seeds from file >> {Fore.LIGHTYELLOW_EX}{c_config_file_name}{Fore.RESET}")
        sleep(2)
        with open(c_config_file_name, "r") as seeds_file:
            seeds = seeds_file.readlines()
        
        for seed in seeds:
            seed = seed.strip()
            hdwallet = HDWallet(symbol=BTC_SYMBOL, use_default_path=False)
            hdwallet.from_mnemonic(mnemonic=seed, language=LANGUAGE, passphrase=PASSPHRASE)
            btc_address = hdwallet.p2pkh_address()
            hdwallet.from_mnemonic(mnemonic=seed, language=LANGUAGE, passphrase=PASSPHRASE)
            hdwallet.symbol = LTC_SYMBOL
            ltc_address = hdwallet.p2pkh_address()
            hdwallet.from_mnemonic(mnemonic=seed, language=LANGUAGE, passphrase=PASSPHRASE)
            hdwallet.symbol = DOGE_SYMBOL
            doge_address = hdwallet.p2pkh_address()
            hdwallet.from_mnemonic(mnemonic=seed, language=LANGUAGE, passphrase=PASSPHRASE)
            hdwallet.symbol = ETH_SYMBOL
            eth_address = hdwallet.p2pkh_address()

            btc_balance, btc_all_time_balance = check_balance("BTC", btc_address, api_urls)
            ltc_balance, ltc_all_time_balance = check_balance("LTC", ltc_address, api_urls)
            doge_balance, doge_all_time_balance = check_balance("DOGE", doge_address, api_urls)
            eth_balance, eth_all_time_balance = check_balance("ETH", eth_address, api_urls)

            total_balance = btc_balance + ltc_balance + doge_balance + eth_balance
            total_all_time_balance = btc_all_time_balance + ltc_all_time_balance + doge_all_time_balance + eth_all_time_balance

            print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}Checking Mnemonic: {Fore.LIGHTYELLOW_EX}{seed}{Fore.RESET}")
            print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}BTC Address: {Fore.LIGHTYELLOW_EX}{btc_address}{Fore.RESET} | Balance: {btc_balance}")
            print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}LTC Address: {Fore.LIGHTYELLOW_EX}{ltc_address}{Fore.RESET} | Balance: {ltc_balance}")
            print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}DOGE Address: {Fore.LIGHTYELLOW_EX}{doge_address}{Fore.RESET} | Balance: {doge_balance}")
            print(f"{Fore.YELLOW}[!]{Fore.RESET} {Fore.LIGHTWHITE_EX}ETH Address: {Fore.LIGHTYELLOW_EX}{eth_address}{Fore.RESET} | Balance: {eth_balance}")

            if total_balance > 0:
                with open(config_success, "a") as success_file:
                    success_file.write(f"{seed} | BTC: {btc_balance}, LTC: {ltc_balance}, DOGE: {doge_balance}, ETH: {eth_balance}\n")
                print(f"{Fore.GREEN}[+]{Fore.RESET} {Fore.LIGHTWHITE_EX}Successful Mnemonic: {Fore.LIGHTYELLOW_EX}{seed}{Fore.RESET}")
            else:
                with open(config_failed, "a") as failed_file:
                    failed_file.write(f"{seed}\n")

            sleep(1)

if __name__ == "__main__":
    main()
