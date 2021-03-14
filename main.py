from selenium.webdriver import Chrome

from web_page_interaction import solve_on_screen


def main():
    # TODO handle this better.  chrome driver auto installer?
    cd_path = "C:/Users/BenB/Documents/BenB/chromedriver_win32/chromedriver.exe"
    browser = Chrome(cd_path)
    browser.get("https://www.puzzle-nonograms.com/")

    for _ in range(5):  # solve 5 games then stop
        solve_on_screen(browser)


if __name__ == "__main__":
    main()
