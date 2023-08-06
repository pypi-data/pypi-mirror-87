# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from plone.testing import z2

import cpskin.policy


class CpskinPolicyPloneWithPackageLayer(PloneWithPackageLayer):
    """
    """
    def setUpZope(self, app, configurationContext):
        super(CpskinPolicyPloneWithPackageLayer, self).setUpZope(
            app,
            configurationContext)
        z2.installProduct(app, 'Products.DateRecurringIndex')

    def tearDownZope(self, app):
        # Uninstall products installed above
        z2.uninstallProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')
        applyProfile(portal, 'cpskin.policy:testing')
        applyProfile(portal, 'cpskin.demo:default')


CPSKIN_POLICY_FIXTURE = CpskinPolicyPloneWithPackageLayer(
    name='CPSKIN_POLICY_FIXTURE',
    zcml_filename='testing.zcml',
    zcml_package=cpskin.policy,
    additional_z2_products=('Products.PasswordStrength',),
    gs_profile_id='cpskin.policy:testing')

CPSKIN_POLICY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_POLICY_FIXTURE,),
    name='CPSkinPolicy:Integration')

CPSKIN_POLICY_ROBOT_TESTING = FunctionalTesting(
    bases=(CPSKIN_POLICY_FIXTURE,
           REMOTE_LIBRARY_BUNDLE_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name='cpskin.policy:Robot')
