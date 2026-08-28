import os
import subprocess
from selenium import webdriver
from selenium.webdriver.common import utils


def Init(baseurl: str = "https://www.google.com"):
    port = utils.free_port()
    print(f"Start browser on port:{port}")
    profile_dir = os.path.join(os.path.dirname(__file__), "chrome_profile")
    os.makedirs(profile_dir, exist_ok=True)
    gchrome = [
        "google-chrome-stable",
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile_dir}",
        "--new-window",
        baseurl,
        "--disable-features=IsolateOrigins,site-per-process",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-popup-blocking",
        "--disable-infobars",
        "--log-level=3"
    ]
    proc = subprocess.Popen(gchrome)
    print(f"browser pid:{proc.pid}")

    options = webdriver.ChromeOptions()
    options.to_capabilities()['goog:loggingPrefs'] = {'browser': 'ALL'}
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    driver = webdriver.Chrome(options=options)
    # .get(url: str) -> open URL
    # .back()-> return previous URL
    # .quit() -> close driver and all windows, end session
    return driver
