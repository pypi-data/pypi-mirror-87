# -*- coding: utf-8 -*-
from plone.testing import z2
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE

import imio.media


IMIO_MEDIA = PloneWithPackageLayer(
    zcml_package=imio.media,
    zcml_filename='testing.zcml',
    gs_profile_id='imio.media:testing',
    name='IMIO_MEDIA'
)

IMIO_MEDIA_INTEGRATION = IntegrationTesting(
    bases=(IMIO_MEDIA, ),
    name="IMIO_MEDIA_INTEGRATION"
)

IMIO_MEDIA_FUNCTIONAL = FunctionalTesting(
    bases=(IMIO_MEDIA, ),
    name="IMIO_MEDIA_FUNCTIONAL"
)

IMIO_MEDIA_ROBOT_TESTING = FunctionalTesting(
    bases=(IMIO_MEDIA, REMOTE_LIBRARY_BUNDLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="IMIO_MEDIA_ROBOT_TESTING")
