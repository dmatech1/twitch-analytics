
-- https://stackoverflow.com/questions/20289410/difference-between-int-primary-key-and-integer-primary-key-sqlite

-- Main table describing each stream as a work.
CREATE TABLE Videos (
    video_id            INTEGER PRIMARY KEY,    -- Unique ID for Twitch VOD.  Negative numbers mean I don't know.
    stream_id           INTEGER,
    stream_status       INTEGER,                -- 0 = Starting up, 1 = In progress, 2 = Complete.

    game_id             INTEGER,                -- Most recent video game ID.
    title               TEXT,                   -- Most recent video title text.
    video_description   TEXT,
    discord_id          INTEGER,                -- Pointer to Discord message that is edited throughout the lifecycle of the video.

    video_snapshot_id   INTEGER,                -- Pointer to the most recent useful record in VideoSnapshots.
    stream_snapshot_id  INTEGER,                -- Pointer to the most recent useful record in StreamSnapshots.

    -- Tracking data that might need to be manually populated later.  Note that I'm required
    -- to wait 24 hours before making the VOD available on YouTube anyway.
    obs_log_path        TEXT,                   -- Path to the OBS log file for this stream.
    mkv_path            TEXT,                   -- Path to the MKV file created by OBS.
    mp4_path            TEXT,                   -- Path to the MP4 file downloaded from Twitch.
    youtube_vod_url     TEXT,                   -- Link to VOD copy on YouTube.

    series_id           INTEGER,                -- Link to a series (playlist on YouTube or collection on Twitch).
    series_ordinal      INTEGER                 -- Which part number of the series it is.
);

CREATE TABLE Series (
    series_id           INTEGER PRIMARY KEY,    -- Unique ID for series.  This is generated purely by this app.
    series_name         TEXT,
    series_status       TEXT,
    series_description  TEXT,
    youtube_playlist    TEXT,
    twitch_collection   TEXT
);

CREATE TABLE DiscordMessages (
    id                  INTEGER PRIMARY KEY,    -- Unique ID for this table.  This is generated purely by this app.
    time_stamp          REAL,                   -- Unix timestamp in floating point format.
    discord_id          INTEGER,                -- Pointer to Discord message that is edited throughout the lifecycle of the video.
    request_method      TEXT,                   -- Request method (POST or PATCH).
    request_url         TEXT,                   -- Full URL.
    message_text        TEXT,                   -- JSON blob submitted to Discord.
    webhook_response    TEXT                    -- JSON blob returned from the PATCH or POST request.
);

-- A valid snapshot of the "Get Videos" response.  The most useful response is right after the stream ends.
-- Of course, I can continue to take snapshots for as long as the video is still up, and that can be useful
-- if I wish to see updates to the "view_count" and "title" attributes.
CREATE TABLE VideoSnapshots (
    snapshot_id         INTEGER PRIMARY KEY,    -- Used for links.
    video_id            INTEGER,                -- "id" value from API response.
    stream_id           INTEGER,                -- "stream_id" value from API response.
    time_stamp          REAL,                   -- Unix timestamp in floating point format.
    json_format         TEXT,                   -- Source of the JSON data.  Some earlier streams might be from "TCD".
    json_data           TEXT                    -- The entire API response.
);

-- A "Get Stream" response.  These are only available while the stream is running, and it doesn't seem to
-- update that frequently.  In fact, it might take almost a minute for a stream to even show up here,
-- although it will show up in "Get Videos" (complete with the stream ID) much sooner.
CREATE TABLE StreamSnapshots (
    snapshot_id         INTEGER PRIMARY KEY,    -- Used for links.
    stream_id           INTEGER,                -- "id" value from API response.
    game_id             INTEGER,                -- "game_id" value from API response.
    time_stamp          REAL,                   -- Unix timestamp in floating point format.
    json_format         TEXT,                   -- Source of the JSON data.  There might be different API versions over time.
    json_data           TEXT                    -- The entire API response.
);

-- Game detail keyed off of Twitch's ID.  This additional info is used for providing convenience
-- links in the Discord notifications.  I'll try to populate this for everything I own.
CREATE TABLE Games (
    game_id             INTEGER PRIMARY KEY,    -- Twitch ID for game that I would select.
    game_name           TEXT,                   -- Twitch game name text associated with "game_id".
    twitch_box_art_url  TEXT,    
    twitch_game_url     TEXT,                   -- Link to Twitch game directory page.
    youtube_game_url    TEXT,                   -- Link to YouTube game channel (if available).

    -- The following are best-effort.  The products for sale might not be exactly the same
    -- as what I have (as bundles might be slightly different).
    game_source         TEXT,                   -- Where I got the game (usually Steam).
    igdb_id             INTEGER,                -- Numeric IGDB ID.
    igdb_url            TEXT,                   -- Link to IGDB page.
    igdb_box_art_url    TEXT,
    steam_app_id        INTEGER,                -- Steam app ID.
    steam_url           TEXT,                   -- Link to Steam page.
    gog_url             TEXT,                   -- 
    epic_url            TEXT                    -- 
);

/*
while sleep 2
do
    echo "======================================"
    twitch api get streams -P -q user_id=217476645
    twitch api get videos -P -q user_id=217476645
done 2>&1 | tee twitch-test.txt
*/

