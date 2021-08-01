import pexpect
import signal
import sys
from time import sleep

def make_child():
    return pexpect.spawn('gnirehtet', args=["run"],
            encoding='utf-8', logfile=sys.stdout, timeout=None)

def clean_quit(sig=None, frame=None):
    print("[log] Quitting...")
    child.kill(signal.SIGINT)
    exit(0)

signal.signal(signal.SIGINT, clean_quit)

def respawn():
    print("[log] Restarting...")
    child.kill(signal.SIGINT)
    child = make_child()

patterns = {
        "ERROR Main:":"quit",
        "disconnected":"disconnected",
        "connected":"connected"
        }
restarting = False
while True:
    child = make_child()
    while True:
        print("expecting...")
        matched = None
        try:
            matched = child.expect(list(patterns.keys()))
        except pexpect.exceptions.EOF:
            restarting = True
            child.kill(signal.SIGINT)
            break
        action = list(patterns.values())[matched]
        if action == "disconnected":
            print("[log] Restarting...")
            restarting = True
            child.kill(signal.SIGINT)
            break
        elif action == "connected":
            print("[log] Restarted")
            restarting = False
        elif action == "quit":
            print("[log] Restarting...")
            sleep(1)
            restarting = True
            child.kill(signal.SIGINT)
            break

