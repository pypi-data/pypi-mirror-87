# -*- coding: utf-8 -*-
from Products.CMFPlone import interfaces
from Products.CMFQuickInstallerTool import interfaces as quiskinstallinterfaces
from zope.interface import implements


class HiddenProfiles(object):
    implements(interfaces.INonInstallable)

    def getNonInstallableProfiles(self):
        """Hides profiles from 'Add Plone site' form"""
        return [u'cpskin.contenttypes:default',
                u'cpskin.core:default',
                u'cpskin.core:members-configuration',
                u'cpskin.core:uninstall',
                u'cpskin.menu:default',
                u'cpskin.menu:uninstall',
                u'cpskin.minisite:default',
                u'cpskin.minisite:uninstall',
                u'cpskin.policy:uninstall',
                u'cpskin.slider:default',
                u'cpskin.slider:uninstall',
                u'cpskin.theme:default',
                u'cpskin.theme:members-configuration',
                u'cpskin.theme:uninstall',
                u'cpskin.workflow:default',
                u'cpskin.workflow:members-configuration',
                u'cpskin.workflow:uninstall',
                u'collective.directory:uninstall',
                ]


class HiddenProducts(object):
    implements(quiskinstallinterfaces.INonInstallable)

    def getNonInstallableProducts(self):
        """Hides profiles from QuickInstaller"""
        return [u'cpskin.core',
                u'cpskin.locales',
                u'cpskin.menu',
                u'cpskin.minisite',
                u'cpskin.policy',
                u'cpskin.slider',
                u'cpskin.theme',
                u'cpskin.workflow']
