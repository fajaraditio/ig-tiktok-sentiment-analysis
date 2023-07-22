import requests
import json
import pandas as pd
import sys
import time
from tqdm import tqdm

def get_comments(url):
    SHORTCODE = url.rsplit('/', 1)[-1]
    QUERY_HASH = "b3055c01b4b222b8a47dc12b090e4e64"
    WAIT = 3
    CRAWL_SIZE = 50

    cursor = ''
    has_next_page = True
    comments = []

    variables = {"shortcode": SHORTCODE, "fetch_comment_count": CRAWL_SIZE,
                "parent_comment_count": CRAWL_SIZE, "after": cursor}

    query = 'https://www.instagram.com/graphql/query/?query_hash=' + \
        QUERY_HASH+'&variables='+json.dumps(variables)

    while True:
        variables = {"shortcode": SHORTCODE, "fetch_comment_count": CRAWL_SIZE,
                    "parent_comment_count": CRAWL_SIZE, "after": cursor}
        query = 'https://www.instagram.com/graphql/query/?query_hash=' + \
            QUERY_HASH+'&variables='+json.dumps(variables)

        # req
        res = requests.get(query).json()

        # update page info
        page_info = res['data']['shortcode_media']['edge_media_to_comment']['page_info']
        tot = res['data']['shortcode_media']['edge_media_to_comment']['count']
        cursor = page_info['end_cursor']
        has_next_page = page_info['has_next_page']

        # iterate edge
        for edge in tqdm(res['data']['shortcode_media']['edge_media_to_comment']['edges']):
            comments.append(
                (edge['node']['owner']['username'], edge['node']['text']))

        print('total crawled : ', str(len(comments)),
            '  remain:', str(tot-len(comments)))

        if has_next_page == False:
            break

        # prevent DDoS
        time.sleep(WAIT)

    exported_comments = []
    for comment in comments:
        exported_comment = [comment[0], comment[1].replace('\n', '')]
        exported_comments.append(exported_comment)

    csv_data = pd.DataFrame(exported_comments).to_csv('uploads/instagram.csv', header=['username', 'comment'], index=False)
