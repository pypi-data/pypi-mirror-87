# -*- coding: utf-8 -*-
import unittest
from zope.event import notify
from zope.traversing.interfaces import BeforeTraverseEvent
from Products.CMFCore.utils import getToolByName
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, \
    setRoles, login

from plone import api
from imio.media.browser import utils
from imio.media.testing import IMIO_MEDIA_INTEGRATION


class TestIntegration(unittest.TestCase):
    layer = IMIO_MEDIA_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        notify(BeforeTraverseEvent(self.portal, self.request))

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        qi_tool = getToolByName(self.portal, 'portal_quickinstaller')
        pid = 'imio.media'
        installed = [p['id'] for p in qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')

    def test_add_media_link(self):
        multimedia = api.content.create(
            container=self.portal,
            type='media_link',
            title='video',
            remoteUrl='http://vimeo.com/95988841',
            maxwidth=300,
            maxheight=200
        )
        self.assertEqual(multimedia.maxheight, 200)

    def test_view(self):
        # Get the vienk_oembed_viewOw
        multimedia = api.content.create(
            container=self.portal,
            type='media_link',
            title='video',
            remoteUrl='http://vimeo.com/95988841',
            maxheight=800)
        view = multimedia.restrictedTraverse('@@medialink_oembed_view')
        self.assertTrue(view())
        self.assertEqual(view.request.response.status, 200)

    def test_utils(self):
        notembed = utils.embed(None, None)
        self.assertTrue(notembed == u"")
        multimedia = api.content.create(
            container=self.portal,
            type='media_link',
            title='video',
            remoteUrl='http://vimeo.com/95988841')
        view = multimedia.restrictedTraverse('@@medialink_oembed_view')
        embed = utils.embed(multimedia, view.request)
        self.assertTrue('<iframe src="https://player.vimeo.com/video/95988841?app_id=122963" width="480" height="270"'in embed)
