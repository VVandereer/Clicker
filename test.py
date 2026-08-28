import time
import subprocess
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException

# ------------------------------------------------------------
# 1. Постоянный профиль Chrome
# ------------------------------------------------------------
profile_dir = os.path.join(os.path.dirname(__file__), "chrome_profile")
os.makedirs(profile_dir, exist_ok=True)
port = 9222

game_url = "https://orteil.dashnet.org/cookieclicker"
game_url2 = "https://mferma.ru"

subprocess.Popen([
        "google-chrome-stable",
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile_dir}",
        "--new-window",
        game_url,
        "--disable-blink-features=AutomationControlled",
        "--disable-features=IsolateOrigins,site-per-process",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-popup-blocking",
        "--disable-infobars",
        "--log-level=3"
])

print("✅ Chrome запущен. Ожидаем загрузки...")
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
driver = webdriver.Chrome(options=options)

try:
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
except Exception as err:
    print(err)
    driver.quit()
    exit()

print("✅ Браузер открыт и страница загружена.")
print("👉 Пройдите капчу вручную (если она появится) и убедитесь, что вы на странице игры.")
print("⏳ Когда будете готовы начать логирование, нажмите Enter...")
input()

try:
    driver.current_url
except InvalidSessionIdException:
    print("❌ Сессия закрыта. Перезапустите скрипт.")
    driver.quit()
    exit()

# ------------------------------------------------------------
# 2. Внедряем слушатель кликов
# ------------------------------------------------------------
driver.execute_script("""
    window.__clicks = [];
    document.addEventListener('click', function(e) {
        function getXPath(el) {
            if (el.id) return '//*[@id="' + el.id + '"]';
            if (el === document.body) return '/html/body';
            var idx = 1;
            var siblings = el.parentNode.childNodes;
            for (var i = 0; i < siblings.length; i++) {
                var sibling = siblings[i];
                if (sibling === el) break;
                if (sibling.nodeType === 1 && sibling.tagName === el.tagName) idx++;
            }
            var xpath = '/' + el.tagName.toLowerCase() + '[' + idx + ']';
            return getXPath(el.parentNode) + xpath;
        }
        window.__clicks.push({
            xpath: getXPath(e.target),
            offsetX: e.offsetX,
            offsetY: e.offsetY,
            clientX: e.clientX,
            clientY: e.clientY,
            button: e.button
        });
    }, true);
""")

print("👉 Теперь кликайте по элементам. Логи будут появляться в консоли.")
print("🛑 Нажмите Ctrl+C для остановки.")

last_count = 0
try:
    while True:
        try:
            clicks = driver.execute_script("return window.__clicks;")
        except InvalidSessionIdException:
            print("❌ Браузер закрыт. Остановка.")
            break
        except WebDriverException as e:
            print(f"⚠️ Ошибка: {e}")
            time.sleep(1)
            continue
        if len(clicks) > last_count:
            for i in range(last_count, len(clicks)):
                c = clicks[i]
                print(f"🖱️ Клик #{i+1}: XPath = {c['xpath']}, координаты ({c['offsetX']}, {c['offsetY']}), кнопка {c['button']}")
            last_count = len(clicks)
        time.sleep(0.3)
except KeyboardInterrupt:
    print("\n👋 Остановлено.")
finally:
    driver.quit()
