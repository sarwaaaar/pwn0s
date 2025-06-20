#!/usr/bin/env python3
import subprocess
import shlex
import os
import sys
import getpass
import time
import signal
import threading
import json

def is_ish_terminal():
    try:
        if 'ISH' in os.environ:
            return True
        with open('/proc/version', 'r') as f:
            return 'ish' in f.read().lower()
    except:
        return False

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[38;2;204;103;102m"
PINK = "\033[38;2;227;148;220m"
YELLOW = "\033[38;2;222;147;95m"
AFB3B5 = "\033[38;2;175;179;181m"
VERSION = "0.3.9"

def clear_screen():
    if is_ish_terminal():
        print("\033[2J\033[H", end="")
        print("\033[3J", end="")
        print("\033c", end="")
        print("\n" * 3)
        sys.stdout.flush()
        time.sleep(0.05)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.flush()

def print_ascii_art():
    print(ASCII_ART)

def show_loading_indicator(message, duration=2):
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    while time.time() < end_time:
        for char in spinner:
            if time.time() >= end_time:
                break
            print(f"\r{YELLOW}[~] {message} {char}{RESET}", end='', flush=True)
            time.sleep(0.1)
    print("\r" + " " * (len(message) + 10) + "\r", end='', flush=True)

def connect_ssh(host, password):
    try:
        if '@' not in host:
            print(f"{RED}[!] Invalid host format. Use: user@host{RESET}")
            return
        clear_screen()
        print_ascii_art()
        print(f"{PINK}Preparing SSH connection to {host}...{RESET}")
        show_loading_indicator(f"Connecting to {host}...", duration=2)
        if is_ish_terminal():
            ssh_cmd = f"sshpass -p {shlex.quote(password)} ssh -o StrictHostKeyChecking=no {host}"
            process = subprocess.Popen(
                ssh_cmd,
                shell=True,
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr,
                universal_newlines=True
            )
            process.wait()
        else:
            ssh_cmd = [
                "sshpass", "-p", password,
                "ssh", "-o", "StrictHostKeyChecking=no", host
            ]
            import pty
            pty.spawn(ssh_cmd)
        clear_screen()
        print_ascii_art()
        print(f"{PINK}SSH session ended.{RESET}")
    except KeyboardInterrupt:
        print(f"\n{PINK}SSH session terminated.{RESET}")
    except Exception as e:
        print(f"{RED}[!] Connection error: {str(e)}{RESET}")

def main():
    clear_screen()
    # Read config.json for credentials
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    if not os.path.exists(config_path):
        print(f"{RED}[!] config.json not found in {os.path.dirname(os.path.abspath(__file__))}{RESET}")
        print(f"{YELLOW}Please create a config.json with username, ip, and password.{RESET}")
        sys.exit(1)
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        username = config.get('username')
        ip = config.get('ip')
        password = config.get('password')
        if not username or not ip or not password:
            print(f"{RED}[!] config.json must contain username, ip, and password.{RESET}")
            sys.exit(1)
        user_host = f"{username}@{ip}"
        print(f"{PINK}Attempting SSH connection to {user_host}...{RESET}")
        connect_ssh(user_host, password)
    except Exception as e:
        print(f"{RED}[!] Failed to read config.json: {str(e)}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()