# -*- coding: utf-8 -*-
from cpskin.policy.setuphandlers import add_cookiescuttr
from cpskin.policy.setuphandlers import configure_autopublish
from cpskin.policy.setuphandlers import ensure_folder_ordering
from cpskin.policy.setuphandlers import set_scales_for_image_cropping
from plone import api
from plone.app.workflow.remap import remap_workflow
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility
from zope.dottedname.resolve import resolve
from zope.ramcache.interfaces.ram import IRAMCache

import logging
import transaction


def install_collective_captchacontactinfo(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')
    portal_setup = api.portal.get_tool('portal_setup')
    portal_setup.runAllImportStepsFromProfile(
            'profile-collective.captchacontactinfo:default')
    logger.info('collective.captchacontactinfo installed')
    contactinfo_properties = api.portal.get_tool("portal_properties").contactinfo_properties
    contactinfo_properties.policy_page = "gdpr-view"


def install_auto_publishing(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')
    portal_setup = api.portal.get_tool('portal_setup')
    portal_setup.runAllImportStepsFromProfile(
            'profile-collective.autopublishing:default')
    logger.info('collective.autopublishing installed')
    configure_autopublish()


def uninstall_restapi(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')
    portal_setup = api.portal.get_tool('portal_setup')
    portal_setup.runAllImportStepsFromProfile(
            'profile-plone.restapi:uninstall')
    portal_quickinstaller = api.portal.get_tool('portal_quickinstaller')
    portal_quickinstaller.uninstallProducts(['plone.restapi'])
    logger.info('plone.restapi uninstalled')


def install_restapi(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')
    portal_setup = api.portal.get_tool('portal_setup')
    portal_setup.runAllImportStepsFromProfile(
            'profile-plone.restapi:default')
    logger.info('plone.restapi installed')


def update_font_to_https(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')
    portal_css = api.portal.get_tool('portal_css')
    for sheet in portal_css.getResources():
        sheet_id = sheet.getId()
        if 'fonts.googleapis.com' in sheet_id:
            if not sheet_id.startswith('https://'):
                # portal_css.unregisterResource(sheetid)
                new_id = sheet_id.replace('http://', 'https://')
                portal_css.renameResource(sheet_id, new_id)
                logger.info('{0} replaced by {1}'.format(sheet_id, new_id))
    portal_css.cookResources()


def update_links(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')
    portal_catalog = api.portal.get_tool('portal_catalog')
    brains = portal_catalog({'portal_type': 'Link'})
    i = 0
    for brain in brains:
        obj = brain.getObject()
        if obj.remoteUrl.startswith('resolveuid'):
            new_url = '${{navigation_root_url}}/{0}'.format(obj.remoteUrl)
            obj.remoteUrl = new_url
            logger.info('{0} update'.format(obj.absolute_url()))
            i += 1
    logger.info('{0} links updated'.format(str(i)))
    update_font_to_https(context, logger)


def remove_old_contentleadimage(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy remove_old_contentleadimage')
    portal = api.portal.get()
    sm = portal.getSiteManager()

    utilities = {
            'subscribers': sm.utilities._subscribers[0],
            'adapters': sm.utilities._adapters[0],
            # 'provided': sm.utilities._provided
            }
    util_klass = resolve('plone.browserlayer.interfaces.ILocalBrowserLayerType')
    reg_klass = resolve('collective.contentleadimage.interfaces.ILeadImageSpecific')
    for sm_type in utilities.keys():
        utility_registrations = utilities[sm_type]
        for x in utility_registrations.keys():
            if x.__module__ == util_klass.__module__ and x == util_klass:
                for name, klass in utility_registrations[x].items():
                    found = find_object_or_class(klass, reg_klass)
                    # if found:
                    #     import pdb; pdb.set_trace()
                    if found:
                        if type(utility_registrations[x][name]) in \
                                [list, tuple, set]:
                            regs = list(utility_registrations[x][name])
                            regs.remove(found)
                            logger.info('{0} {1} removed'.format(sm_type, reg_klass))
                            utility_registrations[x][name] = tuple(regs)
                        else:
                            logger.info('{0} removed'.format(name))
                            del utility_registrations[x][name]

        setattr(sm.utilities, '_' + sm_type, [utility_registrations])


def install_collective_limitfilesizepanel(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')

    portal_setup = api.portal.get_tool('portal_setup')
    portal_setup.runAllImportStepsFromProfile(
            'profile-collective.limitfilesizepanel:default')
    logger.info('collective.limitfilesizepanel installed')


def add_cpskin_collective_contact_workflow(context):
    context.runImportStepFromProfile('profile-cpskin.workflow:to1', 'workflow')
    chain = ('cpskin_collective_contact_workflow',)
    types = ('held_position',
            'organization',
            'person',
            'position')
    state_map = {'active': 'active',
            'deactivated': 'deactivated'}
    remap_workflow(context, type_ids=types, chain=chain,
            state_map=state_map)
    util = queryUtility(IRAMCache)
    if util is not None:
        util.invalidateAll()

    # set a workflow version
    context.runAllImportStepsFromProfile('profile-cpskin.workflow:default')


def delete_multilingualbehavior(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')

    portal = api.portal.get()
    sm = portal.getSiteManager()

    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile(
            'profile-plone.multilingualbehavior:uninstall')

    # Check is PAM is installed, if not remore plone.multilingual
    portal_quickinstaller = getToolByName(context, 'portal_quickinstaller')
    portal_quickinstaller.uninstallProducts(['plone.multilingualbehavior'])
    logger.info('plone.multilingualbehavior uninstalled')

    portal_setup.runAllImportStepsFromProfile(
            'profile-plone.multilingual:uninstall')
    portal_quickinstaller.uninstallProducts(['plone.multilingual'])
    logger.info('plone.multilingual uninstalled')

    subscribers = sm.adapters._subscribers
    for i, sub in enumerate(subscribers):
        for key in sub.keys():
            if 'multilingual' in str(key):
                del subscribers[i][key]
                logger.info('Deleted {0} subscriber'.format(key))
    sm.adapters._subscribers = subscribers

    transaction.commit()
    app = portal.restrictedTraverse('/')
    app._p_jar.sync()


def install_collective_atomrss(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')

    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile(
            'profile-collective.atomrss:default')
    logger.info('collective.atomrss installed')


def install_collective_cookiecuttr(context, logger=None):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(
            'profile-collective.cookiecuttr:default')
    portal = api.portal.get()
    add_cookiescuttr(portal)


def clean_registries(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy.upgrades')
    portal = api.portal.get()
    logger.info('Cleaning registries...')

    jstool = portal.portal_javascripts
    jstool.cookResources()
    logger.info('portal_javascripts has been cleaned!')

    csstool = portal.portal_css
    csstool.cookResources()
    logger.info('portal_css has been cleaned!')
    ps = portal.portal_setup
    # clean portal_setup
    for stepId in ps.getSortedImportSteps():
        stepMetadata = ps.getImportStepMetadata(stepId)
        # remove invalid steps
        if stepMetadata['invalid']:
            logger.info('Removing {0} step from portal_setup'.format(stepId))
            ps._import_registry.unregisterStep(stepId)
            ps._p_changed = True
    logger.info('portal_setup has been cleaned!')

    logger.info('Registries have been cleaned!')


def install_image_cropping(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')

    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile(
            'profile-plone.app.imagecropping:default')
    logger.info('plone.app.imagecropping installed')


def set_allowed_sizes(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')

    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(
            'profile-cpskin.policy:default', 'propertiestool')
    setup_tool.runImportStepFromProfile(
            'profile-cpskin.policy:default', 'plone.app.registry')
    set_scales_for_image_cropping()
    clean_registries(context)
    logger.info('cpskin.policy updated')


def find_object_or_class(objs, klass):
    if type(objs) not in [list, tuple, set]:
        objs = [objs]
    for obj in objs:
        if klass == obj:
            return obj

    return None


def reload_css_registry(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger("cpskin.policy")

    setup_tool = getToolByName(context, "portal_setup")
    setup_tool.runImportStepFromProfile("profile-cpskin.policy:default", "cssregistry")


def improve_eea_expression(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger("cpskin.policy")

    eea_expression = "python:'configure_faceted.html' in request.URL0"
    eea_fixed_expression = "python:'URL0' in request and 'configure_faceted.html' in request.URL0"
    portal = api.portal.get()
    for tool_id in ["portal_javascripts", "portal_css"]:
        tool = api.portal.get_tool(tool_id)
        resources = tool.getResources()
        for resource in resources:
            if resource.getExpression() == eea_expression:
                resource.setExpression(eea_fixed_expression)
                logger.info(
                    "Resource {0} expression has been fixed in {1}".format(
                        resource.getId(), tool_id
                    )
                )


def upgrade_ensure_folder_ordering(context):
    ensure_folder_ordering()
