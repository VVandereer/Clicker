import time
import threading
from pathlib import Path


def jsInjection(path="clickLogger.js"):
    script_path = Path(__file__).parent / path
    with open(script_path, 'r', encoding='utf-8') as f:
        return f.read()


def console_read(driver, stop_event):
    last_timestamp = None
    while not stop_event.is_set():
        logs = driver.get_log('browser')
        for entry in logs:
            if last_timestamp is None or entry['timestamp'] > last_timestamp:
                message = entry.get('message', '')
                if 'CLICK_EVENT:' in message:
                    print(f"Click: {message}")
                last_timestamp = entry['timestamp']
            time.sleep(0.05)


class ClickMonitor:
    def __init__(self, driver):
        self.__driver = driver
        self.__stop_event = threading.Event()
        self.thread = threading.Thread(target=console_read,
                                       args=(driver, self.__stop_event))

    def start(self):
        self.__driver.execute_script(jsInjection())
        self.thread.start()

    def stop(self):
        self.__stop_event.set()
        if self.thread is not None and self.thread.is_alive():
            self.thread.join()
