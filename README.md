# autorenueva-milanuncios
A short script to automatically renew ads on www.milanuncios.com

## Usage

By default, the program will prompt you for your mail and password, and use a Firefox webdriver in headless mode.
You can use stored credentials from a file instead, by using the `-f` flag.

A complete list of options can be shown by running the script with `-h` or `--help` flags.

For example: `./main.py -f credentials.txt --chrome` runs the script with a Chrmome webdriver using the mail and
password from the file `credentials.txt` on the working directory.
