#!/usr/bin/env python3

import logging
import requests
import urllib
import json
import os
import time
import urllib.parse
from requests_oauthlib import OAuth2Session

logging.basicConfig(level=logging.INFO)

# See https://dev.twitch.tv/docs/authentication/scopes
scope = [
    # Banning and blocking misbehaving people.
    "moderator:manage:banned_users",        # Bots might need to ban people who spam the chat.
    "user:manage:blocked_users",            # Bots might also want to block people who get banned.
    "user:read:blocked_users",              # Paired with "user:manage:blocked_users" but perhaps not needed.


    "channel:manage:broadcast",
    "channel:manage:videos",
    "moderator:manage:chat_settings",
    "moderator:read:chat_settings",
    "channel:read:redemptions",
    "channel:manage:redemptions",
    "channel:read:subscriptions",
    "moderator:manage:automod",
    "channel:moderate",
    "chat:edit",                            # Send messages in chat.
    "chat:read",                            # Read chat messages.
    "bits:read",
    "moderation:read"
]

# https://dev.twitch.tv/docs/authentication/refresh-tokens#how-to-use-a-refresh-token

# Must use the "OAuth Authorization Code Grant Flow": 
# https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/#authorization-code-grant-flow


# See "data/twitch-oauth2.json".
redirect_url = "http://localhost:3000"

# For the first iteration, I should code this entirely myself using only "requests" and the bare-bones HTTP server.
# I'll learn more that way.  It might require writing a custom "requests" wrapper like Google did.


# https://github.com/singlerider/twitch-python/blob/master/twitch.py
# https://pytwitcherapi.readthedocs.io/en/latest/_modules/pytwitcherapi/oauth.html
# https://requests-oauthlib.readthedocs.io/en/latest/
