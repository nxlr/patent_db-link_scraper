from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy as np
import mechanicalsoup
import re


# get random user agent 
def get_random_ua():
    random_ua = ''
    ua_file = 'user-agents.txt'
    try:
        with open(ua_file) as f:
            lines = f.readlines()
        if len(lines) > 0:
            prng = np.random.RandomState()
            index = prng.permutation(len(lines) - 1)
            idx = np.asarray(index, dtype=np.integer)[0]
            random_ua = lines[int(idx)]
    except Exception as ex:
        print('Exception in random_ua')
        print(str(ex))
    finally:
        return random_ua.rstrip()

# create random user_agent
user_agent = get_random_ua()

url_google = "https://www.google.com/"

browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},  # Use the lxml HTML parser
        raise_on_404=True,
        user_agent=user_agent,
)

browser.open(url_google)

browser.select_form()

# test whether form is selected or not
browser.get_current_form().print_summary()
