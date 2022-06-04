#!/usr/bin/env python3

import logging
import requests
import urllib
import json
import os
import time
import urllib.parse
from google_auth_oauthlib.flow import InstalledAppFlow

TO_DO = [
  {
    "current_title": "[035] Subnautica: Below Zero -- Back to 4546B and collecting some eggs!",
    "youtube_id": "fkbSK72TX_Q",
    "original_url": "https://www.twitch.tv/videos/1218669183",
    "title": "[035] Subnautica: Below Zero -- Back to 4546B and collecting some eggs!",
    "duration": "3h45m2s",
    "created_at": "2021-11-28T21:08:25Z"
  },
  {
    "current_title": "[036] Subnautica: Below Zero -- Back to 4546B and collecting some eggs!",
    "youtube_id": "Keag2W0MyAA",
    "original_url": "https://www.twitch.tv/videos/1225244694",
    "title": "[036] Subnautica: Below Zero -- Back to 4546B and collecting some eggs!",
    "duration": "1h37m24s",
    "created_at": "2021-12-05T21:12:09Z"
  }
]
logging.basicConfig(level=logging.INFO)

flow = InstalledAppFlow.from_client_secrets_file(
    'data/client_secret_1068468657673-o0k8mk233pvem24jmfdq9uqj5gpf2v9r.apps.googleusercontent.com.json',
    scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])

flow.run_local_server()
sess = flow.authorized_session()

for v in TO_DO:
    print(v)

    r = sess.put(
        f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2Cstatus%2CrecordingDetails",
        json={
            "id": v["youtube_id"],
            "snippet": {
                "title": v["title"],
                "description": f"Original URL: {v['original_url']}\nOriginal Title: {v['title']}\nOriginal Date: {v['created_at']}\nOriginal Duration: {v['duration']}",
                "categoryId": "20"
            },
            "status": {
                "privacyStatus": "public"
            },
            "recordingDetails": {
                "recordingDate": v['created_at'][0:10]
            }
        })

    print(r.status_code)
    print(r.text)
    time.sleep(1)
