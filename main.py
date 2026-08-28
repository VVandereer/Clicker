import time
import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from clickMonitor import clickMonitor


def try_click(driver, by, locator):
    button = driver.find_elements(by, locator)
    if not button:
        return False
    try:
        print("try wait ", locator)
        button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((by, locator)))
        button.click()
        return True
    except TimeoutException:
        return False


def main():
    print("Hello from Clicker!")
    driver = webdriver.Init()
    driver.get("https://vmmo.ru/cabinet/wheel")
    input("Browser opened. Login or solve captcha before and press any key..")

    clickLogger = clickMonitor(driver)
    if True:
        clickLogger.start()
        print("Now clicks on will be catched and print in console log")

    input("Press any key to start script..")
    try:
        while True:
            print("main loop still alive")
            if try_click(driver, By.CSS_SELECTOR, '[onclick="return wheelButton(this);"]'):
                time.sleep(1)
                if driver.find_elements(By.CSS_SELECTOR, "[data-fullscreen-element-name='timeout']"):
                    print("Wait ads end")
                    while driver.find_elements(By.CSS_SELECTOR, "[data-fullscreen-element-name='timeout']"):
                        time.sleep(0.5)
                    print("Close ads")
                    try_click(driver, By.CSS_SELECTOR, '[data-fullscreen-element-name="close-btn"]')
                    time.sleep(0.5)
                    continue
                print("Spin Wheel")
                time.sleep(4)
                if try_click(driver, By.CSS_SELECTOR, '''a[onclick="$('#wheel-error-prize').removeClass('_show'); reload();"]'''):
                    print("Refuse metareward")
                if try_click(driver, By.CSS_SELECTOR, 'a[onclick="return showHintNew();"]'):
                    print("Get reward")
                    time.sleep(0.5)
                    continue
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        clickLogger.stop()
        driver.quit()
        print("correctly stopped")


if __name__ == "__main__":
    main()
    # <a class="vmmo-wheel-button" id="wheel-button" onclick="return wheelButton(this);"></a>
    # <span class="s9094f31c">Награда начислится через</span>
    # data-fullscreen-element-name="close-btn"
    # class="vmmo-prize-wrapper _show"
    # <a class="button-large _low" onclick="return showHintNew();">ПОЛУЧИТЬ</a>
    # <a class="button-large _low" onclick="$('#wheel-error-prize').removeClass('_show'); reload();">ОТЛОЖИТЬ</a>
