# -*- coding: utf-8 -*-
from collective.autopublishing.browser.autopublishsettings import AutopublishSpecification
from collective.autopublishing.browser.autopublishsettings import IAutopublishSettingsSchema
from collective.complexrecordsproxy import ComplexRecordsProxy
from cpskin.core.interfaces import IFolderViewSelectedContent
from cpskin.locales import CPSkinMessageFactory as _
from plone import api
from plone.app.event.interfaces import IEventSettings
from plone.app.workflow.remap import remap_workflow
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.folder.default import DefaultOrdering
from plone.registry.interfaces import IRegistry
from Products.ATContentTypes.lib import constraintypes
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.syndication import IFeedSettings
from Products.CMFPlone.utils import _createObjectByType
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import alsoProvides
from zope.ramcache.interfaces.ram import IRAMCache

import logging
import os


logger = logging.getLogger('cpskin.policy')
timezone = 'Europe/Brussels'


def publishContent(wftool, content):
    if wftool.getInfoFor(content, 'review_state') != 'published':
        actions = [a.get('id') for a in wftool.listActions(object=content)]
        # we need to handle both workflows
        if 'publish_and_hide' in actions:
            wftool.doActionFor(content, 'publish_and_hide')
        elif 'publish' in actions:
            wftool.doActionFor(content, 'publish')


def installPolicy(context):
    if context.readDataFile('cpskin.policy-default.txt') is None:
        return

    logger.info('Installing policy')
    default_language = 'fr'
    portal_languages = api.portal.get_tool('portal_languages')
    portal_languages.setDefaultLanguage(default_language)
    supported = portal_languages.getSupportedLanguages()
    portal_languages.removeSupportedLanguages(supported)
    portal_languages.addSupportedLanguage(default_language)

    # set plone.app.event
    reg = getUtility(IRegistry)
    settings = reg.forInterface(IEventSettings, prefix='plone.app.event')
    if not settings.portal_timezone:
        logger.info('Set timezone to Europe/Brussels')
        settings.portal_timezone = timezone
        settings.first_weekday = 0
        settings.available_timezones = [timezone]

    portal = api.portal.get()

    # review_state
    review_index = 'review_state'
    review_operator = 'plone.app.querystring.operation.selection.is'
    review_states = ['published_and_hidden', 'published_and_shown']

    setCriterion(portal=portal,
                 folder_name='actualites',
                 index=review_index,
                 operator=review_operator,
                 value=review_states)
    setCriterion(portal=portal,
                 folder_name='evenements',
                 index=review_index,
                 operator=review_operator,
                 value=review_states)

    # expires
    not_expired_index = 'expires'
    not_expired_operator = 'plone.app.querystring.operation.date.afterToday'

    setCriterion(portal=portal,
                 folder_name='actualites',
                 index=not_expired_index,
                 operator=not_expired_operator)
    setCriterion(portal=portal,
                 folder_name='evenements',
                 index='end',
                 operator='plone.app.querystring.operation.date.afterToday')

    renameIndexhtml(portal)
    portal.setLayout('folderview')

    add_alaune(portal)
    create_menu(portal)
    add_cookiescuttr(portal)
    set_scales_for_image_cropping()
    enable_sitemap(portal)
    add_mail_host()
    # use_email_as_login()
    set_contact_worflow()
    configure_autopublish()
    ensure_folder_ordering()


def configure_autopublish():
    settings = getUtility(IRegistry).forInterface(
        IAutopublishSettingsSchema,
        omit=('publish_actions', 'retract_actions'),
        factory=ComplexRecordsProxy)

    publish_action = AutopublishSpecification(
        {
            'portal_types': (u'News Item', 'Event'),
            'initial_state': u'created',
            'transition': u'publish_and_hide',
        }
    )
    settings.publish_actions = (publish_action,)

    retract_action = AutopublishSpecification(
        {
            'portal_types': (u'News Item', 'Event'),
            'initial_state': u'published_and_hidden',
            'transition': u'back_to_created',
        }
    )
    retract_action.date_index = u'expires'
    settings.retract_actions = (retract_action,)
    settings.dry_run = False


def renameIndexhtml(portal):
    if portal.get('index_html'):
        # Should be deteled
        api.content.rename(obj=portal['index_html'], new_id='index_html.old')


def uninstallPolicy(context):
    if context.readDataFile('cpskin.policy-uninstall.txt') is None:
        return

    logger.info('Uninstalling policy')
    portal = context.getSite()
    deleteContentRules(portal)

    review_index = 'review_state'
    review_operator = 'plone.app.querystring.operation.selection.is'
    review_state = ['published']

    setCriterion(portal=portal,
                 folder_name='actualites',
                 index=review_index,
                 operator=review_operator,
                 value=review_state)
    setCriterion(portal=portal,
                 folder_name='evenements',
                 index=review_index,
                 operator=review_operator,
                 value=review_state)


def createEventsAndNews(portal):
    """
    Inspired by Products.CMFPlone.setuphandlers
    """
    language = portal.Language()
    wftool = getToolByName(portal, 'portal_workflow')
    actu_folder = getattr(portal, 'actualites')
    events_folder = getattr(portal, 'evenements')
    # News topic
    if actu_folder:
        actu_folder.title = _(u'Actualités')
        actu_folder.description = _(u'Actualités du site')
        _createObjectByType(
            'Collection',
            portal.actualites,
            id='actualites',
            title=actu_folder.title,
            description=actu_folder.description)

        folder = portal.actualites
        alsoProvides(folder, IFolderViewSelectedContent)
        folder.setConstrainTypesMode(constraintypes.ENABLED)
        folder.setLocallyAllowedTypes(['News Item'])
        folder.setImmediatelyAddableTypes(['News Item'])
        folder.setDefaultPage('actualites')
        folder.unmarkCreationFlag()
        folder.setLanguage(language)
        alsoProvides(folder, IFolderViewSelectedContent)
        publishContent(wftool, folder)

        topic = portal.actualites.actualites
        IFeedSettings(topic).enabled = True
        topic.setLanguage(language)

        query = [{'i': 'portal_type',
                  'o': 'plone.app.querystring.operation.selection.is',
                  'v': ['News Item']},
                 {'i': 'review_state',
                  'o': 'plone.app.querystring.operation.selection.is',
                  'v': ['published']}]
        topic.setQuery(query)

        topic.setSort_on('effective')
        topic.setSort_reversed(True)
        topic.setLayout('summary_view')
        topic.unmarkCreationFlag()
        publishContent(wftool, topic)

    # Events topic
    if events_folder:
        events_folder.title = _(u'Événements')
        events_folder.description = _(u'Événements du site')
        _createObjectByType('Collection', portal.evenements, id='evenements',
                            title=events_folder.title,
                            description=events_folder.description)

        folder = portal.evenements
        alsoProvides(folder, IFolderViewSelectedContent)
        folder.setConstrainTypesMode(constraintypes.ENABLED)
        folder.setLocallyAllowedTypes(['Event'])
        folder.setImmediatelyAddableTypes(['Event'])
        folder.setDefaultPage('evenements')
        folder.unmarkCreationFlag()
        folder.setLanguage(language)
        publishContent(wftool, folder)

        topic = folder.evenements
        IFeedSettings(topic).enabled = True
        topic.unmarkCreationFlag()
        topic.setLanguage(language)

        query = [{'i': 'portal_type',
                  'o': 'plone.app.querystring.operation.selection.is',
                  'v': ['Event']},
                 {'i': 'start',
                  'o': 'plone.app.querystring.operation.date.afterToday',
                  'v': ''},
                 {'i': 'review_state',
                  'o': 'plone.app.querystring.operation.selection.is',
                  'v': ['published']}]
        topic.setQuery(query)
        topic.setSort_on('start')
        topic.setLayout('summary_view')
        publishContent(wftool, topic)


def add_alaune(portal):
    news_folder = getattr(portal, 'actualites', None)
    if news_folder:
        # check if folder is not already provided
        alsoProvides(news_folder, IFolderViewSelectedContent)
    event_folder = getattr(portal, 'evenements', None)
    if event_folder:
        # check if folder is not already provided
        alsoProvides(event_folder, IFolderViewSelectedContent)
    alaune_folder = getattr(portal, 'a-la-une', None)

    if not alaune_folder:
        folder = api.content.create(container=portal,
                                    type='Folder',
                                    id='a-la-une')
        folder.setTitle(_(u'À la une'))
        folder.reindexObject()
        portalPath = api.portal.get().getPhysicalPath()
        contextPath = '/'.join(folder.getPhysicalPath()[len(portalPath):])
        alsoProvides(folder, IFolderViewSelectedContent)
        collection = api.content.create(container=folder,
                                        type='Collection',
                                        id='a-la-une',
                                        title=_(u'À la une'))
        query = [{'i': 'hiddenTags',
                  'o': 'plone.app.querystring.operation.selection.is',
                  'v': 'a-la-une'},
                 {'i': 'path',
                  'o': 'plone.app.querystring.operation.string.path',
                  'v': '/{0}'.format(contextPath)}]
        collection.setQuery(query)
        collection.setSort_on('effective')
        collection.setSort_reversed(True)
        collection.setLayout('summary_view')
        folder.setDefaultPage('a-la-une')
        portal.moveObjectToPosition(folder.id, 1)


def migrateTopicIds(portal):
    pc = getToolByName(portal, 'portal_catalog')
    for brainTopic in pc(portal_type='Topic'):
        topic = brainTopic.getObject()
        topic_parent = topic.aq_parent
        api.content.delete(obj=topic)
        if topic_parent.getId() == 'news':
            api.content.rename(obj=topic_parent, new_id='actualites')
        if topic_parent.getId() == 'events':
            api.content.rename(obj=topic_parent, new_id='evenements')


def setCriterion(portal, folder_name, index, operator, value=None):
    """
    Change existing criterion to collection, or add a new one
    """
    folder = getattr(portal, folder_name, None)
    if folder and getattr(folder, 'index', False):
        collection = folder.index
        if not getattr(collection, 'query', False):
            migrateTopicIds(portal)
            createEventsAndNews(portal)
            folder = getattr(portal, folder_name, None)
            collection = folder.index

        queries = collection.query

        # Remove existing query, usefull for reinstalling too
        for query in queries[:]:
            if query['i'] == index:
                queries.remove(query)

        # Create new query
        new_query = {'i': index,
                     'o': operator}
        if value is not None:
            new_query['v'] = value

        queries.append(new_query)

        collection.setQuery(queries)


def deleteContentRules(portal):
    storage = getUtility(IRuleStorage)
    if 'citizen-move-event' in storage:
        del storage['citizen-move-event']
    if 'citizen-reject-event' in storage:
        del storage['citizen-reject-event']


def create_menu(portal):
    folders = [
        {'ma-commune': 'Ma commune'},
        {'loisirs': 'Loisirs'},
        {'economie': 'Economie'},
        {'je-suis': 'Je suis'},
        {'je-trouve': 'Je trouve'},
    ]
    for f in folders:
        folder_id, folder_name = f.items()[0]
        if not getattr(portal, folder_id, None):
            folder = api.content.create(
                container=portal,
                type='Folder',
                id=folder_id,
            )
            folder.setTitle(folder_name)
            folder.reindexObject()
            api.content.transition(folder, 'publish_and_show')


def add_cookiescuttr(portal):
    api.portal.set_registry_record(
        'collective.cookiecuttr.interfaces.ICookieCuttrSettings.cookiecuttr_enabled',  # noqa
        True)

    api.portal.set_registry_record(
        'collective.cookiecuttr.interfaces.ICookieCuttrSettings.implied_consent',  # noqa
        True)

    api.portal.set_registry_record(
        'collective.cookiecuttr.interfaces.ICookieCuttrSettings.accept_button',
        [{'text': u'Accept cookies', 'language': u'en'},
         {'text': u'Accepter les cookies', 'language': u'fr'}])

    api.portal.set_registry_record(
        'collective.cookiecuttr.interfaces.ICookieCuttrSettings.link',
        [{'text': u'/cookies-page ', 'language': u'en'},
         {'text': u'/cookies-page', 'language': u'fr'}])

    api.portal.set_registry_record(
        'collective.cookiecuttr.interfaces.ICookieCuttrSettings.text',
        [{'text': u"We use cookies. <a href='{{cookiePolicyLink}}' title='read about our cookies'> Read everything </a>", 'language': u'en'},  # noqa
         {'text': u"Nous utilisons des cookies pour faciliter la navigation et le partage social. <a href='{{cookiePolicyLink}}' title='read about our cookies'> Plus d\'informations </a>", 'language': u'fr'}])  # noqa


def set_scales_for_image_cropping():
    """This is made in setuphandler beacause propertiestool.xml must be
    charged before adding scales for image cropping"""
    crop_allowed = [
        'slider', 'collection', 'header', 'banner', 'visuel', 'multimedia']
    api.portal.set_registry_record(
        'plone.app.imagecropping.browser.settings.ISettings.cropping_for',
        crop_allowed)


def enable_sitemap(context, logger=None):
    pprop = getToolByName(context, 'portal_properties')
    site_properties = pprop.site_properties
    site_properties.exposeDCMetaTags = True
    site_properties.enable_sitemap = True


def add_mail_host(context=None):
    mailhost = api.portal.get_tool('MailHost')
    mailhost.smtp_queue = True
    smtp_queue_directory = os.environ.get(
        'SMTP_QUEUE_DIRECTORY',
        '/home/imio/imio-website/var/mailhost/queue')
    mailhost.smtp_queue_directory = smtp_queue_directory
    # mailhost.smtp_host = 'mailrelay.imio.be'
    mailhost.smtp_host = 'mailrelay.imio.be'
    mailhost.smtp_port = 25
    mailhost._stopQueueProcessorThread()
    mailhost._startQueueProcessorThread()
    mailhost.manage_restartQueueThread()


def use_email_as_login():
    pprop = api.portal.get_tool('portal_properties')
    site_properties = pprop.site_properties
    site_properties.manage_changeProperties(use_email_as_login=True)


def set_contact_worflow():
    portal = api.portal.get()
    portal_workflow = api.portal.get_tool('portal_workflow')
    workflow = portal_workflow.getWorkflowsFor('organization')
    if len(workflow) > 1:
        logger.info(u'To much workflow for contacts.')
        return
    if len(workflow) == 0:
        logger.info(u'No workflow for contacts.')
        return
    workflow_id = workflow[0].id
    if workflow_id == 'cpskin_collective_contact_workflow':
        logger.info(u'cpskin_collective_contact_workflow already set.')
        return
    chain = ('cpskin_collective_contact_workflow',)
    types = ('held_position',
             'organization',
             'person',
             'position')
    state_map = {'active': 'active',
                 'deactivated': 'deactivated'}
    remap_workflow(portal, type_ids=types, chain=chain,
                   state_map=state_map)
    util = queryUtility(IRAMCache)
    if util is not None:
        util.invalidateAll()


def ensure_folder_ordering():
    old_order_key = DefaultOrdering.ORDER_KEY
    logger = logging.getLogger("cpskin.policy")
    portal_catalog = api.portal.get_tool("portal_catalog")
    brains = portal_catalog({"portal_type": "Folder"})
    for brain in brains:
        obj = brain.getObject()
        if obj and obj._ordering == "unordered":
            annotations = IAnnotations(obj)
            if old_order_key in annotations:
                # old order stuff remained in annotation and can breaks
                # objectIds() with missing old stored objects ids
                del annotations[old_order_key]
            obj.setOrdering(u"")
            order = obj.getOrdering()
            for id in obj._tree:
                if id not in order._order():
                    order.notifyAdded(id)
            logger.info("Fixed ordering for folder : {}".format(brain.getURL()))
