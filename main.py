# importing required package of webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.opera.options import Options
from selenium.webdriver.support.wait import WebDriverWait

if __name__ == '__main__':
    browser = webdriver.Edge(r"C:\warhouse\edgedriver\msedgedriver.exe")
    # browser.maximize_window()
    browser.get('https://www.youtube.com/watch?v=75S8fU9Dkxw')
    try:
        # Get the text box to insert Email using selector ID
        page = WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located("text"))
        print(page)
        sleep(10)
    except TimeoutException:
        print("No element found")
    sleep(10)
    browser.close()
