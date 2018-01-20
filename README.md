# autorenueva-milanuncios
A short script to automatically renew ads on www.milanuncios.com

## Installation
You can download and put the script wherever you want. The script needs to be run with Python 3.

You will also need Selenium, which you can install via [pip](https://pip.pypa.io).

If using Firefox, you will need geckodriver in your PATH. You can get the latest release [here](https://github.com/mozilla/geckodriver/releases). Note that geckodriver might not work with old versions of Firefox, so if you're using an old version, update it or run it with [Firefox Nightly](https://nightly.mozilla.org).

If using Chrome, you will need chromedriver in your PATH, which you can get [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

## Usage

By default, the program will prompt you for your mail and password, and use a Firefox webdriver in headless mode.
You can use stored credentials from a file instead, by using the `-f` flag.

A complete list of options can be shown by running the script with `-h` or `--help` flags.

For example: `./main.py -f credentials.txt --chrome -w 10` runs the script with a Chrmome webdriver using the mail and
password from the file `credentials.txt` on the working directory, and waiting 10 seconds between ads.
