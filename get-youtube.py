#!/usr/bin/env python3

import logging
import requests
import urllib
import json
import os
import time
import urllib.parse
from google_auth_oauthlib.flow import InstalledAppFlow


# Adapted from https://stackoverflow.com/a/434314/7077511.
import itertools
def chunks(iterable,size):
    it = iter(iterable)
    chunk = list(itertools.islice(it,size))
    while chunk:
        yield chunk
        chunk = list(itertools.islice(it,size))


logging.basicConfig(level=logging.INFO)

flow = InstalledAppFlow.from_client_secrets_file(
    'data/client_secret_1068468657673-o0k8mk233pvem24jmfdq9uqj5gpf2v9r.apps.googleusercontent.com.json',
    scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])

flow.run_local_server()
sess = flow.authorized_session()


video_items = []

PAGE_TOKEN=""
page_num = 1
while True:
    r = sess.get(
        f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&forMine=true&maxResults=50&order=date&safeSearch=none&type=video&pageToken={urllib.parse.quote_plus(PAGE_TOKEN)}")

    # Write it out for later use.
    with open(f"twitch-analytics/youtube/videos-{page_num}.json", "w") as f:
        f.write(r.text)

    # Process it.
    obj = r.json()
    print(r.json())

    video_items.extend(obj["items"])

    if not "nextPageToken" in obj:
        break

    PAGE_TOKEN = obj["nextPageToken"]

    page_num += 1
    time.sleep(0.5)


# Now, get details.
video_ids = [obj["id"]["videoId"] for obj in video_items]


for c in chunks(video_ids, 10):
    print(",".join(c))

    r = sess.get(
        f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics%2CtopicDetails%2CfileDetails%2Cstatus&id={urllib.parse.quote_plus(','.join(c))}")

    # Write it out for later use.
    with open(f"twitch-analytics/youtube/details-{page_num}.json", "w") as f:
        f.write(r.text)

    page_num += 1
    time.sleep(0.5)
