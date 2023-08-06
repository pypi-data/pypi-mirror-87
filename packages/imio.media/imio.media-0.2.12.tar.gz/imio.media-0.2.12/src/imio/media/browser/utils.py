# -*- coding: utf-8 -*-
from imio.media.browser.consumer import MedialinkConsumerView


def embed(media, request):
    consumer_view = MedialinkConsumerView(media, request)
    if not consumer_view or not getattr(media, 'remoteUrl', False):
        return u""
    consumer_view._url = media.remoteUrl

    return consumer_view.get_embed_auto()


def get_style(media):
    result = ''
    if media.maxwidth:
        result += 'max-width: {}px;'.format(media.maxwidth)

    if media.maxheight:
        result += 'max-height: {}px;'.format(media.maxheight)

    return result
