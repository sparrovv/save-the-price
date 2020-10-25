# -*- coding: utf-8 -*-
from optparse import OptionParser
import logging
import sys

from krakow.async_fetcher import AsyncFetcher
from krakow.otodom_parser import OtodomParser
from krakow.gsheet_uploader import GSheetsAppender
from functional import seq

from datetime import datetime

import os
import base64
import json
from google.cloud import storage
from google.oauth2 import service_account


def upload_blob(source_file_name, destination_blob_name, credentials):
    """Uploads a file to the bucket."""
    project_name = os.getenv('GCS_PROJECT')
    bucket_name = os.getenv('GCS_BUCKET')

    storage_client = storage.Client(credentials=credentials, project=project_name)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


def save_in_sheets(seqOfData, sheet_id, credentials):
    keys = [
        "title", "area", "price", "rooms", "square_meters", "price_per_m", "link", "created_at", "updated_at",
        "import_date", "advert_id", "rent", "year", "address"
    ]

    rows = seqOfData \
        .map(lambda x: [x.get(k) for k in keys]) \
        .to_list()

    appender = GSheetsAppender(sheet_id, "Sheet1!A2:D2", credentials)
    appender.append(rows)


def get_credentials():
    kb64 = os.getenv('GCS_SA_KEY')
    key_content = base64.b64decode(kb64)

    google_key = json.loads(key_content)
    return service_account.Credentials.from_service_account_info(google_key)


def collect_details(results):
    urls = seq(results) \
        .map(lambda r: r['link'])

    fetcher = AsyncFetcher(urls)
    data = fetcher.fetch_all()
    return data


def merge_with_details(record, details):
    matching_record = details \
        .find(lambda x: x[0] == record['link'])

    if (matching_record != None):
        return {**record, **matching_record[1]}
    else:
        return record


def main():
    logger = logging.getLogger('myapp')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    parser = OptionParser()

    parser.add_option("-u", "--upload", dest="upload", help="upload to google storage", default=False, action="store_true")
    parser.add_option("-p", "--upload-path", dest="upload_path", help="upload path to google storage")

    parser.add_option("-g", "--sheet-id", dest="sheet_id", help="google sheet id")

    parser.add_option("-n", "--number-of-pages", dest="number_of_pages", help="how many pages should be traversed")
    parser.add_option("-f", "--file-name-prefix", dest="file_name_prefix", help="the file name prefix")

    (options, args) = parser.parse_args()

    otodom_url = args[0]
    number_of_pages = int(options.number_of_pages) if options.number_of_pages is not None else 6

    date_time_obj = datetime.now()
    time_str = date_time_obj.isoformat()

    file_name_prefix = options.file_name_prefix if options.file_name_prefix is not None else "search_result"
    file_name = f"{file_name_prefix}_{time_str}.json"
    file_path = f"files/{file_name}"

    otodom_parser = OtodomParser(otodom_url, number_of_pages, date_time_obj)
    parsed_results = otodom_parser.parse()

    logger.info(f"Collecting details for ${len(parsed_results)}")
    details = collect_details(parsed_results)

    logger.info(f"Merging with details")
    enriched_data = seq(parsed_results) \
        .map(lambda x: merge_with_details(x, details))

    # def con(dict):
    #     logger.info(f"Converting ")
    #     return json.dumps(dict)
    #

    logger.info(f"Saving to JSON file")
    # enriched_data.map(lambda x: con(x))\
    #     .to_file(file_path)
    enriched_data.to_jsonl(f"{file_path}")

    if options.upload:
        credentials = get_credentials()
        upload_blob(file_path, f"{options.upload_path}/{file_name}", credentials)

    if options.sheet_id is not None:
        credentials = get_credentials()
        save_in_sheets(enriched_data, options.sheet_id, credentials)

    logger.info(f"Done")


if __name__ == '__main__':
    main()
