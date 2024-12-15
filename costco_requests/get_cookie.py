from selenium import webdriver

class get_new_cookie:

    def get_cookie(self):
        webdriver = self.webdriver_setup()
        webdriver.get("https://www.costco.ca/")
        all_cookies = webdriver.get_cookies()
        cookies_dict = {}
        cookie_string = ""
        for cookie in all_cookies:
            cookie_string += f"{cookie['name']}={cookie['value']}; "
        cookie_string = cookie_string.strip("; ")
        print(cookie_string)
        return cookie_string


    def webdriver_setup(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        driver = webdriver.Chrome(options=options)
        return driver
    



