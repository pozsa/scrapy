'''
https://www.healthgrades.com/

https://curl.trillworks.com/
'''

import math
import os
import random
import time

import requests

import core

FULL_DIR = 'json/full_json/'
RESULTS_DIR = 'json/results_json/'
PROVIDERS_DIR = 'json/providers_json/'
page_num = 1
max_page = 1
padding = 0
filename = '1.json'

headers = {
    'pragma': 'no-cache',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'accept': '*/*',
    'cache-control': 'no-cache',
}

params = (
    ('distances', 'National'),
    ('what', 'Invisalign\xAE'),
    ('searchType', 'Procedure'),
    ('zip', '10025'),
    ('category', 'provider'),
    ('pageNum', f'{page_num}'),
)

response = requests.get(
    'https://www.healthgrades.com/api3/usearch',
    headers=headers,
    params=params)

#TODO check response status
#response.status_code

try:
    content = response.json()
except Exception as e:
    err_msg = f'{e.args}\n\n{response.text}'
    core.notify(err_msg)
    exit(err_msg)

try:
    total_count = content['search']['searchResults']['totalCount']
    page_size = content['search']['searchResults']['provider']['pageSize']
    max_page = math.ceil(total_count / page_size)
    padding = len(str(max_page))
    filename = f'{page_num:0{padding}d}.json'

    search_results = content['search']['searchResults']
    providers = content['search']['searchResults']['provider']['results']
except Exception as e:
    #TODO logging
    core.notify(e.args)
    exit(e.args)

core.save_json_to_file(FULL_DIR, filename, content)
core.save_json_to_file(RESULTS_DIR, filename, search_results)
core.save_json_to_file(PROVIDERS_DIR, filename, providers)

for page_num in range(2, max_page + 1):
    crawl_delay = random.randint(30, 60)
    time.sleep(crawl_delay)

    filename = f'{page_num:0{padding}d}.json'

    params = (
        ('distances', 'National'),
        ('what', 'Invisalign\xAE'),
        ('searchType', 'Procedure'),
        ('zip', '10025'),
        ('category', 'provider'),
        ('pageNum', f'{page_num}'),
    )

    response = requests.get(
        'https://www.healthgrades.com/api3/usearch',
        headers=headers,
        params=params)

    content = response.json()

    try:
        search_results = content['search']['searchResults']
        providers = content['search']['searchResults']['provider']['results']
    except Exception as e:
        #TODO logging
        core.notify(e.args)
        exit(e.args)

    core.save_json_to_file(FULL_DIR, filename, content)
    core.save_json_to_file(RESULTS_DIR, filename, search_results)
    if providers:
        core.save_json_to_file(PROVIDERS_DIR, filename, providers)
    else:
        err_msg = f'No providers found! Page: {page_num}'
        core.notify(err_msg)
        exit(err_msg)

    if page_num == max_page:
        core.notify('Job done!')
