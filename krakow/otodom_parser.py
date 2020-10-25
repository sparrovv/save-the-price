import requests
from bs4 import BeautifulSoup
import json
import re

from datetime import datetime

class OtodomParser:
    def __init__(self, address_string, last_page_number=1, now=datetime.now()):
        if type(address_string) is not str:
            raise Exception("Address string can't be empty or not str type.")

        self.actual_page = 1
        self.last_page_number = last_page_number
        self.address_string = '{0}&page={1}'.format(address_string, "{}")
        self.import_tstamp = now
        self.result_list = []


    @staticmethod
    def str_to_int(input):
        # return int(filter(str.isdigit, input))
        res = re.findall(r'\d+', input)
        return(int("".join(res)))


    @staticmethod
    def str_to_number(input):
        res = re.sub('[^0-9,]', "", input).replace(",", ".")
        return(float("".join(res)))


    @staticmethod
    def get_all_details(page_content):
        offer = BeautifulSoup(page_content, 'html.parser')\
            .find(id = 'server-app-state')\
            .text

        dict = json.loads(offer)

        most_important_data = dict['initialProps']['meta']['target']
        year = most_important_data['Build_year']
        rent = most_important_data.get('Rent', None)
        extra_important_data = dict['initialProps']['data']['advert']
        advert_id = extra_important_data['advertId']
        created_at = extra_important_data['dateCreated']
        updated_at = extra_important_data['dateModified']
        location = extra_important_data['location']
        address = location['address']
        # remove noise
        del extra_important_data['photos']
        del extra_important_data['userAds']
        del extra_important_data['breadcrumb']

        return {
            'year': year,
            'rent': rent,
            'advert_id': advert_id,
            'created_at': created_at,
            'updated_at': updated_at,
            'address': address,
            'meta_target_data': most_important_data,
            'advert_data': extra_important_data
        }

    @staticmethod
    def get_offer_details(offer, tstamp):
        all_needed_atts = {
            "title": offer.find('header').find("h3").text.strip().replace("\n", " "),
            "area": offer.find('header').find("p").text.strip(),
            "price":  OtodomParser.str_to_int(offer.find("li", {"class" : "offer-item-price"}).text.strip()),
            "rooms":  OtodomParser.str_to_int(offer.find("li", {"class" : "offer-item-rooms"}).text.strip()),
            "square_meters":  OtodomParser.str_to_number(offer.find("li", {"class" : "offer-item-area"} ).text.strip()),
            "price_per_m": OtodomParser.str_to_int(offer.find("li", {"class" : "offer-item-price-per-m"} ).text.strip()),
            "link": offer.find('a').attrs['href'],
            "import_date": tstamp.isoformat()
        }

        return all_needed_atts


    def parse(self):
        r = requests.get(self.address_string.format(self.actual_page))

        while self.actual_page <= self.last_page_number:
            print("Parsing page {}".format(self.actual_page))
            soup = BeautifulSoup(r.content, 'html.parser')
            offers = soup.find_all('article')

            for offer in offers:
                self.result_list.append(self.get_offer_details(offer, self.import_tstamp))

            self.actual_page += 1
            r = requests.get(self.address_string.format(self.actual_page))


        return self.result_list
