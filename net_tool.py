#!/usr/bin/env python3
import os
import sys
import time
import socket
import subprocess
import threading
import random
import re
from datetime import datetime

# --- Auto Dependency Installer ---
def install_dependencies():
    print("\033[93m[*] Dependencies missing. Installing jutsu scrolls (libraries)...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "colorama", "speedtest-cli"])
        print("\033[92m[+] Dependencies installed! Restarting tool...\033[0m")
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        print(f"\033[91m[-] Failed to install dependencies: {e}\033[0m")
        sys.exit(1)

try:
    import requests
    from requests.auth import HTTPBasicAuth, HTTPDigestAuth
    from colorama import Fore, Style, init
    import speedtest
except ImportError:
    install_dependencies()

# Initialize colors
init(autoreset=True)

class NetworkTool:
    def __init__(self):
        self.running = False
        self.gateway_ip = "Unknown"
        self.target_host = "8.8.8.8" 
        
        # Background Monitor Variables
        self.bg_monitor_active = False
        self.current_latency = 0
        self.connection_status = "Offline"
        self.packet_loss_count = 0
        self.monitor_thread = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def banner(self):
        print(Fore.CYAN + Style.BRIGHT + """
    ╔════════════════════════════════════════╗
    ║        TERMUX NETWORK CONNECT V5       ║
    ║        [ BD Edition - TP-Link ]        ║
    ╚════════════════════════════════════════╝
    """ + Style.RESET_ALL)

    # --- Background Process ---
    def _monitor_loop(self):
        while self.bg_monitor_active:
            try:
                # Silent Ping
                output = subprocess.check_output(
                    ["ping", "-c", "1", "-W", "2", self.target_host], 
                    stderr=subprocess.STDOUT, 
                    text=True
                )
                match = re.search(r'time=(\d+\.?\d*)', output)
                if match:
                    self.current_latency = float(match.group(1))
                    self.connection_status = "Online"
                else:
                    self.current_latency = 999
                    self.connection_status = "High Latency"
            except:
                self.current_latency = 0
                self.connection_status = "Offline"
                self.packet_loss_count += 1
            time.sleep(1.5)

    def start_background_monitor(self):
        if not self.bg_monitor_active:
            self.bg_monitor_active = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            print(Fore.GREEN + "[*] Background Monitor Started (Chakra Flowing)...")

    def stop_background_monitor(self):
        self.bg_monitor_active = False

    # --- Utilities ---
    def get_gateway_ip(self):
        try:
            result = subprocess.check_output(["ip", "route"], text=True)
            match = re.search(r'default via (\d+\.\d+\.\d+\.\d+)', result)
            if match:
                self.gateway_ip = match.group(1)
            else:
                self.gateway_ip = "Not Found"
        except:
            self.gateway_ip = "Error"
        return self.gateway_ip

    def update_tool(self):
        print(Fore.YELLOW + "\n[*] Checking for updates from the Cloud (GitHub)...")
        try:
            if not os.path.isdir(".git"):
                print(Fore.RED + "[-] This tool was not installed via Git.")
                return

            print(Fore.CYAN + "[*] Pulling latest scrolls...")
            result = subprocess.run(["git", "pull"], capture_output=True, text=True)
            
            if "Already up to date" in result.stdout:
                print(Fore.GREEN + "[+] Your tool is already up to date! Dattebayo!")
            elif result.returncode == 0:
                print(Fore.GREEN + "[+] Update Successful! Restarting tool...")
                os.execv(sys.executable, ['python'] + sys.argv)
            else:
                print(Fore.RED + "[-] Update Failed.")
        except Exception as e:
            print(Fore.RED + f"[-] Update Error: {e}")

    # --- Features ---
    def display_stats(self):
        self.clear_screen()
        self.banner()
        print(Fore.YELLOW + "LIVE MONITOR (Press Ctrl+C to return to menu)")
        print(Fore.CYAN + "-" * 50)
        try:
            while True:
                lat = self.current_latency
                if self.connection_status == "Offline": color = Fore.RED
                elif lat < 80: color = Fore.GREEN
                elif lat < 150: color = Fore.YELLOW
                else: color = Fore.RED

                msg = f"\rStatus: {color}{self.connection_status:<10} {Fore.WHITE}| Latency: {color}{lat} ms {Fore.WHITE}| Loss Events: {Fore.RED}{self.packet_loss_count}"
                sys.stdout.write(msg)
                sys.stdout.flush()
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass

    def packet_sender(self):
        print(Fore.YELLOW + "\n[*] Packet Sender (Data Transmission Test)")
        target = input("Target Domain/IP (e.g., google.com): ").strip()
        try:
            port = int(input("Port (default 80): ").strip() or "80")
            size_mb = float(input("Data Size in MB (e.g., 1): ").strip() or "1")
        except ValueError:
            print(Fore.RED + "Invalid number.")
            return

        if size_mb > 10: size_mb = 10
        size_bytes = int(size_mb * 1024 * 1024)
        print(Fore.CYAN + f"[*] Generating {size_mb} MB payload...")
        payload = b'A' * size_bytes 
        
        print(Fore.YELLOW + f"[*] Connecting to {target}:{port}...")
        try:
            start_time = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((target, port))
            print(Fore.GREEN + "[*] Sending Data...")
            s.sendall(payload)
            s.close()
            duration = time.time() - start_time
            print(Fore.GREEN + f"[+] Sent in {duration:.2f}s | Speed: {size_mb / duration:.2f} MB/s")
        except Exception as e:
            print(Fore.RED + f"[-] Failed: {e}")

    def fetch_router_logs(self):
        self.get_gateway_ip()
        print(Fore.YELLOW + "\n[*] Router Log Extractor (TP-Link Optimized)")
        default_path = "/userRpm/SysLogRpm.htm"
        use_default = input(f"Use default path ({default_path})? (y/n): ").lower()
        log_path = default_path if use_default != 'n' else input("Custom path: ").strip()
        if not log_path.startswith("/"): log_path = "/" + log_path
        
        full_url = f"http://{self.gateway_ip}{log_path}"
        user = input("User (admin): ").strip() or "admin"
        pwd = input("Pass (admin): ").strip() or "admin"

        print(Fore.YELLOW + f"[*] Accessing {full_url}...")
        try:
            r = requests.get(full_url, auth=HTTPBasicAuth(user, pwd), timeout=5)
            if r.status_code == 401:
                r = requests.get(full_url, auth=HTTPDigestAuth(user, pwd), timeout=5)

            if r.status_code == 200:
                print(Fore.GREEN + "[+] LOGS FOUND!")
                clean = re.sub('<[^<]+?>', ' ', r.text)
                lines = [l.strip() for l in clean.splitlines() if l.strip()]
                for line in lines[-15:]: print(line[:80])
                if input(Fore.WHITE + "\nSave log? (y/n): ").lower() == 'y':
                    with open("router_log.txt", "w") as f: f.write(r.text)
                    print(Fore.GREEN + "Saved.")
            else:
                print(Fore.RED + f"[-] Failed. Code: {r.status_code}")
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

    def hacker_mode(self):
        """Toy feature: Plays a hacker animation."""
        print(Fore.RED + "\n[!] WARNING: ENTERING SECRET MODE [!]")
        try:
            duration = int(input(Fore.WHITE + "Set Duration (seconds): "))
        except:
            return

        print(Fore.GREEN + "[*] Initializing Matrix Protocol...")
        time.sleep(1)
        
        phrases = [
            "Encrypting handshake...", "Bypassing Firewall Layer 7...", 
            "Injecting payload 0x44A...", "Root access: PENDING...", 
            "Decrypting hash...", "Tracing Packet Route...", 
            "Accessing Mainframe...", "Downloading database...",
            "Overriding security protocols...", "Establishing secure tunnel..."
        ]
        
        end_time = time.time() + duration
        try:
            while time.time() < end_time:
                action = random.choice([1, 2, 3])
                if action == 1:
                    # Print fake hex dump
                    hex_str = " ".join([f"{random.randint(0, 255):02X}" for _ in range(8)])
                    print(Fore.GREEN + f"0x{random.randint(1000, 9999)}: {hex_str} | ...")
                elif action == 2:
                    # Print fake command
                    print(Fore.WHITE + f"[*] {random.choice(phrases)}")
                else:
                    # Print binary
                    print(Fore.CYAN + "".join([str(random.randint(0, 1)) for _ in range(40)]))
                
                time.sleep(random.uniform(0.05, 0.3))
            
            print(Fore.GREEN + Style.BRIGHT + "\n[+] ACCESS GRANTED. SYSTEM COMPROMISED.")
            print(Fore.WHITE + "(Just kidding! This was a simulation.)")
            input("\nPress Enter to return...")
        except KeyboardInterrupt:
            print("\nAborted.")

    # --- Main Menu ---
    def start(self):
        self.clear_screen()
        self.banner()
        print(Fore.WHITE + "Type " + Fore.GREEN + "connect" + Fore.WHITE + " to initialize system.")
        
        while True:
            try:
                cmd = input(Fore.CYAN + "\ntermux-net > " + Fore.RESET).strip().lower()
                
                if cmd == "connect":
                    self.start_background_monitor()
                    while True:
                        print(Fore.GREEN + "\n[ System Connected ]")
                        print(Fore.WHITE + "1. Live Stats")
                        print(Fore.WHITE + "2. Packet Sender")
                        print(Fore.WHITE + "3. Router Logs")
                        print(Fore.WHITE + "4. Disconnect")
                        print(Fore.YELLOW + "5. Update Tool")
                        print(Fore.MAGENTA + "6. Hacker Mode (Toy)")
                        
                        choice = input(Fore.YELLOW + "Select > " + Fore.RESET)
                        
                        if choice == "1": self.display_stats()
                        elif choice == "2": self.packet_sender()
                        elif choice == "3": self.fetch_router_logs()
                        elif choice == "4":
                            self.stop_background_monitor()
                            print(Fore.RED + "[*] Disconnected.")
                            break
                        elif choice == "5": self.update_tool()
                        elif choice == "6": self.hacker_mode()
                        else: print("Invalid option.")

                elif cmd == "exit":
                    if self.bg_monitor_active: self.stop_background_monitor()
                    print(Fore.GREEN + "Sayonara! 👋")
                    sys.exit(0)
                else:
                    print("Type 'connect' first.")
            except KeyboardInterrupt:
                if self.bg_monitor_active: self.stop_background_monitor()
                sys.exit(0)

if __name__ == "__main__":
    t = NetworkTool()
    t.start()
