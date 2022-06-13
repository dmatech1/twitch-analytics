#!/usr/bin/env python3

import keyring
import logging
import requests
import urllib
import json
import os
import time
import urllib.parse
# from requests_oauthlib import OAuth2Session

logging.basicConfig(level=logging.INFO)

# See https://dev.twitch.tv/docs/authentication/scopes
scope = [
    # Banning and blocking misbehaving people.
    "moderator:manage:banned_users",        # Bots might need to ban people who spam the chat.
    "user:manage:blocked_users",            # Bots might also want to block people who get banned.
    "user:read:blocked_users",              # Paired with "user:manage:blocked_users" but perhaps not needed.

    # Chat-related permissions.
    "moderator:manage:automod",
    "moderator:manage:chat_settings",
    "moderator:read:chat_settings",
    "chat:edit",                            # Send messages in chat.
    "chat:read",                            # Read chat messages.
    "channel:moderate",                     # Delete chat messages (and other moderator things).

    # I don't currently use redemptions, but I'll request those permissions anyway.
    "channel:read:redemptions",
    "channel:manage:redemptions",

    # Miscellaneous permissions.
    "channel:read:subscriptions",
    "channel:manage:broadcast",
    "channel:manage:videos",
    "bits:read",
    "moderation:read"
]

# https://dev.twitch.tv/docs/authentication/refresh-tokens#how-to-use-a-refresh-token

# Must use the "OAuth Authorization Code Grant Flow": 
# https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/#authorization-code-grant-flow


# See "data/twitch-oauth2.json".

# A desktop app would need to a couple fallback ports in case one of them was taken.
redirect_urls = ["http://localhost:3000", "http://localhost:4000", "http://localhost:5000"]


# For the first iteration, I should code this entirely myself using only "requests" and the bare-bones HTTP server.
# I'll learn more that way.  It might require writing a custom "requests" wrapper like Google did.

# https://github.com/singlerider/twitch-python/blob/master/twitch.py
# https://pytwitcherapi.readthedocs.io/en/latest/_modules/pytwitcherapi/oauth.html
# https://requests-oauthlib.readthedocs.io/en/latest/

