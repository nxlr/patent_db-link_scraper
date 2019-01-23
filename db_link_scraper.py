from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy as np
import mechanicalsoup
import re
import time
import xlwt 
from xlwt import Workbook 

# returns all the wipo members as mentioned on the website
def wipo_members(): 
    url = "https://www.wipo.int/members/en/"

    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},  # Use the lxml HTML parser
        raise_on_404=True,
        user_agent=user_agent,
    )

    browser.open(url)
    page = browser.get_current_page()

    countries_list = page.find("div", {"class": "cols cols--three"}).find_all("li")
    countries = []
    
    for li in countries_list:
        countries.append(li.get_text())

    browser.close()
    return countries


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

# get the results 
def get_results(query, num_results, lang_code):
    assert isinstance(query, str), 'Search term must be a string'
    assert isinstance(num_results, int), 'Number of results must be an integer'
    escaped_query = query.replace(' ', '+')
    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_query, num_results, lang_code)
    response = requests.get(google_url, headers=headers)
    response.raise_for_status()
    return response.content

# get the relevant content from soup
def parse_results(results_html):
    soup = BeautifulSoup(results_html, 'html.parser')
    result_block = soup.find_all('div', attrs={'class': 'g'})
    for result in result_block:
        link = result.find('a', href=True)
        title = result.find('h3', attrs={'class': 'r'})
        if link and title:
            link_tmp = link['href'][7:]
            head, sep, tail = link_tmp.partition('&')
            link = head
            title = title.get_text()
            result_dict = {'link': link, 'title': title}
    return result_dict

# scrape for results on google
def scrape_google(query, num_results, lang_code):
    try:
        results_html = get_results(query, num_results, lang_code)
        result = parse_results(results_html)
        return result
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")

# main function
if __name__ == '__main__':
    start = time.time()


    # create random user_agent
    user_agent = get_random_ua()

    headers = {
        'user-agent': user_agent,
    }

    # list of countries on wipo website
    countries = wipo_members()

    # Excel Workbook is created 
    wb = Workbook() 

    # first sheet created
    sheet1 = wb.add_sheet('Sheet 1') 
    serial_number = 0

    for country in countries:
        query = country + ' patent database'

        # scrape top 1 results for the query
        result = scrape_google(query, 1, "en")

        link = result.get('link')
        title = result.get('title')

        #print(country, link, title)

        sheet1.write(serial_number, 0, serial_number+1)
        sheet1.write(serial_number, 1, country)
        sheet1.write(serial_number, 2, link)
        sheet1.write(serial_number, 3, title)
        
        serial_number += 1
        print(serial_number)
        
    wb.save('countries_patent-db_links.xls') 
    end = time.time()
    print(end - start)
    
    