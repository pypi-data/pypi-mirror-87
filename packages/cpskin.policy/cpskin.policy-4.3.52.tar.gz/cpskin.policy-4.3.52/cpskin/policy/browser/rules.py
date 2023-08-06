# -*- coding: utf-8 -*-
from plone import api
from plone.app.redirector.interfaces import IRedirectionStorage
from Products.Five import BrowserView
from zope.component import queryUtility


class RulesScriptView(BrowserView):

    def run(self):
        context = self.context
        redirect = queryUtility(IRedirectionStorage)
        currentPath = '/'.join(context.getPhysicalPath())
        newPath = redirect.get(currentPath, '')
        newObj = context.unrestrictedTraverse(newPath)
        api.content.transition(obj=newObj, transition='publish_and_hide')
        return True
