from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy as np
import mechanicalsoup
import re

google = "https://www.google.com/"

browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},  # Use the lxml HTML parser
        raise_on_404=True,
        user_agent=user_agent,
)

browser.open(url)

browser.select_form()

# test whether form is selected or not
browser.get_current_form().print_summary()
