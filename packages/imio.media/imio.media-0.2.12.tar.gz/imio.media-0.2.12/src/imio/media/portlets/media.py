# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
from zope import schema
from imio.media import _
from plone.app.portlets.browser import formhelper
from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from AccessControl import getSecurityManager
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletDataProvider
from zope.formlib import form
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from imio.media.browser import utils


class IMediaPortlet(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u"Portlet title"),
        description=_(u"Title of the rendered portlet"),
        required=False,
    )

    target_media = schema.Choice(
        title=_(u"Target Media"),
        description=_(u"Find the Media Link which provides the items to list"),
        required=True,
        source=SearchableTextSourceBinder(
            {"portal_type": ("media_link",)}, default_query="path:"
        ),
    )


class Assignment(base.Assignment):
    implements(IMediaPortlet)

    def __init__(self, header=u"", target_media=None):
        self.header = header
        self.target_media = target_media

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        if hasattr(self, "header"):
            return self.header
        return _(u"Media Portlet")


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile("media.pt")
    render = _template

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    @property
    def available(self):
        link = self.media_link()
        return link is not None and len(link)

    def get_header(self):
        return self.data.header

    def medialink_url(self):
        media = self.media_link()
        if media is None:
            return None
        else:
            return media.absolute_url()

    def embed(self):
        return utils.embed(self.media_link(), self.request)

    def get_style(self):
        return utils.get_style(self.media_link())

    @memoize
    def media_link(self):
        media_path = self.data.target_media
        if not media_path:
            return None
        if media_path.startswith("/"):
            media_path = media_path[1:]
            if not media_path:
                return None

        portal_state = getMultiAdapter(
            (self.context, self.request), name=u"plone_portal_state"
        )
        portal = portal_state.portal()
        result = portal.unrestrictedTraverse(media_path, default=None)
        if result is not None:
            sm = getSecurityManager()
            if not sm.checkPermission("View", result):
                result = None
        return result

    def include_empty_footer(self):
        return True


class AddForm(base.AddForm):
    form_fields = form.Fields(IMediaPortlet)
    form_fields["target_media"].custom_widget = UberSelectionWidget

    label = _(u"Add media portlet")
    description = _(u"This portlet displays a media link")

    def create(self, data):
        return Assignment(**data)


class EditForm(formhelper.EditForm):
    """Portlet edit form.
   """

    form_fields = form.Fields(IMediaPortlet)
    form_fields["target_media"].custom_widget = UberSelectionWidget

    schema = IMediaPortlet
    label = _(u"Edit media portlet")
    description = _(u"This portlet displays a media link")
