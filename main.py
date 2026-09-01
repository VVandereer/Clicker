import webdriver
import argparse
import script
from clickMonitor import ClickMonitor


parser = argparse.ArgumentParser(prog="uv run main.py", description="Browser Clicker")
parser.add_argument("--debug", action="store_true", help="Enable debug output")
parser.add_argument("--nogui", action="store_true", help="Run webdriver in nogui mode")
args = parser.parse_args()


def main():
    print("Clicker is running!")
    driver = webdriver.Init(nogui=args.nogui)

    clickLogger = ClickMonitor(driver)
    if args.debug:
        clickLogger.start()
        print("Clicks on will be catched and print in console log")

    try:
        input("Press any key to start script..")
        script.wheel_button(driver)
    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        clickLogger.stop()
        driver.quit()
        print("\nCorrectly stopped")


if __name__ == "__main__":
    main()
    # <a class="vmmo-wheel-button" id="wheel-button" onclick="return wheelButton(this);"></a>
    # <span class="s9094f31c">Награда начислится через</span>
    # data-fullscreen-element-name="close-btn"
    # class="vmmo-prize-wrapper _show"
    # <a class="button-large _low" onclick="return showHintNew();">ПОЛУЧИТЬ</a>
    # <a class="button-large _low" onclick="$('#wheel-error-prize').removeClass('_show'); reload();">ОТЛОЖИТЬ</a>
