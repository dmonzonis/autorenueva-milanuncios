#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from getpass import getpass

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Global constants
BASE_URL = "http://www.milanuncios.com/mis-anuncios/"


def get_credentials():
    """Return credentials entered by the user on standard input."""
    mail = input("Mail: ")
    password = getpass()

    return mail, password


def login(driver, mail, password):
    """Log in using the mail and password provided as arguments."""
    id_box = driver.find_element_by_id('email')
    id_box.clear()
    id_box.send_keys(mail)
    pwd_box = driver.find_element_by_id('contra')
    pwd_box.clear()
    pwd_box.send_keys(password)
    pwd_box.send_keys(Keys.RETURN)


def renew_ads_in_page(driver, id_list, sleep_time=.5):
    """Renew ads from a list containing the full ad IDs.

    Iteratively renews all ads from the list, following human-like behavior.
    A sleep time can be supplied to not raise any suspicion.
    """
    for id in id_list:
        # Get the javascript command for opening the pop-up using only the ID numbers
        open_popup = "ventana('renovar/?id=','{0}')".format(id.text[1:])
        driver.execute_script(open_popup)

        # Switch to pop-up and click renew link
        driver.switch_to_frame("ifrw")
        clickable = driver.find_element_by_id("lren")
        clickable.click()

        # Check for any alerts, in case the ad couldn't be renewed
        # In case there's an alert, close it and the pop-up
        try:
            alert = WebDriverWait(driver, 1).until(
                EC.alert_is_present()
            )
            alert.accept()
        except Exception:
            pass

        # Switch back to parent frame
        driver.switch_to_default_content()
        sleep(sleep_time)


def renew_ads(driver, sleep_time=1):
    """With the driver on the first ad page, renews all ads on all pages.

    A sleep time can be supplied to wait between page switching and not raise any suspicion.
    """
    page = 1
    while True:
        # Get tags containing ad IDs
        id_list = driver.find_elements_by_class_name("x5")

        # If there are no ads in the page, we are done
        if not id_list:
            return

        # Renew all ads in the current page
        renew_ads_in_page(driver, id_list)

        # Go to the next page
        page += 1
        driver.get(BASE_URL + "?pagina=" + str(page))
        sleep(sleep_time)


def main():
    # Get user credentials
    mail, password = get_credentials()

    # Start headless driver and access user page
    options = webdriver.FirefoxOptions()
    options.set_headless(True)
    driver = webdriver.Firefox(firefox_options=options)
    driver.get(BASE_URL)

    # Set implicit wait in case elements are not readily available
    driver.implicitly_wait(5)

    login(driver, mail, password)
    renew_ads(driver)

    driver.quit()


if __name__ == "__main__":
    main()
