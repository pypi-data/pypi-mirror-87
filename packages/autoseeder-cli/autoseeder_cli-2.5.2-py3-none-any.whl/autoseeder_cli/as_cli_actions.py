import requests
import json
import sys

from io import BytesIO

try:
    from urlparse import urljoin
    from urllib import urlencode
except ImportError:
    from urllib.parse import urljoin, urlencode

from .util import api_login, logger

__all__ = ['AutoseederLister',
           'AutoseederScreenshotDownloader',
           'AutoseederSearcher',
           'AutoseederSubmitter',
           'AutoseederTokenGetter',
           'AutoseederURLViewer',
           'AutoseederCSVDownloader'
           ]


class AbstractAutoseederAction(object):
    user = None
    password = None
    base_url = None
    token = None

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', None)
        logger.debug(kwargs)
        self.user = kwargs.pop('user', None)
        self.password = kwargs.pop('password', None)
        self.base_url = kwargs.pop('base_url', None)
        if not self.token and self.user and self.password:
            self.token = api_login(self.base_url, self.user, self.password)
        elif self.token:
            pass
        else:
            raise ValueError('Error logging you into {}, check your environment credentials'.format(self.base_url))


class AutoseederLister(AbstractAutoseederAction):
    limit = None

    def __init__(self, *args, limit = None, desc = None, **kwargs):
        try:
            if limit is not None:
                limit = int(limit)
        except (TypeError, ValueError):
            raise TypeError("--limit must be a number")

        self.limit = limit
        self.desc = desc
        super(AutoseederLister, self).__init__(*args, **kwargs)

    def get_url_list(self, url_filter = None):
        path = urljoin(self.base_url, 'api/v0/urls/')
        params = {}
        if self.limit is not None and self.limit > 0:
            print("Note: A limit is in use, returning at most {} rows".format(self.limit), file=sys.stderr)
            params['limit'] = self.limit
        if self.desc:
            params['desc'] = 'yes'
        if url_filter is not None:
            params['url_filter'] = url_filter
        if len(params.keys()) > 0:
            path = path + '?' + urlencode(params)
        h = {'Authorization': 'Token ' + self.token,
             'Accept': 'application/json; indent=2'}
        r = requests.get(path, headers=h)
        logger.debug(r)

        if r.status_code == 401:
            raise RuntimeError('Invalid token, could not authenticate')
        elif r.status_code != 200:
            logger.debug(r.status_code)
            logger.debug(r.content)
            raise RuntimeError('Unhandled response from URL list API endpoint')

        return r.json()

    def format_report(self):
        report = self.get_url_list()
        return json.dumps(report, indent=2)


class AutoseederSearcher(AbstractAutoseederAction):
    """
    AutoseederSearcher lets you find the UUIDs of particular URLs
    so you can perform other operations on them.

    NOTE: This is a highly inefficient stand-in at the moment for
    a proper search API. It gets full list, then returns UUID from
    first match.
    """

    def __init__(self, *args, **kwargs):
        super(AutoseederSearcher, self).__init__(*args, **kwargs)
        self.lister = AutoseederLister(base_url=self.base_url, token=self.token)

    def find_urls(self, url_term, *, detail: bool = False):
        """
        Return the UUID for each URL matching the <url_term>.
        """
        url_list = self.lister.get_url_list(url_filter=url_term)

        if len(url_list) > 0:
            for url in url_list:
                if detail == False:
                    yield url.get("uuid")
                else:
                    yield url
        else:
            raise ValueError("Couldn't find any URL containing '{}'".format(url_term))


class AutoseederSubmitter(AbstractAutoseederAction):
    def __init__(self, *args, **kwargs):
        super(AutoseederSubmitter, self).__init__(*args, **kwargs)

    def submit_url(self, url, seed_regions_str=None):
        """
        :param url: URL string to be submitted
        :param seed_regions_str: string containing comma-separated list of
                                 seeding regions (e.g. "AU,NZ")
        """
        path = urljoin(self.base_url, 'api/v0/submit/')
        h = {'Authorization': 'Token ' + self.token, 'Content-Type': 'application/json'}
        d = {'url': url}

        if seed_regions_str:
            d['proxy_constraints'] = {'countries': seed_regions_str.split(',')}

        logger.debug("Submitting with HTTP params: {}".format(d))

        r = requests.post(path, json=d, headers=h)
        logger.debug(r.status_code)
        logger.debug(r.content)

        if r.status_code == 401:
            raise RuntimeError('Invalid token, could not authenticate')
        elif r.status_code == 409:
            raise ValueError('URL appears to be a duplicate')
        elif r.status_code != 201:
            logger.debug("Error submitting to API: {}".format(r.content))
            raise RuntimeError('Unexpected response from URL submission API endpoint')

        return r.json()


class AutoseederURLViewer(AbstractAutoseederAction):
    def __init__(self, *args, **kwargs):
        super(AutoseederURLViewer, self).__init__(*args, **kwargs)

    def get_url_data(self, uuid):
        path = urljoin(self.base_url, 'api/v0/urls/{}/'.format(uuid))
        h = {'Authorization': 'Token ' + self.token,
             'Accept': 'application/json; indent=2'}
        r = requests.get(path, headers=h)

        if r.status_code == 401:
            raise ValueError('Invalid token')
        elif r.status_code == 404:
            raise Exception('Error from API endpoint: No such UUID ({}) exists'.format(uuid))
        elif r.status_code != 200:
            logger.debug(r.status_code)
            logger.debug(r.content)
            raise Exception('Unhandled response from URL list API endpoint')

        return json.dumps(r.json(), indent=2)


class AutoseederTokenGetter(AbstractAutoseederAction):
    def __init__(self, *args, **kwargs):
        super(AutoseederTokenGetter, self).__init__(*args, **kwargs)

    def get_token(self):
        return self.token


class AutoseederScreenshotDownloader(AbstractAutoseederAction):
    def __init__(self, *args, **kwargs):
        super(AutoseederScreenshotDownloader, self).__init__(*args, **kwargs)

    def get_screenshot(self, uuid):
        path = urljoin(self.base_url, 'api/v0/urls/screenshot/{}'.format(uuid))
        h = {'Authorization': 'Token ' + self.token}
        r = requests.get(path, headers=h, stream=True)

        if r.status_code == 401:
            raise ValueError('Invalid token')
        elif r.status_code == 404:
            raise Exception('Error from API endpoint: No such UUID ({}) exists'.format(uuid))
        elif r.status_code != 200:
            logger.debug(r.status_code)
            logger.debug(r.content)
            raise Exception('Unhandled response from screenshot API endpoint.')
        with BytesIO() as stream:
            for chunk in r:
                stream.write(chunk)
            return stream.getvalue()


class AutoseederCSVDownloader(AbstractAutoseederAction):
    def get_csv_data(self):
        path = urljoin(self.base_url, 'api/v0/urls/?output_format=csv')
        h = {'Authorization': 'Token ' + self.token}
        r = requests.get(path, headers=h)

        if r.status_code == 401:
            raise RuntimeError('Invalid token, could not authenticate')
        elif r.status_code != 200:
            logger.debug(r.status_code)
            logger.debug(r.content)
            raise RuntimeError('Unhandled response from URL list API endpoint')

        return r.text
