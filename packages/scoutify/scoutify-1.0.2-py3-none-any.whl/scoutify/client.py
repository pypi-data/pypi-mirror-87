import requests as rq
"""
    Main class of client object
"""
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'


class Scoutify(object):
    def __init__(
            self,
            access_token=None,
            client_id=None,
            client_secret=None,
            redirect_url=None,
    ):
        self._access_token = access_token
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_url = redirect_url
        self._header = None

    def __get__(self, instance, owner):
        return self

    def __str__(self):
        return self._client_id

    def set_access_token(self, access_token):
        self._access_token = access_token
        self._header = {'Authorization': 'Bearer {}'.format(access_token)}

    def search(self, search_type, artist_name):
        if not self._header:
            return "No token available"
        search_url = "{}/{}".format(SPOTIFY_API_BASE_URL, 'search')
        if search_type.lower() not in ['artist', 'track', 'album', 'playlist']:
            print('Invalid search type')
            return
        params = {'type': search_type.lower(), 'q': artist_name.lower()}
        resp = rq.get(search_url, params=params, headers=self._header)
        return resp.json()

    def several_artists(self, artist_ids):
        if not self._header:
            return "No token available"
        url = "{}/{}".format(SPOTIFY_API_BASE_URL, 'artists')
        params = {'ids': ",".join(artist_ids)}
        resp = rq.get(url, params=params, headers=self._header)
        return resp.json()



