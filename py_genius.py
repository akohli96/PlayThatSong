"""
Genius

Thin wrapper around the Genius API
"""

from __future__ import print_function
from functools import wraps
import requests


def textformat(func):
    "Add text_format value to kwargs if not supplied"
    @wraps(func)
    def inner(*args, **kwargs):
        "Add text_format to kwargs"
        try:
            tformat = kwargs['text_format']
        except KeyError:
            tformat = 'dom'

        if tformat.lower() not in ['dom', 'html', 'plain']:
            raise TypeError("Optional arg 'text_format' can only be one of 'dom', 'html' or 'plain'")

        kwargs['text_format'] = tformat.lower()
        return func(*args, **kwargs)
    return inner

class Genius(object):
    """
    Thin wrapper around Genius API

    If all goes well, each method returns a
    dictionary of JSON data from the Genius
    REST API
    """
    def __init__(self, access_token):
        _auth = {'Authorization': "Bearer {}".format(access_token)}
        self._session = requests.Session()
        self._session.headers.update(_auth)
        self.prefix = "https://api.genius.com"

    def __internal_call(self, method, url, params=None):
        response = self._session.request(method, url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def search(self, query):
        "Search documents hosted on Genius"
        url = "{}/search".format(self.prefix)
        payload = {"q": query}

        return self.__internal_call('GET', url, params=payload)

    @textformat
    def get_annotations(self, _id, text_format=None):
        "Data for a specific annotation."
        url = "{}/annotations/{}".format(self.prefix, _id)
        payload = {"text_format": text_format}

        return self.__internal_call('GET', url, params=payload)

    @textformat
    def get_referents(self, created_by_id, song_id=None, web_page_id=None, text_format=None, per_page=None, page=None):
        "Referents by content item or user responsible for an included annotation."
        # locals needs to be called first to limit its contents
        args = locals()

        if song_id and web_page_id:
            raise TypeError("You may pass only one of 'song_id' and 'web_page_id', not both.")

        # reduce dictionary of kwarg names and values to only those with values
        payload = {
            key : value
            for key, value
            in args.items()
            if value and key not in [
                'self',
                'created_by_id'
            ]}
        print(payload)

        url = "{}/referents/{}".format(self.prefix, created_by_id)

        return self.__internal_call('GET', url, params=payload)

    @textformat
    def get_song(self, _id, text_format=None):
        "Data for a specific song."
        url = "{}/songs/{}".format(self.prefix, _id)
        payload = {"text_format": text_format}

        return self.__internal_call('GET', url, params=payload)

    @textformat
    def get_artist(self, _id, text_format=None):
        "Data for a specific artist."
        url = "{}/artists/{}".format(self.prefix, _id)
        payload = {"text_format": text_format}

        return self.__internal_call('GET', url, params=payload)

    def get_artist_songs(self, _id, sort=None, page=None, per_page=None):
        """Documents (songs) for the artist specified.
        By default, 20 items are returned for each request."""
        # locals needs to be called first to limit its contents
        args = locals()

        # reduce dictionary of kwarg names and values to only those with values
        payload = {
            key : value
            for key, value
            in args.items()
            if value and key not in [
                'self',
                '_id'
            ]}
        print(payload)

        url = "{}/artists/{}/songs".format(self.prefix, _id)

        return self.__internal_call('GET', url, params=payload)

    def get_web_pages(self, raw_annotatable_url=None, canonical_url=None, og_url=None):
        # locals needs to be called first to limit its contents
        args = locals()

        if not(raw_annotatable_url or canonical_url or og_url):
            raise TypeError("Provide as many of the following variants of the URL as possible:\n 'raw_annotatable_url', 'canonical_url', 'og_url'")
        
        
        url = "{}/web_pages/lookup".format(self.prefix)

        # reduce dictionary of kwarg names and values to only those with values
        payload = {
            key : value
            for key, value
            in args.items()
            if value and key != 'self'
        }
        print(payload)

        return self.__internal_call('GET', url, params=payload)



    """
    Methods requiring scopes.
    Not available when using a client_access_token thus not implemented.

    @textformat
    def get_account(self, text_format=None):
        #Account information for the currently authenticated user.

        #Requires scope: me
        
        url = "{}/account".format(self.prefix)
        return self.__internal_call('GET', url)

    def post_annotation(self):
        pass

    def update_annotation(self, _id):
        pass

    def delete_annotation(self, _id):
        pass

    def upvote_annotation(self, _id):
        pass

    def downvote_annotation(self, _id):
        pass

    def unvote_annotation(self, _id):
        pass
    """