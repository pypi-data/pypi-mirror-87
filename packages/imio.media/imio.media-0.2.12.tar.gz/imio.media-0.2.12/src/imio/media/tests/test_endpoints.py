# -*- coding: utf-8 -*-
import unittest
from zope.event import notify
from zope.traversing.interfaces import BeforeTraverseEvent
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, \
    setRoles, login
from imio.media.testing import IMIO_MEDIA_INTEGRATION


class TestIntegration(unittest.TestCase):
    layer = IMIO_MEDIA_INTEGRATION

    def setUp(self):
        from imio.media import endpoints
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        notify(BeforeTraverseEvent(self.portal, self.request))
        self.module = endpoints
        self.regex_providers = endpoints.REGEX_PROVIDERS

    def test_get_structure(self):
        from imio.media import endpoints
        structure = endpoints.get_structure()
        len_endpoints = len(structure)
        self.assertTrue(len_endpoints > 0)
        for hostname in structure:
            endpoints = structure[hostname]
            for endpoint in endpoints:
                self.assertIn(u'regex', endpoint)
                self.assertIn(u'factory', endpoint)
                self.assertIn(u'consumer', endpoint)
                self.assertIn(u'endpoint', endpoint)
                endpoint_instance = endpoint['factory'](endpoint)
                self.assertIsNotNone(endpoint_instance)
                consumer_instance = endpoint['consumer'](endpoint_instance)
                self.assertIsNotNone(consumer_instance)
