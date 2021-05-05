#!/usr/bin/env python3
import scrapy
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import json
import re


# import logging
# import http.client as http_client

# http_client.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


class Search:
    def __init__(self, url):
        self.url = url


class Contact(scrapy.Item):
    cell_phone = scrapy.Field()
    home_phone = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip = scrapy.Field()
    member_id = scrapy.Field()


    #cell_phone,home_phone,category,sub_category = scrapy.Field()


def main():
    base_url = 'https://classifieds.ksl.com/search/perPage/96'
    searches = ['/Cycling/Bike-Racks']

    for search in searches:
        ua = UserAgent()
        random_ua = ua.random
        print(f'Using random user-agent: {random_ua}')
        headers = {
            'user-agent': random_ua  # to help us not get blocked
        }

        url = base_url + search
        r = requests.get(url, headers=headers)
        print(r.status_code)

        soup = BeautifulSoup(r.content, 'html.parser')
        scripts = soup.find_all(attrs={"type": "text/javascript", "src": None})

        for script in scripts:
            # print(script.string)
            if "window.renderSearchSection" in script.string:
                m = re.search('listings: (.*),\n', script.string)
                print(m.group(1))
                listings = json.loads(m.group(1))
                print(len(listings))
                for listing in listings:
                    print(listing.get("id"))


if __name__ == "__main__":
    main()
