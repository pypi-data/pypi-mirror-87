# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from imio.media.browser import utils


class FacetedOembedView(BrowserView):
    """
    """

    def embed(self, obj):
        return utils.embed(obj, self.request)

    def get_style(self, obj):
        return utils.get_style(obj)
