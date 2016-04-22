import json
import random
import sys
from urllib.parse import urlparse, quote

import certifi
import download_settings as settings
import urllib3
from bs4 import BeautifulSoup
from urllib3.contrib.socks import SOCKSProxyManager

names_scheme = {"female": [], "male": [], "surname": []}

"""
USAGE:
1. Import in main.
2. Section of code for main
"""


def get_page(source):
    protocol = urlparse(source)[0] + "://"
    source = protocol + quote(source.replace(protocol, ""))

    if settings.USING_PROXY:
        http = SOCKSProxyManager(
            settings.proxy_type + "://" + settings.proxy_host + ":" + settings.proxy_port,
            cert_reqs="CERT_REQUIRED",  # Force certificate check
            ca_certs=certifi.where(),  # Path to the Certifi bundle
        )
    else:
        http = urllib3.PoolManager(
            cert_reqs="CERT_REQUIRED",  # Force certificate check
            ca_certs=certifi.where(),  # Path to the Certifi bundle
        )

    try:
        page = http.urlopen(
            "GET",
            source,
            preload_content=False,
            # timeout=urllib3.Timeout(connect=5.0, read=10.0),
            headers={'User-Agent': 'Mozilla'}
        )

    except urllib3.exceptions.MaxRetryError as error:
        print("Connection error:", error)
        sys.exit(1)

    else:
        return page


def extract_names(page, names, kind):
    soup = BeautifulSoup(page.read(), "html.parser")
    found = soup.html.body.findAll("tr")  # Names are in table rows
    for name in found:
        content = name.contents[-1].text
        if content != "Imię":
            names[kind].append(content)


def extract_surnames(page, names):
    soup = BeautifulSoup(page.read(), "html.parser")
    found = soup.html.body.findAll("strong")
    for surname in found:
        names["surname"].append(surname.text)


def get_surnames(names):
    for letter in settings.polish_letters:
        print("Getting surnames beginning with letter", letter + "...")
        link = settings.polish_source_surname + "/" + letter
        extract_surnames(get_page(link), names)


def get_names(names):
    print("Getting female names...")
    extract_names(get_page(settings.polish_source_female), names, "female")
    print("Getting male names...")
    extract_names(get_page(settings.polish_source_male), names, "male")
    get_surnames(names)

    names["female"].sort()
    names["male"].sort()


def save_json(names):
    f = open("data.json", "w+")
    f.write(json.dumps(names))
    f.close()


def load_json():
    f = open("data.json", "r")
    names = json.loads(f.read())
    f.close()
    return names


def main():
    names = names_scheme
    download_names.get_names(names)
    save_json(names)
    # names = load_json()
    print(len(names["female"]))
    print(len(names["male"]))
    print(len(names["surname"]))

if __name__ == '__main__':
    main()
