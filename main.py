import os
import json
from datetime import datetime
import logging
import argparse
from typing import List, Dict, Any

import serpapi


logging.basicConfig(level=logging.INFO)
allowed_engines = ['apple_app_store', 'google_play']
allowed_devices = ['mobile', 'desktop', 'tablet']


class AppInfoRetriever:

    def __init__(self, serpapi_key: str):
        self.serpapi_key = serpapi_key or os.environ['SERP_API_KEY']
        self.client = serpapi.Client(api_key=self.serpapi_key)
        self.logger = logging.getLogger('app_info_retriever')
        print(f'Using SerpApi key {self.serpapi_key}')

    def setup_params(self, query: str, engine: str, device: str, country: str, language: str,
                     disallow_explicit: bool = False, num: int = 20, start_page: int = 0) -> Dict[str, Any]:
        """
        Returns a prepared parameters dict for the `serpapi.Client().search()` method
        :param query:               Search query
        :param engine:              Engine to be searched
        :param device:              Device type
        :param country:             Country
        :param language:            App languages
        :param disallow_explicit:   Whether or not to include explicit content in search results
        :param num:                 Number of results per page (max. 20)
        :param start_page:          Index of start page
        :return:                    Params dict for serpapi client
        """
        return {
            'api_key': self.serpapi_key,
            'engine': engine,
            'device': device,
            'country': country,
            'lang': language,
            'disallow_explicit': disallow_explicit,
            'num': num,
            'page': start_page,
            'q': query,    # Used for Google Play Store
            'term': query  # Used for Apple App Store
        }

    def save_results(self, results: List[Any], output_fp: str):
        """
        Saves search results to a JSON file
        :param results:             Search results
        :param output_fp:           Output file path
        :return:
        """
        with open(output_fp, 'w') as f:
            f.write(json.dumps(results, indent=4, ensure_ascii=False))

    def run(self, queries: List[str],
                 engines: List[str] = allowed_engines,
                 countries: List[str] = ['de'],
                 languages: List[str] = ['de-de'],
                 disallow_explicit: bool = False,
                 start_page: int = 0,
                 max_pages: int = 50,
                 device: str = allowed_devices[0]):
        """
        Runs the retrieval process by sending search queries to SerpApi
        :param queries:             List of search queries
        :param engines:             List of engines to be searched
        :param countries:           List of countries to be searched
        :param languages:           List of languages to be searched
        :param disallow_explicit:   Whether or not to include explicit content in search results
        :param start_page:          Index of start page
        :param max_pages:           Max. number of pages to be retrieved
        :param device:              Device type
        """
        # Iterate over queries, engines, countries and languages
        for q in queries:
            for e in engines:
                for c in countries:
                    for l in languages:
                        print(f'Retrieving results for query={q}, engine={e}, country={c}, language={l}')
                        params = self.setup_params(query=q,
                                                   device=device,
                                                   engine=e,
                                                   country=c,
                                                   language=l,
                                                   start_page=start_page,
                                                   disallow_explicit=disallow_explicit)
                        results = []
                        page_idx = 1

                        # Iterate over pages until `max_pages`
                        while page_idx <= max_pages:
                            page_idx += 1
                            print(f'Scraping page {params["page"]}...')
                            search = self.client.search(params)
                            new_page_results = search.as_dict()     # JSON -> Python dict
                            results.extend(new_page_results['organic_results'])

                            if 'next' in new_page_results.get('serpapi_pagination', {}):
                                params['page'] += 1
                            else:
                                break
                        print(f'Saving results...')
                        print('------------------')
                        output_fp = os.path.join('data', f'{e}.{q}.{datetime.now()}.json')
                        self.save_results(results, output_fp)
        print('Done.')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--queries', '-q',
                            nargs='+',
                            default=[],
                            help='List of search queries')
    arg_parser.add_argument('--engines', '-e',
                            nargs='+',
                            default=allowed_engines,
                            choices=allowed_engines,
                            help='List of engines to query')
    arg_parser.add_argument('--countries', '-c',
                            nargs='+',
                            default=['de'],
                            help='List of countries to query')
    arg_parser.add_argument('--languages', '-l',
                            nargs='+',
                            default=['de-de'],
                            help='List of languages to query')
    arg_parser.add_argument('--disallow-explicit',
                            action='store_true',
                            help='List of countries to query')
    arg_parser.add_argument('--start-page',
                            type=int,
                            default=0,
                            help='index of start page')
    arg_parser.add_argument('--max_pages', '-m',
                            type=int,
                            default=10,
                            help='Max. number of pages to search for apps. Important as stopping criterion for Google '
                                 'Play Store due to infinity scroll')
    arg_parser.add_argument('--device', '-d',
                            type=str,
                            default='mobile',
                            choices=allowed_devices,
                            help='Device type')
    arg_parser.add_argument('--serpapikey', '-k',
                            type=str,
                            help='SerpApi key')

    args = arg_parser.parse_args()
    retriever = AppInfoRetriever(serpapi_key=args.serpapikey)
    retriever.run(queries=args.queries,
                  engines=args.engines,
                  countries=args.countries,
                  languages=args.languages,
                  disallow_explicit=args.disallow_explicit,
                  start_page=args.start_page,
                  max_pages=args.max_pages,
                  device=args.device
                  )
