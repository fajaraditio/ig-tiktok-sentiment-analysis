from apify_client import ApifyClient
import pandas as pd
import os


def get_ig_comments(url):
    APIFY_TOKEN = 'apify_api_qDAntUROedXheACajglcVKG9OdEVj11O2BHC'

    # Initialize the ApifyClient with your API token
    client = ApifyClient(APIFY_TOKEN)

    # Prepare the Actor input
    run_input = {
        "directUrls": [url],
        "resultsLimit": 100,
    }

    # Run the Actor and wait for it to finish
    run = client.actor(
        "apify~instagram-comment-scraper").call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)

    exported_comments = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        exported_comment = [item['ownerUsername'],
                            item['text'].replace('\n', '')]
        exported_comments.append(exported_comment)

    if (not os.path.exists('uploads/instagram_src.csv')):
        csv_data = pd.DataFrame(exported_comments).to_csv(
            'uploads/instagram_src.csv', header=['username', 'comment'], index=False)
    else:
        csv_data = pd.DataFrame(exported_comments).to_csv(
            'uploads/instagram_src.csv', mode='a', index=False, header=False)


def get_tiktok_comments(url):
    APIFY_TOKEN = 'apify_api_qDAntUROedXheACajglcVKG9OdEVj11O2BHC'

    # Initialize the ApifyClient with your API token
    client = ApifyClient(APIFY_TOKEN)

    # Prepare the Actor input
    run_input = {
        "postURLs": [url],
        "commentsPerPost": 100,
        "maxRepliesPerComment": 0,
    }

    # Run the Actor and wait for it to finish
    run = client.actor(
        "clockworks~tiktok-comments-scraper").call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)

    exported_comments = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        exported_comment = [item['uniqueId'], item['text'].replace('\n', '')]
        exported_comments.append(exported_comment)

    if (not os.path.exists('uploads/tiktok_src.csv')):
        csv_data = pd.DataFrame(exported_comments).to_csv(
        'uploads/tiktok_src.csv', header=['username', 'comment'], index=False)
    else:
        csv_data = pd.DataFrame(exported_comments).to_csv(
            'uploads/tiktok_src.csv', mode='a', index=False, header=False)
