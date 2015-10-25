from zope.interface import implements
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewlet

from Products.CMFCore.utils import getToolByName

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from DateTime.DateTime import DateTime # Zope 2's DateTime



class CalendarViewlet(BrowserView):
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        super(CalendarViewlet, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager


    def update(self):

        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        
        
    render = ViewPageTemplateFile('calendar_viewlet.pt')