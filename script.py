import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def try_click(driver, by, locator):
    button = driver.find_elements(by, locator)
    if not button:
        return False
    try:
        print("try wait ", locator)
        button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((by, locator)))
        button.click()
        return True
    except Exception as err:
        print(f"Click err: {err}")
        return False


def wheel_button(driver):
    driver.get("https://vmmo.ru/cabinet/wheel")
    input("Website opened. Login or solve captcha before and press any key..")
    while True:
        print("New cycle")
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
