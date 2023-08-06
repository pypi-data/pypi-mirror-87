from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing import IS_PLONE_5
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
from plone.registry.interfaces import IRegistry
from plone.testing import z2
from zope.component import getUtility
from zope.configuration import xmlconfig
import izug.refegovservice.tests.builders


class RefeGovServiceLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

        # installProduct() is *only* necessary for packages outside
        # the Products.* namespace which are also declared as Zope 2
        # products, using <five:registerPackage /> in ZCML.
        z2.installProduct(app, 'izug.refegovservice')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'izug.refegovservice:default')
        if IS_PLONE_5:
            applyProfile(portal, 'plone.app.dexterity:testing')
            # set available languages - which default to ['en']
            registry = getUtility(IRegistry)
            registry['plone.available_languages'] = ['en', 'de']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


IZUG_REFEGOVSERVICE_FIXTURE = RefeGovServiceLayer()
IZUG_REFEGOVSERVICE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IZUG_REFEGOVSERVICE_FIXTURE, ),
    name="IzugRefEgovService:Integration")
IZUG_REFEGOVSERVICE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IZUG_REFEGOVSERVICE_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="IzugRefEgovService:Functional")
