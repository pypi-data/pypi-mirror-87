import json
import secrets

import aiohttp
from lxml import html


def danbooru():
    """
    Returns an GalleryClient instance with Danbooru data.
    :return:
    :rtype: opalart.GalleryClient
    """
    client_data = {
        'as_json': True,
        'client_name': 'danbooru_',
        'client_url': 'https://danbooru.donmai.us/posts.json?tags=',
    }
    return GalleryClient(client_data)


def e621():
    """
    Returns an GalleryClient instance with E621 data.
    :return:
    :rtype: opalart.GalleryClient
    """
    client_data = {
        'as_json': True,
        'client_name': 'E621',
        'client_url': 'https://e621.net/posts.json?tags=',
        'headers': {'User-Agent': 'opalart/0.0.9'}
    }
    return GalleryClient(client_data)


def gelbooru():
    """
    Returns an GalleryClient instance with Gelbooru data.
    :return:
    :rtype: opalart.GalleryClient
    """
    client_data = {
        'as_json': False,
        'client_name': 'Gelbooru',
        'client_url': 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags='
    }
    return GalleryClient(client_data)


def konachan():
    """
    Returns an GalleryClient instance with Konachan data.
    :return:
    :rtype: opalart.GalleryClient
    """
    client_data = {
        'as_json': True,
        'client_name': 'Konachan',
        'client_url': 'https://konachan.com/post.json?limit=1000&tags='
    }
    return GalleryClient(client_data)


def rule34():
    """
    Returns an GalleryClient instance with Rule 34 data.
    :return:
    :rtype: opalart.GalleryClient
    """
    client_data = {
        'as_json': False,
        'client_name': 'Rule 34',
        'client_url': 'https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags='
    }
    return GalleryClient(client_data)


def xbooru():
    """
    Returns an GalleryClient instance with Xbooru data.
    :return:
    :rtype: opalart.GalleryClient
    """
    client_data = {
        'as_json': False,
        'client_name': 'Xbooru',
        'client_url': 'http://xbooru.com/index.php?page=dapi&s=post&q=index&tags='
    }
    return GalleryClient(client_data)


def yandere():
    """
    Returns an GalleryClient instance with Yande.re data.
    :return:
    :rtype: opalart.GalleryClient
    """
    client_data = {
        'as_json': True,
        'client_name': 'Yande.re',
        'client_url': 'https://yande.re/post.json?tags='
    }
    return GalleryClient(client_data)


class GalleryClient(object):
    def __init__(self, client_data):
        """
        :param client_data: The gallery client's data.
        :type client_data: dict
        """
        self.as_json = client_data.get('as_json')
        self.client_name = client_data.get('client_name')
        self.client_url = client_data.get('client_url')
        self.headers = client_data.get('headers')
        self.include_hash = False
        self.limit = None
        self.tags = None

    async def _fetch_posts(self):
        """|coro|
        Fetches posts with the given tags from the client.
        :return:
        :rtype: list[dict]
        """
        lookup_url = '{}{}&limit={}'.format(self.client_url, self.tags, self.limit)
        async with aiohttp.ClientSession() as aio_client:
            async with aio_client.get(lookup_url, headers=self.headers) as aio_session:
                data = await aio_session.read()
                if self.as_json:
                    try:
                        posts = json.loads(data)
                    except json.JSONDecodeError:
                        posts = []
                else:
                    posts = html.fromstring(data)
        return self._filter_posts(posts)

    def _make_post_list(self, posts):
        """
        Makes a list of file URLs and MD5 hashes, if requested.
        :param posts: The posts to parse.
        :type posts: dict or list[lxml.html.HtmlElement]
        :return:
        :rtype: list[str] or list[tuple]
        """
        key = 'url' if self.client_name == 'E621' else 'file_url'
        post_list = [ps[key] for ps in posts]
        if self.include_hash:
            post_list = [(ps_url, ps['md5']) for ps_url, ps in zip(post_list, posts)]
        return post_list

    def _filter_posts(self, posts):
        """
        Filters posts based on if they include a file_url field.
        :param posts: The posts to filter.
        :type posts: dict or list[lxml.html.HtmlElement]
        :return:
        :rtype: list[dict]
        """
        if self.as_json:
            if self.client_name == 'E621':
                posts = posts.get('posts')
                posts = [ps.get('file') for ps in posts if ps.get('file').get('url')]
            else:
                posts = [ps for ps in posts if ps.get('file_url')]
        else:
            posts = [dict(ps.attrib) for ps in posts if ps.attrib.get('file_url')]
        return self._make_post_list(posts)

    def _set_params(self, tags, limit, include_hash):
        """
        Sets parameters for use when fetching the client URL.
        :param tags: The tags to search for.
        :type tags: list[str]
        :param limit: The max number of results to return.
        :type limit: int
        :param include_hash: Whether or not to include MD5 hashes.
        :type limit: bool
        :return:
        """
        self.include_hash = include_hash
        if limit and str(limit).isdigit():
            self.limit = str(abs(limit))
        else:
            self.limit = '100'
        sorted_tags = sorted([tag.lower() for tag in tags])
        self.tags = '+'.join(sorted_tags) if tags else 'nude'

    async def getposts(self, tags, limit=None, include_hash=False):
        """|coro|
        Fetches a posts with the given tags from the client.
        Specify a lower limit to speed up response time.
        :param tags: The tags to search for.
        :type tags: list[str]
        :param limit: The max number of results to return.
        :type limit: int
        :param include_hash: Whether or not to include MD5 hashes.
        :type limit: bool
        :return:
        :rtype: list[str]
        """
        self._set_params(tags, limit, include_hash)
        posts = await self._fetch_posts()
        return posts or None

    async def randpost(self, tags, limit=None, include_hash=False):
        """|coro|
        Fetches a random post with the given tags from the client.
        Specify a lower limit to speed up response time.
        :param tags: The tags to search for.
        :type tags: list[str]
        :param limit: The max number of results to return.
        :type limit: int
        :param include_hash: Whether or not to include MD5 hashes.
        :type limit: bool
        :return:
        :rtype: str
        """
        self._set_params(tags, limit, include_hash)
        posts = await self._fetch_posts()
        return secrets.choice(posts) if posts else None
