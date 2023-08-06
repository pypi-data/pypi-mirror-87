# -*- coding: utf-8 -*-
from collective.oembed import endpoints
from collective.oembed.api2embed import structure as api2embed_structure
from collective.oembed.consumer import _render_details_cachekey
from collective.oembed.consumer import ConsumerView
from collective.oembed.url2embed import structure as url2embed_structure
from imio.media.endpoints import get_structure
from plone.memoize.ram import cache
from urlparse import urlsplit

import logging
import requests


class MedialinkConsumerView(ConsumerView):
    def __init__(self, context, request):
        super(MedialinkConsumerView, self).__init__(context, request)

    def update(self):
        if not self.structure:
            s_cookieless = get_structure()
            s_endpoints = endpoints.get_structure()
            s_url2embed = url2embed_structure.get_structure()
            s_api2embed = api2embed_structure.get_structure()
            for providers in (s_cookieless, s_endpoints, s_url2embed, s_api2embed):
                for hostname in providers:
                    if hostname not in self.structure:
                        self.structure[hostname] = []
                    infos = providers[hostname]
                    for info in infos:
                        self.structure[hostname].append(info)

    @cache(_render_details_cachekey)
    def get_embed(self, url, maxwidth=None, maxheight=None):
        return self.get_embed_uncached(url, maxwidth=maxwidth, maxheight=maxheight)

    def get_embed_uncached(self, url, maxwidth=None, maxheight=None):
        """Override from collective.oembed to update unshort_url method """
        # logger.info("request not in cache: get_embed(%s)" % url)
        url = unshort_url(url)
        self.url = url
        self.update()
        embed = None
        consumer = self.get_consumer(url)

        if consumer and not embed:
            embed = consumer.get_embed(url, maxwidth=maxwidth, maxheight=maxheight)

        return embed

    @cache(_render_details_cachekey)
    def get_data(self, url, maxwidth=None, maxheight=None, format="json"):
        """Override from collective.oembed to update unshort_url method """
        self.update()
        url = unshort_url(url)
        consumer = self.get_consumer(url)

        if consumer:
            data = consumer.get_data(
                url, maxwidth=maxwidth, maxheight=maxheight, format=format
            )

            return data


def unshort_url(url):
    host = urlsplit(url)[1]
    if host in SHORT_URL_DOMAINS:

        logging.getLogger("requests").setLevel(logging.WARNING)
        return requests.head(url).headers["location"]

    return url


SHORT_URL_DOMAINS = [
    "tinyurl.com",
    "goo.gl",
    "bit.ly",
    "t.co",
    "youtu.be",
    "vbly.us",
]
