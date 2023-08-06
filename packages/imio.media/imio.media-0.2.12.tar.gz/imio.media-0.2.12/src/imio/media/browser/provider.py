# -*- coding: utf-8 -*-
from collective.oembed.provider import OEmbedProvider
from imio.media.browser.consumer import MedialinkConsumerView

import json


class MedialinkProxyOembedProvider(OEmbedProvider, MedialinkConsumerView):
    """This oembed provider can be used as proxy consumer"""

    def __init__(self, context, request):
        OEmbedProvider.__init__(self, context, request)
        MedialinkConsumerView.__init__(self, context, request)
        self.is_local = False

    def update(self):
        if self.url is None:
            self.url = self.request.get("url", None)

        OEmbedProvider.update(self)  # update in all case
        if self.url.startswith(self.context.absolute_url()):
            self.is_local = True
        else:
            MedialinkConsumerView.update(self)
            self._url = self.url
            self._maxheight = self.maxheight
            self._maxwidth = self.maxwidth

    def __call__(self):
        self.update()
        if self.is_local:
            result = OEmbedProvider.__call__(self)
        else:

            result = MedialinkConsumerView.get_data(
                self,
                self.url,
                maxwidth=self.maxwidth,
                maxheight=self.maxheight,
                format="json",
            )

            if type(result) == dict:
                result = json.dumps(result)

        return result
