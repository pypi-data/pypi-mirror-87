# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.publisher.browser import BrowserView


class CookiesPage(BrowserView):

    index = ViewPageTemplateFile('templates/cookies.pt')

    def __init__(self, context, request):
        super(CookiesPage, self).__init__(context, request)
        # self.city_name = api.portal.get_registry_record(
        #     'cpskin.core.interfaces.ICPSkinSettings.city_name')
        # portal = api.portal.get()
        # self.site_id = portal.getId()
