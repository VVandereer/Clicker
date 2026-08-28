import time
import webdriver
from clickMonitor import clickMonitor


def main():
    print("Hello from Clicker!")
    driver = webdriver.Init()
    driver.get("https://vmmo.ru/cabinet/wheel")
    input("Browser opened. Login or solve captcha before and press any key..")

    clickLogger = clickMonitor(driver)
    if True:
        clickLogger.start()
        print("Now clicks on will be catched and print in console log")
    try:
        while True:
            print("main loop still alive")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        clickLogger.stop()
        driver.quit()


if __name__ == "__main__":
    main()
