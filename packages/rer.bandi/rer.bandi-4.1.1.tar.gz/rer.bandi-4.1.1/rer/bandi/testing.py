# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.restapi.testing import PloneRestApiDXLayer
from plone.testing import z2

import rer.bandi


class RerBandiLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=rer.bandi)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'rer.bandi:default')


RER_BANDI_FIXTURE = RerBandiLayer()


RER_BANDI_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RER_BANDI_FIXTURE,), name='RerBandiLayer:IntegrationTesting'
)


RER_BANDI_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(RER_BANDI_FIXTURE,), name='RerBandiLayer:FunctionalTesting'
)


RER_BANDI_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        RER_BANDI_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='RerBandiLayer:AcceptanceTesting',
)


class RerBandiRestApiLayer(PloneRestApiDXLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(RerBandiRestApiLayer, self).setUpZope(app, configurationContext)

        self.loadZCML(package=rer.bandi)

    def setUpPloneSite(self, portal):
        super(RerBandiRestApiLayer, self).setUpPloneSite(portal)
        applyProfile(portal, 'rer.bandi:default')


RER_BANDI_API_FIXTURE = RerBandiRestApiLayer()
RER_BANDI_API_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RER_BANDI_API_FIXTURE,), name="RerBandiRestApiLayer:Integration"
)

RER_BANDI_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(RER_BANDI_API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="RerBandiRestApiLayer:Functional",
)
