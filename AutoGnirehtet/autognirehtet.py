import pexpect
import signal
import sys
from time import sleep, time
from ppadb.client import Client as AdbClient
import subprocess
import threading
from pprint import pprint
from random import random
from functools import partial

class DeviceHandler:
    def __init__(self, device_serial):
        # Serial number of the device to care of
        self.serial = device_serial
        self.child = None
        self.running = False
    def make_child(self):
        port = int(random()*1000)+1000
        return pexpect.spawn('gnirehtet', args=["run", self.serial, "-p", str(port)],
                encoding='utf-8', logfile=sys.stdout, timeout=None)

    def clean_quit(self):
        print("[log] Quitting...")
        self.child.kill(signal.SIGINT)
        self.running = False

    def run(self):
        patterns = {
                "ERROR Main:":"quit",
                "disconnected":"disconnected",
                "connected":"connected"
        }
        self.child = self.make_child()
        self.running = True
        disconnected = True
        lastConnectedTime = time()
        while self.running:
            if disconnected:
                disconnectedDuration = time()-lastConnectedTime
                # print(f"Duration: {disconnectedDuration}")
                if disconnectedDuration > 3:
                    self.clean_quit()
                    break
            print("expecting...")
            matched = None
            try:
                matched = self.child.expect(list(patterns.keys()), timeout=1)
            except pexpect.exceptions.EOF:
                self.child.kill(signal.SIGINT)
                self.clean_quit()
                break
            except pexpect.exceptions.TIMEOUT:
                continue
            action = list(patterns.values())[matched]
            if action == "disconnected" or action == "quit":
                disconnected = True
                lastConnectedTime = time()
                # self.clean_quit()
                # break
            elif action == "connected":
                disconnected = False
                print("[log] Connected")


class MainLoop:
    def __init__(self):
        self.global_running = False
        signal.signal(signal.SIGINT, lambda signal,frame: self.stop() )
    def stop(self):
        print("STOPPING !!!")
        self.global_running = False
    def run(self):
        PORT = 5037
        self.global_running = True
        subprocess.run(["adb", "start-server", "-P", str(PORT)])
        client = AdbClient(host="127.0.0.1")
        def get_device_list():
            return [ d.serial for d in client.devices() ]
        print(get_device_list())
        handlers_map = {}
        def sync_handlers(handlers_map, devices_list):
            # First pop all not running handlers
            handled_devices = list(handlers_map.keys())
            for device_serial in handled_devices:
                (handler, thread) = handlers_map[device_serial]
                if not handler.running:
                    handlers_map.pop(device_serial)
            # Creating the needed handlers
            for device_serial in devices_list:
                if not device_serial in handlers_map.keys():
                    new_handler = DeviceHandler(device_serial)
                    new_handler_thread = threading.Thread(target=new_handler.run)
                    handlers_map[device_serial] = (new_handler, new_handler_thread)
                    new_handler_thread.start()

        def pprint_handlers(handlers_map):
            pprint(
                dict(zip(
                    handlers_map.keys(),
                    map(lambda h: (f"running: {h[0].running}", f"thread: {h[1].is_alive()}"),
                            handlers_map.values()))
            ))
        while self.global_running:
            print(f"self.global_running: {self.global_running}")
            sync_handlers(handlers_map, get_device_list())
            pprint_handlers(handlers_map)
            sleep(1)

        for (handler,thread) in handlers_map.values():
            handler.clean_quit()
            thread.join()

def run():
    mainloop = MainLoop()
    mainloop.run()
