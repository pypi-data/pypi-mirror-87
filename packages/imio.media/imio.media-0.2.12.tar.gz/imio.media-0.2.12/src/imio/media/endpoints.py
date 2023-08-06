# -*- coding: utf-8 -*-
from collective.oembed.endpoints import Consumer
from collective.oembed.endpoints import endpoint_factory
from collective.oembed.endpoints import TEMPLATES

import logging
import oembed
import re
import urlparse
logger = logging.getLogger("collective.oembed")


class CookieLessConsumer(Consumer):
    """Consumer which wrap one end point"""

    def get_embed(self, url, maxwidth=None, maxheight=None, format="json"):
        data = self.get_data(url, maxwidth=maxwidth, maxheight=maxheight, format=format)
        if not data:
            return u""
        data = self.get_no_cookie_url(data)
        if data is None or u"type" not in data:
            return u""
        return TEMPLATES[data[u"type"]] % data

    def get_no_cookie_url(self, data):
        iframe_html = data.get("html")
        regex_result = re.search(r'src\s*=\s*"(.+?)"', iframe_html)
        if regex_result is not None:
            url = regex_result.groups()[0]
            parsed = urlparse.urlparse(url)
            new_url = u""
            if "youtube" in parsed.hostname.lower():
                youtube_title = data.get("title")
                iframe_html = iframe_html.replace(
                    u"<iframe", u"{} title=\"{}\"".format(u"<iframe", youtube_title)
                )
                new_url = u"{}://{}{}".format(
                    parsed.scheme, "www.youtube-nocookie.com", parsed.path
                )
                data["html"] = iframe_html.replace(url, new_url)
            if "vimeo" in parsed.hostname.lower():
                new_url = u"{}://{}{}?dnt=1".format(
                    parsed.scheme, parsed.netloc, parsed.path
                )
                data["html"] = iframe_html.replace(url, new_url)
        return data


REGEX_PROVIDERS = [
    {
        u"hostname": ("www.youtube.com",),
        u"regex": ["regex:.*youtube\.com/watch.*", "regex:.*youtube\.com/playlist.*"],
        u"endpoint": "http://www.youtube.com/oembed",
        u"timeout": 2,
    },
    {
        u"hostname": ("vimeo.com",),
        u"regex": ["https://vimeo.com/*", "https://vimeo.com/*"],
        u"endpoint": "https://vimeo.com/api/oembed.{format}",
        u"timeout": 2,
    },
]


# def endpoint_factory(info):
#     return oembed.OEmbedEndpoint(
#         info[u"endpoint"], info[u"regex"], timeout=info["timeout"]
#     )


def get_structure():
    endpoints = {}

    for provider in REGEX_PROVIDERS:
        provider["factory"] = endpoint_factory
        provider["consumer"] = CookieLessConsumer
        provider["timeout"] = provider.get("timeout", oembed.NO_TIMEOUT)
        for hostname in provider["hostname"]:
            endpoints[hostname] = [provider]

    return endpoints
