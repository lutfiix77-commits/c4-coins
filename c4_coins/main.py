import os
import sys
import time
import importlib

def slow_print(text, speed=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")
    slow_print("\033[1;37m     🌟 \033[1;36mPremium Automation Script Members \033[1;37m🌟")
    slow_print("\033[1;37m      🛠️  \033[1;32mCreators : \033[1;33mC4-Coins Team \033[1;37m🛠️")
    print("\033[1;34m" + "💎 " + "="*41 + " 💎")
    
    print("\n\033[1;37m    [ SELECT YOUR COMMAND ]")
    print("\033[1;34m  ─────────────────────────────")
    print("\033[1;32m  1. \033[1;37mAdBeast Auto Claim")
    print("\033[1;32m  2. \033[1;37mBitFaucet Auto Claim")
    print("\033[1;34m  ─────────────────────────────")
    print("\033[1;31m  0. \033[1;37mExit")
    
    choice = input("\n\033[1;36m[?] Please input number \033[1;37m => ")

    # Pakai nama murni tanpa titik dulu buat mapping
    menu_map = {
        '1': 'adbeast',
        '2': 'bitfaucet'
    }

    if choice == '0':
        print("\n\033[1;32m[!] Thank you for using our services. Goodbye!\033[0m")
        sys.exit()

    if choice in menu_map:
        try:
            module_name = menu_map[choice]
            
            # Logika Adaptif: Cek kalau jalan sebagai package (pip) atau file lokal
            if __package__:
                # Kalau dari pip, wajib pakai titik di depan
                script = importlib.import_module(f".{module_name}", package=__package__)
            else:
                # Kalau jalan manual 'python main.py'
                script = importlib.import_module(module_name)
            
            script.run()
            
        except ImportError as e:
            print(f"\n\033[1;31m[!] Error: {module_name} not found! ({e})\033[0m")
            time.sleep(2)
            main()
        except Exception as e:
            print(f"\n\033[1;31m[!] Unexpected Error: {e}\033[0m")
            time.sleep(3)
            main()
    else:
        print("\n\033[1;31m[!] Invalid Option!")
        time.sleep(2)
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[1;31m[!] Operation cancelled by user.\033[0m")
        sys.exit()    if choice == '0':
        print("\n\033[1;32m[!] Thank you for using our services. Goodbye!\033[0m")
        sys.exit()

    if choice in menu_map:
        try:
            module_name = menu_map[choice]
            script = importlib.import_module(module_name, package=__package__)
            script.run()
            
        except ImportError:
            print(f"\n\033[1;31m[!] Error: {module_name} not found!\033[0m")
            time.sleep(2)
            main()
        except AttributeError:
            print(f"\n\033[1;31m[!] Error: Function 'run()' not found in {module_name}!\033[0m")
            time.sleep(2)
            main()
        except Exception as e:
            print(f"\n\033[1;31m[!] Unexpected Error: {e}\033[0m")
            time.sleep(3)
            main()
    else:
        print("\n\033[1;31m[!] Invalid Option!")
        time.sleep(2)
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[1;31m[!] Operation cancelled by user.\033[0m")
        sys.exit()
    if choice == '0':
        print("\n\033[1;32m[!] Thank you for using our services. Goodbye!\033[0m")
        sys.exit()

    if choice in menu_map:
        try:
            module_name = menu_map[choice]
            # Dynamic Import
            script = importlib.import_module(module_name)
            
            # This triggers the 'run' function in your sub-files
            script.run()
            
        except ImportError:
            print(f"\n\033[1;31m[!] Error: {module_name}.py not found!\033[0m")
            time.sleep(2)
            main()
        except AttributeError:
            print(f"\n\033[1;31m[!] Error: Function 'run()' not found in {module_name}.py!\033[0m")
            time.sleep(2)
            main()
        except Exception as e:
            print(f"\n\033[1;31m[!] Unexpected Error: {e}\033[0m")
            time.sleep(3)
            main()
    else:
        print("\n\033[1;31m[!] Invalid Option!")
        time.sleep(2)
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[1;31m[!] Operation cancelled by user.\033[0m")
        sys.exit()
