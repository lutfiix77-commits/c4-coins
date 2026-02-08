import os
import sys
import time
import json
import random
import requests
import asyncio
import re
import urllib.parse
from telethon.sync import TelegramClient
from telethon import functions, types, events
from fake_useragent import UserAgent

API_ID = 28752231
API_HASH = 'ec1c1f2c30e2f1855c3edee7e348480b'
BOT_NAME = 'bitfaucetgbot'
TARGET_GROUP = 'cukiiiiiiihtyamm'

COMMAND_MAP = {
    "adlink.click": "/adlink",
    "shrinkearn.com": "/shrinkearn",
    "shrinkme.io": "/shrinkme",
    "clk.sh": "/clk"
}

def slow_print(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    print()

async def auto_bypass(client, token, email, coin_id):
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 12; K)",
        'authorization': f"Bearer {token}",
        'accept': "application/json"
    }
    
    while True:
        print("\033[1;35m" + "🔗 " + "="*41 + " 🔗")
        print("\033[1;37m     🚀 \033[1;35mAuto Bypass Shortlink Mode \033[1;37m🚀")
        print("\033[1;35m" + "🔗 " + "="*41 + " 🔗")
        
        try:
            res = requests.get("https://api.bitfaucet.net/api/shortlinks", headers=headers).json()
            excluded = ["lnkfy.xyz", "shortano.link", "coinclix.co", "fc.lc", "exe.io", "cuty.io", "earnow.online"]
            available = [item for item in res if item.get('domain') in COMMAND_MAP and item.get('domain') not in excluded]
        except:
            available = []

        if not available:
            for i in range(120, -1, -1):
                sys.stdout.write(f"\r\033[1;31m⚠️ No Links! Cool down: {i}s remaining...")
                sys.stdout.flush()
                time.sleep(1)
            sys.stdout.write("\r" + " " * 60 + "\r")
            continue

        target = random.choice(available)
        domain = target.get('domain')
        provider_id = target.get('_id')

        print(f"\033[1;34m[⚡] \033[1;37mTargeting: \033[1;33m{domain}")
        
        start_payload = {"providerId": provider_id, "coinId": coin_id}
        start_res = requests.post("https://api.bitfaucet.net/api/shortlinks/start", json=start_payload, headers=headers).json()
        
        if not start_res.get('success'):
            print("\033[1;31m[!] Failed to get URL, retrying...")
            continue
            
        short_url = start_res.get('url')
        command = f"{COMMAND_MAP[domain]} {short_url}"
        
        sent_msg = await client.send_message(TARGET_GROUP, command)
        context = {"result_url": None, "done": asyncio.Event()}

        @client.on(events.NewMessage(chats=TARGET_GROUP))
        async def handler(event):
            me = await client.get_me()
            if "api.bitfaucet.net/api/shortlinks/verify/" in event.raw_text:
                is_for_me = False
                if event.reply_to and event.reply_to.reply_to_msg_id == sent_msg.id:
                    is_for_me = True
                elif me.username and me.username in event.raw_text:
                    is_for_me = True
                elif str(me.id) in event.raw_text:
                    is_for_me = True
                
                if is_for_me:
                    url_match = re.search(r'(https?://api\.bitfaucet\.net/api/shortlinks/verify/[^\s"}\']+)', event.raw_text)
                    if url_match:
                        context["result_url"] = url_match.group(1)
                        context["done"].set()

        try:
            await asyncio.wait_for(context["done"].wait(), timeout=60)
            client.remove_event_handler(handler)
            
            print(f"\033[1;32m[✔] Link Captured! Verifying...")
            v_res = requests.get(context["result_url"], headers={'User-Agent': 'Mozilla/5.0'})
            
            if "Success!" in v_res.text:
                print("\033[1;32m✨ BYPASS SUCCESS: Shortlink Cleared!")
                print("\033[1;34m" + "="*43 + "\n")
                return
            else:
                print("\033[1;31m[!] Verification Failed.")
        except asyncio.TimeoutError:
            print("\033[1;31m[!] Timeout! Group bot no response.")
            client.remove_event_handler(handler)

async def run():
    client = TelegramClient('c4coins', API_ID, API_HASH)
    await client.start()

    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")
    slow_print("\033[1;37m     🌟 \033[1;36mScript AutoMation Premium Members \033[1;37m🌟")
    slow_print("\033[1;37m      🛠️  \033[1;32mCreators : \033[1;33mC4-Coins Team \033[1;37m🛠️")
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")

    await client.send_message(BOT_NAME, '/start')
    time.sleep(2)
    
    bot = await client.get_entity(BOT_NAME)
    res_webview = await client(functions.messages.RequestWebViewRequest(
        peer=bot, bot=bot, platform='android', from_bot_menu=False, url='https://bitfaucet.net/'
    ))
    
    auth_url = res_webview.url
    init_data = auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]
    data = urllib.parse.unquote(init_data)
    
    ua = UserAgent().random
    headers = {
        'User-Agent': ua,
        'Accept': "application/json, text/plain, */*",
        'Content-Type': "application/json",
        'origin': "https://bitfaucet.net",
        'x-requested-with': "org.telegram.messenger",
        'referer': "https://bitfaucet.net/",
    }

    login_req = requests.post("https://api.bitfaucet.net/api/auth/login", json={"initData": data, "referralCode": "6846731693"}, headers=headers)
    res = login_req.json()
    
    token = res['token']
    firstName = res['user']['firstName']
    balance = res['user']['balance']

    slow_print(f"\033[1;32m👋 Welcome {firstName}! Your Balance = {balance} 💰")

    config_file = 'config_faucet.json'
    email = ""
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config_data = json.load(f)
            email = config_data.get("email", "")
        
        print(f"\033[1;32mI Found Email \033[1;33m{email}")
        change = input("\033[1;37mDou u want To change Email Faucet Pay.? (yes/no) => ").lower()
        if change == 'yes':
            email = input("\033[1;37m📩 Enter your FaucetPay Email => ")
            with open(config_file, 'w') as f:
                json.dump({"email": email}, f)
    else:
        email = input("\033[1;37m📩 Enter your FaucetPay Email => ")
        with open(config_file, 'w') as f:
            json.dump({"email": email}, f)

    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")
    slow_print("\033[1;37m     🌟 \033[1;36mScript AutoMation Premium Members \033[1;37m🌟")
    slow_print("\033[1;37m      🛠️  \033[1;32mCreators : \033[1;33mC4-Coins Team \033[1;37m🛠️")
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")    
    head = headers.copy()
    head["authorization"] = f"Bearer {token}"
    
    requests.post("https://api.bitfaucet.net/api/auth/link-faucetpay", json={"address": email}, headers=head)
    coins_res = requests.get("https://api.bitfaucet.net/api/faucet/coins", headers=head).json()

    print("\n\033[1;34m" + "-"*41)
    id_list = []
    for index, coin in enumerate(coins_res, 1):
        print(f"\033[1;33m{index}. \033[1;37m{coin['symbol']}")
        id_list.append(coin['_id'])
    
    select = int(input("\033[1;37m 🔢 Enter Selection Number => "))
    coin_id = id_list[select-1]
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")
    slow_print("\033[1;37m     🌟 \033[1;36mScript AutoMation Premium Members \033[1;37m🌟")
    slow_print("\033[1;37m      🛠️  \033[1;32mCreators : \033[1;33mC4-Coins Team \033[1;37m🛠️")
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")
    while True:
        me_res = requests.get("https://api.bitfaucet.net/api/auth/me", headers=head).json()
        remaining = 50 - me_res['user']['claimsSinceLastShortlink']
        
        if remaining <= 0:
            print(f"\n\033[1;31m⚠️ Shortlink Limit Reached! Switching to Auto-Bypass...")
            await auto_bypass(client, token, email, coin_id)
            continue

        ads_start = requests.post("https://api.bitfaucet.net/api/ads/start", json={"provider": "adsgram_rewarded"}, headers=head).json()
        
        if ads_start.get("success"):
            slow_print("\033[1;32m📺 Get Ads For Claim  ✅ Success")
            adSessionId = ads_start['adSessionId']
            nonce = ads_start['nonce']
            
            for i in range(11, -1, -1):
                sys.stdout.write(f"\r\033[1;33m⏳ Simulating watch ads: {i}s remaining...")
                sys.stdout.flush()
                time.sleep(1)
            sys.stdout.write("\r" + " " * 60 + "\r")

            ads_comp = requests.post("https://api.bitfaucet.net/api/ads/complete", json={
                "adSessionId": adSessionId,
                "nonce": nonce,
                "provider": "adsgram_interstitial",
                "result": "success",
                "meta": {"type": "rewarded"}
            }, headers=head).json()

            if ads_comp.get("status") == "verified" or ads_comp.get("success"):
                slow_print("\033[1;32m⏳ Watch Ads Progress ✅ Verified")
                claim_res = requests.post("https://api.bitfaucet.net/api/faucet/claim", json={
                    "coinId": coin_id, "address": email, "adSessionId": adSessionId
                }, headers=head).json()

                if claim_res.get("success"):
                    amt = claim_res['amountSatoshis']
                    currency = claim_res['currency']
                    f_amt = amt if currency == "PEPE" else "{:.8f}".format(amt / 100000000)
                    slow_print(f"\033[1;32m🎉 Success Payout {f_amt} {currency} to {email}")
                
                print(f"\033[1;37m📊 Claims remaining before shortlink = {remaining - 1} x")

                for i in range(11, -1, -1):
                    sys.stdout.write(f"\r\033[1;37m🕒 Next claim In {i}s")
                    sys.stdout.flush()
                    time.sleep(1)
                sys.stdout.write("\r" + " " * 50 + "\r")
            else:
                time.sleep(5)

# BAGIAN INI YANG DIPASTIKAN BISA JALAN ASYNC
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run())
    except KeyboardInterrupt:
        print("\n\033[1;31m🛑 Stopped by user.")
        print("\033[1;34m" + "="*41)
        choice = input("\033[1;37mDo u want to change number telegram ..?\nIf want to change enter \033[1;32myes \033[1;37mand if dont want to change enter \033[1;31mno \033[1;37m=> ").lower()
        
        if choice == 'yes':
            if os.path.exists('c4coins.session'):
                os.remove('c4coins.session')
                print("\033[1;32m✅ Session deleted. Next run will ask for new number.")
            else:
                print("\033[1;33m⚠️ No session file found.")
        else:
            print("\033[1;36mℹ️ Session kept. Script closed.")
        
        print("\033[1;34m" + "="*41)
        sys.exit()
