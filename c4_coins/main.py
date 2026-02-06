import requests
import json
import time
import sys
import os
import random
import base64
import re
import emoji
from datetime import datetime, timedelta

# --- FUNGSI GLOBAL ---
def slow_print(text, speed=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def adbeast_script():
    # --- LOGIC ASLI (TIDAK DIUBAH) ---
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EX_PATH = os.path.join(BASE_DIR, '..', 'ex')
    FILE_PATH = os.path.join(EX_PATH, 'time.json')

    def setup_expired():
        if not os.path.exists(EX_PATH):
            os.makedirs(EX_PATH)
        if not os.path.exists(FILE_PATH):
            start_time = datetime.now()
            expired_time = start_time + timedelta(days=3)
            data = {"start": start_time.strftime("%Y-%m-%d %H:%M:%S"), "expired": expired_time.strftime("%Y-%m-%d %H:%M:%S")}
            with open(FILE_PATH, 'w') as f: json.dump(data, f)
            return data
        else:
            with open(FILE_PATH, 'r') as f: return json.load(f)

    def get_remaining_time(expired_str):
        expired_dt = datetime.strptime(expired_str, "%Y-%m-%d %H:%M:%S")
        remaining = expired_dt - datetime.now()
        if remaining.total_seconds() <= 0: return None
        days = remaining.days
        hours, rem = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        return f"{days} days {hours} hour {minutes} min"

    def check_expired():
        data = setup_expired()
        remaining = get_remaining_time(data['expired'])
        if remaining is None:
            print("\n\033[1;31m[!] SCRIPT EXPIRED! Please contact admin.\033[0m")
            sys.exit()
        return data

    def generate_ua():
        android_vers = random.randint(10, 14)
        chrome_vers = f"{random.randint(110, 130)}.0.{random.randint(1000, 6000)}.{random.randint(10, 200)}"
        device_models = ["SM-G960F", "Pixel 7", "M2012K11AG", "RMX3301", "POCO F3"]
        return f"Mozilla/5.0 (Linux; Android {android_vers}; {random.choice(device_models)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_vers} Mobile Safari/537.36"

    def solve_captcha(json_data):
        challenge_raw = json_data.get("challenge", "")
        target_keyword = challenge_raw.replace("Select the ", "").lower().strip()
        for option in json_data.get("options", []):
            try:
                base64_str = option['data'].split(',')[1]
                decoded_svg = base64.b64decode(base64_str).decode('utf-8')
                match = re.search(r'>([^<]+)</text>', decoded_svg)
                if match:
                    found_emoji = match.group(1)
                    emoji_name = emoji.demojize(found_emoji).replace(":", "").replace("_", " ").lower()
                    if target_keyword in emoji_name or emoji_name in target_keyword: return option['id']
            except Exception: continue
        return None

    data_time = check_expired()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")
    slow_print("\033[1;37m     🌟 \033[1;36mScript AutoMation Premium Members \033[1;37m🌟")
    slow_print("\033[1;37m      🛠️  \033[1;32mCreators : \033[1;33mC4-Coins Team \033[1;37m🛠️")
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")
    slow_print(f"\n\033[1;37m[#] \033[1;32mExpired At : \033[1;33m{data_time['expired']}")
    slow_print("\033[1;37m[#] \033[1;32mStatus     : \033[1;36mTrial 3 Days \033[1;37m| \033[1;32mMode: \033[1;33mHigh-Speed ⚡\n")

    email = input("\033[1;37m[?] Enter your FaucetPay Email: \033[1;33m")
    ua = generate_ua()
    fp = "".join(random.choices("0123456789abcdef", k=8))
    headers = {
    'User-Agent': ua,
    'Accept': "application/json, text/plain, */*",
    'Content-Type': "application/json",
    'sec-ch-ua-platform': "\"Android\"",
    'x-requested-with': "XMLHttpRequest", # WAJIB ADA
    'sec-ch-ua': f"\"Chromium\";v=\"130\", \"Android WebView\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    'origin': "https://faucet.adbeast.xyz",
    'referer': "https://faucet.adbeast.xyz/",
    'accept-language': "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
}

    login_url = "https://faucetapis.adbeast.xyz/api/auth/login"
    login_payload = {"identifier": email, "referredBy": "KV2EJO7O", "fingerprint": fp, "botMetadata": {"webdriver": False, "hasChrome": False, "languages": 2, "plugins": 0, "isTampermonkey": False, "isDebuggerOpen": False, "hardware": 8, "memory": 4, "touchPoints": 5}}

    try:
        resp_login = requests.post(login_url, data=json.dumps(login_payload), headers=headers)
        if resp_login.status_code == 200:
            res_json = resp_login.json()
            if res_json.get("success"):
                cookie_raw = resp_login.headers.get("set-cookie")
                token_val = cookie_raw.split("token=")[1].split(";")[0]
                token = f"token={token_val}"
                slow_print(f"\033[1;32m[!] Login Successful! Welcome: {res_json['user']['username']}")
                head = headers.copy(); head["Cookie"] = token
                while True:
                    check_expired()
                    try:
                        status_url = "https://faucetapis.adbeast.xyz/api/faucet/status"
                        status_resp = requests.get(status_url, headers=head).json()
                        claimsLeft = status_resp.get("claimsLeft", 0)
                        session = status_resp.get("sessionToken")
                        slow_print(f"\033[1;34m[#] Remaining claims today : \033[1;37m{claimsLeft}")
                        if claimsLeft == 0: break
                        captcha_url = "https://faucetapis.adbeast.xyz/api/faucet/captcha"
                        cap_resp = requests.get(captcha_url, headers=head).json()
                        result_id = solve_captcha(cap_resp)
                        if result_id:
                            claim_url = "https://faucetapis.adbeast.xyz/api/faucet/claim"
                            claim_payload = {"captcha_answer": result_id, "challenge_id": cap_resp.get("challengeId"), "claim_token": cap_resp.get("claimToken"), "session_token": session, "fingerprint": fp, "botMetadata": {"webdriver": False, "hasChrome": False, "languages": 2, "plugins": 0, "isTampermonkey": False, "isDebuggerOpen": False, "hardware": 8, "memory": 4, "touchPoints": 5}, "behaviorData": {"moveCount": random.randint(5, 15), "movePattern": [], "clickCoords": {"x": random.randint(100, 400), "y": random.randint(200, 500)}, "hasKeyboard": False, "isTrusted": True, "honeypot": False, "duration": random.randint(2000, 4000)}, "claim_speed": random.randint(2000, 3000)}
                            claim_res = requests.post(claim_url, data=json.dumps(claim_payload), headers=head).json()
                            if claim_res.get("success"):
                                slow_print(f"\033[1;32m[✔] Claim Success! Sent {float(claim_res.get('amount')):.8f} TRX")
                            else: slow_print(f"\033[1;31m[✖] Claim Failed: {claim_res.get('message')}")
                        else: slow_print("\033[1;31m[!] Emoji mapping failed.")
                        for i in range(10, 0, -1):
                            sys.stdout.write(f"\r\033[1;37m[#] Wait for next claim: \033[1;33m{i}s   "); sys.stdout.flush(); time.sleep(1)
                    except Exception as e: 
                        print(f"Error Loop: {e}")
                        time.sleep(5)
            else: 
                print(f"Login Gagal: {res_json.get('message')}")
                sys.exit()
        else:
            print(f"HTTP Error: {resp_login.status_code}")
            sys.exit()
    except Exception as e:
        # INI BIAR KELUAR PESANNYA KALAU CRASH
        print(f"\n\033[1;31m[!] CRASH DETECTED: {e}\033[0m")
        sys.exit()

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")
    slow_print("\033[1;37m     🌟 \033[1;36mScript AutoMation Premium Members \033[1;37m🌟")
    slow_print("\033[1;37m      🛠️  \033[1;32mCreators : \033[1;33mC4-Coins Team \033[1;37m🛠️")
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")
    print("\n\033[1;37m    [ SELECT YOUR COMMAND ]")
    print("\033[1;34m  ─────────────────────────────")
    slow_print("\033[1;32m  1. \033[1;37mAdBeast Auto Claim")
    print("\033[1;34m  ─────────────────────────────")
    choice = input("\n\033[1;36m[?] Please input number \033[1;37m => ")
    if choice == '1':
        adbeast_script()
    else:
        print("\n\033[1;31m[!] Invalid Option!")
        time.sleep(2)
        main()

if __name__ == "__main__":
    main()
