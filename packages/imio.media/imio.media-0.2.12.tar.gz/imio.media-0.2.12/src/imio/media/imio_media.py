# -*- coding: utf-8 -*-
from zope.interface import implements
from plone.supermodel import model
from zope.schema import TextLine, Int
from . import _
from plone.app.textfield import RichText
from plone.dexterity.content import Item


class IMediaLink(model.Schema):
    """ Schema for MediaLink template """
    remoteUrl = TextLine(
        title=_(u'URL'),
        description=u'',
        default=u'http://'
    )

    maxwidth = Int(
        title=_(u'Max width'),
        description=_(u'Like "1024", this value is in pixel'),
        required=False,
        default=1024,
    )

    maxheight = Int(
        title=_(u'Max height'),
        description=_(u'Like "768", this value is in pixel'),
        required=False,
    )

    richdescription = RichText(
        title=_(u'Detailed description'),
        required=False
    )


class MediaLink(Item):
    """ """
    implements(IMediaLink)

    def style_attr(self):
        return "width: {};height: {}".format(
            self.maxwidth,
            self.maxheight)
