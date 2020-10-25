from functional import seq
from requests_futures.sessions import FuturesSession
from krakow.otodom_parser import OtodomParser


class AsyncFetcher:

    def __init__(self, urls):
        self.urls = seq(urls)

    def get_result(self, result):
        return {
            'url': result.url,
            'status': result.status_code,
            'body': result.content
        }

    def convert_to_expected_struct(self, result):
        return OtodomParser.get_all_details(result['body'])

    def fetch_all(self):
        session = FuturesSession()
        # batch by 10
        grouped_by = self.urls.grouped(10)
        # grouped_by.for_each()
        results = []
        for group in grouped_by:
            print(f"Fetching results for the group ${len(group)}")
            futures = seq(group).map(lambda url: session.get(url))
            seq(futures) \
                .for_each(lambda f: results.append(f.result()))

        return seq(results) \
            .map(lambda r: self.get_result(r)) \
            .filter(lambda result: result['status'] == 200) \
            .map(lambda result: (result['url'], self.convert_to_expected_struct(result)))
