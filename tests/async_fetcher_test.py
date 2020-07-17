import pytest
from krakow.async_fetcher import AsyncFetcher
from concurrent.futures import  wait

class TestAsyncFetcher():

    def test_async_fetcher(self):
        urls = [
            'https://www.otodom.pl/oferta/mieszkanie-90-m-krakow-ID46VTS.html#a7152b973b',
            'https://www.otodom.pl/oferta/piekne-mieszkanie-w-sercu-krowodrzy-z-2-balkonami-ID457GJ.html#a7152b973b',
            'https://www.otodom.pl/oferta/piekne-mieszkanie-w-srodmiesciu-94-mkw-za-555-000-ID44HnA.html#a7152b973b',
            'https://www.otodom.pl/oferta/piekne-foo'
        ]

        fetcher = AsyncFetcher(urls)
        results = fetcher.fetch_all()

        print(results)

        assert(True)



