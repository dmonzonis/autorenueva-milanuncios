#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from getpass import getpass
import argparse

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


def renew_ads(driver, sleep_time=.5, quiet=False):
    """With the driver on the first ad page, renews all ads on all pages.

    A sleep time can be supplied to wait between page switching and not raise any suspicion.
    """
    page = 1
    while True:
        # Get tags containing ad IDs
        id_list = driver.find_elements_by_class_name("x5")

        # If there are no ads in the page, we are done
        if not id_list:
            if not quiet:
                print("No more ads found. Finishing...")
            return

        # Renew all ads in the current page
        if not quiet:
            print("{0} ads found in page {1}. Renewing...".format(
                len(id_list),
                page
            ))
        renew_ads_in_page(driver, id_list, sleep_time=sleep_time)

        # Go to the next page
        if not quiet:
            print("Done. Going to next page.")
        page += 1
        driver.get(BASE_URL + "?pagina=" + str(page))
        sleep(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=argparse.FileType('r'), help="read credentials from file")
    parser.add_argument('--head', '-H', action='store_true', help="don't run in headless mode")
    parser.add_argument('--chrome', '-c', action='store_true', help="use Chrome webdriver")
    parser.add_argument('--quiet', '-q', action='store_true', help="run in quiet mode")
    parser.add_argument('--wait', '-w', type=float, default=.5,
                        help="seconds to wait between ads", metavar="t")

    args = parser.parse_args()

    # Get user credentials
    if args.f:
        try:
            mail, password = [line.strip() for line in args.f if line.strip()]
        except ValueError:
            print("Error: Credentials file must have mail and password each on a separate line!")
            return
    else:
        mail, password = get_credentials()

    # Start a Firefox or Chrome driver
    if args.chrome:
        options = webdriver.ChromeOptions()
        options.set_headless(not args.head)
        driver = webdriver.Chrome(chrome_options=options)
    else:
        options = webdriver.FirefoxOptions()
        options.set_headless(not args.head)
        driver = webdriver.Firefox(firefox_options=options)

    if args.wait > 0:
        sleep_time = args.wait
    else:
        if not args.quiet:
            print("Wait time has to be positive! Using the default 1 second.")
        sleep_time = 1

    # Start headless driver and access user page
    driver.get(BASE_URL)

    # Set implicit wait in case elements are not readily available
    driver.implicitly_wait(5)

    login(driver, mail, password)
    renew_ads(driver, sleep_time=sleep_time, quiet=args.quiet)

    driver.quit()


if __name__ == "__main__":
    main()
