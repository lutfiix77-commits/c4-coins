import os
import sys
import time
import json
import random
import requests
import urllib.parse
from telethon.sync import TelegramClient
from telethon import functions, types
from fake_useragent import UserAgent

def slow_print(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    print()

def run():
    api_id = 28752231
    api_hash = 'ec1c1f2c30e2f1855c3edee7e348480b'
    bot_name = 'bitfaucetgbot'
    
    client = TelegramClient('c4coins', api_id, api_hash)
    client.start()

    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")
    slow_print("\033[1;37m     🌟 \033[1;36mScript AutoMation Premium Members \033[1;37m🌟")
    slow_print("\033[1;37m      🛠️  \033[1;32mCreators : \033[1;33mC4-Coins Team \033[1;37m🛠️")
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")
    slow_print("\033[1;37m[#] \033[1;32mStatus     : \033[1;36mAuthorization \033[1;37m| \033[1;32mMode: \033[1;33mHigh-Speed ⚡\n")

    client.send_message(bot_name, '/start')
    time.sleep(2)
    
    bot = client.get_entity(bot_name)
    res_webview = client(functions.messages.RequestWebViewRequest(
        peer=bot,
        bot=bot,
        platform='android',
        from_bot_menu=False,
        url='https://bitfaucet.net/'
    ))
    
    auth_url = res_webview.url
    init_data = auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]
    data = urllib.parse.unquote(init_data)
    
    ua = UserAgent().random

    headers = {
        'User-Agent': ua,
        'Accept': "application/json, text/plain, */*",
        'Content-Type': "application/json",
        'sec-ch-ua-platform': "\"Android\"",
        'sec-ch-ua': "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Android WebView\";v=\"144\"",
        'sec-ch-ua-mobile': "?1",
        'origin': "https://bitfaucet.net",
        'x-requested-with': "org.telegram.messenger",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://bitfaucet.net/",
        'accept-language': "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        'priority': "u=1, i"
    }

    payload = {
        "initData": data,
        "referralCode": "6846731693"
    }

    login_req = requests.post("https://api.bitfaucet.net/api/auth/login", json=payload, headers=headers)
    res = login_req.json()
    
    token = res['token']
    firstName = res['user']['firstName']
    balance = res['user']['balance']

    slow_print(f"\033[1;32m👋 Welcome {firstName}! Your Balance = {balance} 💰")

    email = input("\033[1;37m📩 Enter your FaucetPay Email => ")
    
    head = headers.copy()
    head["authorization"] = f"Bearer {token}"
    
    requests.post("https://api.bitfaucet.net/api/auth/link-faucetpay", json={"address": email}, headers=head)

    coins_res = requests.get("https://api.bitfaucet.net/api/faucet/coins", headers=head).json()

    print("\n\033[1;34m" + "-"*41)
    slow_print("\033[1;37m🔍 Please Select Currency for Claim:")
    id_list = []
    symbol_list = []
    for index, coin in enumerate(coins_res, 1):
        print(f"\033[1;33m{index}. \033[1;37m{coin['symbol']}")
        id_list.append(coin['_id'])
        symbol_list.append(coin['symbol'])
    print("\033[1;34m" + "-"*41)

    select = int(input("\033[1;37m 🔢 Enter Selection Number => "))
    coin_id = id_list[select-1]

    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")
    slow_print("\033[1;37m     🌟 \033[1;36mScript AutoMation Premium Members \033[1;37m🌟")
    slow_print("\033[1;37m      🛠️  \033[1;32mCreators : \033[1;33mC4-Coins Team \033[1;37m🛠️")
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")
    slow_print("\033[1;37m[#] \033[1;32mStatus     : \033[1;36mAuthorization \033[1;37m| \033[1;32mMode: \033[1;33mHigh-Speed ⚡\n")

    while True:
        ads_start = requests.post("https://api.bitfaucet.net/api/ads/start", json={"provider": "telega"}, headers=head).json()
        
        if ads_start.get("success"):
            slow_print("\033[1;32m📺 Get Ads For Claim  ✅ Success")
            adSessionId = ads_start['adSessionId']
            nonce = ads_start['nonce']

            ads_comp = requests.post("https://api.bitfaucet.net/api/ads/complete", json={
                "adSessionId": adSessionId,
                "nonce": nonce,
                "provider": "telega",
                "result": "success",
                "meta": {"result": "success"}
            }, headers=head).json()

            if ads_comp.get("status") == "verified" or ads_comp.get("success"):
                slow_print("\033[1;32m⏳ Watch Ads Progress ✅ Verified")

                claim_res = requests.post("https://api.bitfaucet.net/api/faucet/claim", json={
                    "coinId": coin_id,
                    "address": email,
                    "adSessionId": adSessionId
                }, headers=head).json()

                if claim_res.get("success"):
                    amt = claim_res['amountSatoshis']
                    currency = claim_res['currency']
                    f_amt = amt if currency == "PEPE" else "{:.8f}".format(amt / 100000000)
                    slow_print(f"\033[1;32m🎉 Success Payout {f_amt} {currency} to {email} Faucet Pay")

                me_res = requests.get("https://api.bitfaucet.net/api/auth/me", headers=head).json()
                remaining = 50 - me_res['user']['claimsSinceLastShortlink']
                
                slow_print(f"\033[1;37m📊 Claims remaining before shortlink = {remaining} x")

                if remaining <= 0:
                    print(f"\n\033[1;31m⚠️ Please manually bypass shortlink via bot => https://t.me/bitfaucetgbot?start=6846731693")
                    sys.exit()

                for i in range(11, -1, -1):
                    sys.stdout.write(f"\r\033[1;37m🕒 Wait for Next claim In {i} seconds")
                    sys.stdout.flush()
                    time.sleep(1)
                sys.stdout.write("\r" + " " * 50 + "\r")

if __name__ == "__main__":
    run()
