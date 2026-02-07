import os
import sys
import time
import json
import random
import requests
from telethon.sync import TelegramClient
from telethon import functions, types
from fake_useragent import UserAgent

def slow_print(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)
    print()

def main():
    api_id = 28752231
    api_hash = 'ec1c1f2c30e2f1855c3edee7e348480b'
    
    client = TelegramClient('c4coins', api_id, api_hash)
    client.start()

    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")
    slow_print("\033[1;37m     🌟 \033[1;36mScript AutoMation Premium Members \033[1;37m🌟")
    slow_print("\033[1;37m      🛠️  \033[1;32mCreators : \033[1;33mC4-Coins Team \033[1;37m🛠️")
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")
    slow_print("\033[1;37m[#] \033[1;32mStatus     : \033[1;36mAuthorization \033[1;37m| \033[1;32mMode: \033[1;33mHigh-Speed ⚡\n")

    data = "user=%7B%22id%22%3A8570709418%2C%22first_name%22%3A%22Leonx76%22%2C%22last_name%22%3A%22%22%2C%22language_code%22%3A%22id%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FjSc1cAO7y3unolNY2HTw54A0qNa4penzTNWwWIEcHsi1dalygbqEuZSdYgB_5FCt.svg%22%7D&chat_instance=6189154118145842666&chat_type=sender&start_param=6846731693&auth_date=1770440587&signature=h6foGrPl6q_U2QkZqPYv4awXUEPhNtAuvRHvNKyEkBRi3wmGfCraR5Aoqi9-v-Xp-zCIz2aOiBeOX8kqglvpDg&hash=7472d86953f35540b7a50326e769f2571ab5fa86d1ee896ded95a6ad56e5c590"
    
    ua = UserAgent().random

    login_headers = {
        'User-Agent': ua,
        'Accept': "application/json, text/plain, */*",
        'Content-Type': "application/json",
        'sec-ch-ua-platform': '"Android"',
        'origin': "https://bitfaucet.net",
        'x-requested-with': "org.telegram.messenger",
        'referer': "https://bitfaucet.net/"
    }

    login_payload = {
        "initData": data,
        "referralCode": "6846731693"
    }

    res = requests.post("https://api.bitfaucet.net/api/auth/login", json=login_payload, headers=login_headers).json()
    token = res['token']
    first_name = res['user']['firstName']
    balance = res['user']['balance']

    slow_print(f"\033[1;32m[+] \033[1;37mWelcome \033[1;33m{first_name}\033[1;37m! Your Balance = \033[1;36m{balance}")

    email = input("\033[1;37m[?] Enter your FaucetPay Email => ")

    head = login_headers.copy()
    head["authorization"] = f"Bearer {token}"

    prin = requests.post("https://api.bitfaucet.net/api/auth/link-faucetpay", json={"address": email}, headers=head)

    coins = requests.get("https://api.bitfaucet.net/api/faucet/coins", headers=head).json()

    print("\n\033[1;34m" + "-"*30)
    slow_print("\033[1;37mPlease Select Currency for Claim:")
    id_list = []
    symbol_list = []
    for index, coin in enumerate(coins, 1):
        print(f"\033[1;33m{index}. \033[1;37m{coin['symbol']}")
        id_list.append(coin['_id'])
        symbol_list.append(coin['symbol'])
    print("\033[1;34m" + "-"*30)

    select = int(input("\033[1;37m[?] Enter Selection Number => "))
    selected_id = id_list[select-1]
    selected_symbol = symbol_list[select-1]

    while True:
        ads_start = requests.post("https://api.bitfaucet.net/api/ads/start", json={"provider": "telega"}, headers=head).json()
        
        if ads_start.get("success"):
            slow_print("\033[1;32m[+] \033[1;37mGet Ads For Claim  \033[1;32m✅ Success")
            ad_session_id = ads_start['adSessionId']
            nonce = ads_start['nonce']

            ads_comp = requests.post("https://api.bitfaucet.net/api/ads/complete", json={
                "adSessionId": ad_session_id,
                "nonce": nonce,
                "provider": "telega",
                "result": "success",
                "meta": {"result": "success"}
            }, headers=head).json()

            if ads_comp.get("success"):
                slow_print("\033[1;32m[+] \033[1;37mWatch Ads Progress \033[1;32m✅ Verified")

                claim = requests.post("https://api.bitfaucet.net/api/faucet/claim", json={
                    "coinId": selected_id,
                    "address": email,
                    "adSessionId": ad_session_id
                }, headers=head).json()

                if claim.get("success"):
                    amount = claim['amountSatoshis']
                    currency = claim['currency']
                    if currency != "PEPE":
                        formatted_amount = "{:.8f}".format(amount / 100000000)
                    else:
                        formatted_amount = amount
                    
                    slow_print(f"\033[1;32m[#] \033[1;37mSuccess Payout \033[1;33m{formatted_amount} {currency} \033[1;37mto \033[1;36m{email} \033[1;37mFaucetPay")

                me = requests.get("https://api.bitfaucet.net/api/auth/me", headers=head).json()
                claims_done = me['user']['claimsSinceLastShortlink']
                remaining = 50 - claims_done
                
                slow_print(f"\033[1;33m[!] \033[1;37mClaims remaining before shortlink: \033[1;31m{remaining}x")

                if remaining <= 0:
                    print("\n\033[1;31m" + "!"*45)
                    slow_print("\033[1;37mPlease bypass manual shortlink via bot => \033[1;34mhttps://t.me/bitfaucetgbot?start=6846731693")
                    print("\033[1;31m" + "!"*45)
                    sys.exit()

                for i in range(11, -1, -1):
                    print(f"\r\033[1;37m[*] Wait for Next Claim In \033[1;33m{i} \033[1;37mseconds...  ", end="")
                    time.sleep(1)
                print("\r" + " " * 50 + "\r", end="")

if __name__ == "__main__":
    main()
