# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory
from Products.CMFCore.permissions import setDefaultRoles
_ = MessageFactory('imio.media')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""


PROJECTNAME = "imio.media"
DEFAULT_ADD_CONTENT_PERMISSION = "%s: Add media portlet" % PROJECTNAME
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION,
                ('Manager', 'Site Administrator', 'Owner',))
