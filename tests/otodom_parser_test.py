import pytest
from krakow.otodom_parser import OtodomParser
from datetime import datetime
from tests.test_utils import article_krakow as data
from bs4 import BeautifulSoup

class TestOtodomParser():
    def test_empty_address_string(self):
        with pytest.raises(Exception):
            OtodomParser(123)


    def test_read_page_details(self):
        file_name = "tests/single_page.html"

        with open(file_name, 'r', encoding='utf-8') as fp:
            test_page = fp.read()

        result = OtodomParser.get_all_details(test_page)

        expected = {
            'year' : '2002',
            'rent' : 700,
            'advert_id' : 60139104 ,
            'created_at' : '2020-01-22 14:00:51',
            'updated_at' : '2020-07-31 16:27:44',
            'address' : 'Kraków, Krowodrza, Oboźna',
        }

        for k, v in expected.items():
            assert v == result[k]


    def test_article_krakow_gets_the_right_data(self):
        now = datetime.now()
        offer = BeautifulSoup(data, 'html.parser').find_all('article')[0]

        result = OtodomParser.get_offer_details(offer, now)
        expected = {
            'title': '99 m²  0% prowizji! 4/5 - pokojowe, 4 balkony!',
            'area': 'Mieszkanie na sprzedaż: Kraków, Bronowice, Bronowice Małe',
            'price': 752500,
            'rooms': 4,
            'square_meters': 99.3,
            'price_per_m': 7601,
            'link': 'https://www.otodom.pl/oferta/0-prowizji-4-5-pokojowe-4-balkony-ID46MnG.html#ca42dde59f',
            "import_date": now.isoformat()
        }

        assert result == expected

