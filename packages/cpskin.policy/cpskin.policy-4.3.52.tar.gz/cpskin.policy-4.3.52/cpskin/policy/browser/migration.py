# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Acquisition import aq_parent
from collective.preventactions.interfaces import IPreventDelete
from collective.preventactions.interfaces import IPreventMoveOrRename
from OFS.interfaces import IOrderedContainer
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2Base
from Products.Five.browser import BrowserView
from plone import api
from plone.app.contenttypes.migration import dxmigration
from plone.app.folder.utils import timer
from plone.folder.interfaces import IOrdering
from time import strftime
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
import logging

logger = logging.getLogger("cpskin.policy")


class FolderishTypesMigrationView(BrowserView):
    """ Installs collective.folderishtypes and migrate existing contents """

    def mklog(self):
        """ Helper to prepend a time stamp to the output """
        write = self.request.RESPONSE.write

        def log(msg, level="info"):
            if level == "warn":
                logger.warn(msg)
            else:
                logger.info(msg)
            msg = "{0} {1}\n".format(strftime("%d/%m/%Y - %H:%M:%S"), msg)
            write(msg)

        return log

    def install_folderish_types(self):
        portal_setup = api.portal.get_tool("portal_setup")
        portal_setup.runAllImportStepsFromProfile(
            "profile-collective.folderishtypes.dx:default"
        )

    def fix_folderish_types(self):
        log = self.mklog()
        catalog = api.portal.get_tool("portal_catalog")
        ordering_nb = btree_nb = 0
        for brain in catalog():
            obj = brain.getObject()
            is_container = isinstance(obj, BTreeFolder2Base)
            if not is_container:
                continue
            if not IOrdering.providedBy(obj):
                alsoProvides(obj, IOrdering)
                obj.reindexObject(["object_provides"])
                ordering_nb += 1
            if obj._tree is None:
                BTreeFolder2Base._initBTrees(obj)
                btree_nb += 1
        log("{0} objects IOrdering interface have been fixed.".format(ordering_nb))
        log("{0} objects tree have been fixed.".format(btree_nb))

    def __call__(self):
        log = self.mklog()
        real = timer()

        self.install_folderish_types()
        log("collective.folderishtypes installed.")

        catalog = api.portal.get_tool("portal_catalog")
        catalog.clearFindAndRebuild()
        log("Portal catalog has been rebuilt.")

        changed_base_classes = [
            "plone.app.contenttypes.content.Document",
            "plone.app.contenttypes.content.NewsItem",
            "plone.app.contenttypes.content.Event",
        ]

        migrated = []
        not_migrated = []
        for brain in catalog():
            obj = brain.getObject()
            old_class_name = dxmigration.get_old_class_name_string(obj)
            if old_class_name in changed_base_classes:
                prevented_delete = prevented_move = False
                obj_id = obj.getId()
                parent = aq_parent(aq_inner(obj))
                if IPreventDelete.providedBy(obj):
                    prevented_delete = True
                    noLongerProvides(obj, IPreventDelete)
                if IPreventMoveOrRename.providedBy(obj):
                    prevented_move = True
                    noLongerProvides(obj, IPreventMoveOrRename)
                position_in_parent = None
                ordered = IOrderedContainer(parent, None)
                if ordered is not None:
                    position_in_parent = ordered.getObjectPosition(obj_id)
                if dxmigration.migrate_base_class_to_new_class(
                    obj, migrate_to_folderish=True
                ):
                    migrated.append(obj)
                    if position_in_parent is not None:
                        ordered.moveObject(obj_id, position_in_parent)
                    if prevented_delete:
                        alsoProvides(obj, IPreventDelete)
                    if prevented_move:
                        alsoProvides(obj, IPreventMoveOrRename)
                else:
                    not_migrated.append(obj)

        if migrated:
            log("{0} objects have been migrated.".format(len(migrated)))
        if not_migrated:
            log(
                "{0} objects have NOT been migrated.".format(len(not_migrated)),
                level="warn",
            )

        catalog.clearFindAndRebuild()
        log("Portal catalog has been rebuilt.")

        msg = "Processed folderish types migration in {0}.".format(real.next())
        log(msg)
