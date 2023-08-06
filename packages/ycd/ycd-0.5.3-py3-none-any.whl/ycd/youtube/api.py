import httpx
from .. settings import Settings

# with open('apik.dat') as f:
#     API_KEY = f.readline()


YOUTUBE_URI = 'https://www.googleapis.com/youtube/v3/playlistItems'


def get_video_items(channel_id: str):
    client = httpx.Client()
    PLAYLIST_ID = ''.join(('UU', channel_id[2:]))
    API_KEY = Settings().config['api_key']
    PARAMS = {'key': API_KEY, 'part': 'snippet',
              'playlistId': PLAYLIST_ID, 'maxResults': 50}

    while True:
        try:
            resp = client.get(YOUTUBE_URI, params=PARAMS)
            resp.raise_for_status()
            content = resp.json()
        except httpx.HTTPStatusError as e:
            print(
                str(e) + "This is because of the network environment, not this programm.")
            break
        items = content.get('items')
        nextPageToken = content.get('nextPageToken')
        if items:
            yield items
            # continue
        if nextPageToken:
            PARAMS.update({'pageToken': nextPageToken})
        else:
            return


def check_validation(key: str):
    client = httpx.Client()
    PLAYLIST_ID = 'UUBR8-60-B28hp2BmDPdntcQ'
    API_KEY = key
    PARAMS = {'key': API_KEY, 'part': 'snippet',
              'playlistId': PLAYLIST_ID, 'maxResults': 50}
    try:
        resp = client.get(YOUTUBE_URI, params=PARAMS)
        resp.raise_for_status()
        content = resp.json()
    except httpx.HTTPStatusError:
        return False
    items = content.get('items')
    if items:
        return True
    return False
