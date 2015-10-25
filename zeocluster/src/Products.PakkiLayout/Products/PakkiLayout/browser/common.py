from zope.interface import implements
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewlet
from zope.deprecation.deprecation import deprecate

from AccessControl import getSecurityManager
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from urllib import quote_plus

from Products.CMFPlone.utils import log

class ViewletBase(BrowserView):
    """ Base class with common functions for link viewlets.
    """
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        super(ViewletBase, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager

    @property
    @deprecate("Use site_url instead. ViewletBase.portal_url will be removed in Plone 4")
    def portal_url(self):
        return self.site_url


    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()

    def render(self):
        # defer to index method, because that's what gets overridden by the template ZCML attribute
        return self.index()

    def index(self):
        raise NotImplementedError(
            '`index` method must be implemented by subclass.')

class GlobalSectionsViewlet(ViewletBase):
    index = ViewPageTemplateFile('sections.pt')

    def update(self):
        portal_tabs_view = getMultiAdapter((self.context, self.request),
                                           name='portal_tabs_view')
        self.portal_tabs = portal_tabs_view.topLevelTabs()

        selectedTabs = self.context.restrictedTraverse('selectedTabs')
        self.selected_tabs = selectedTabs('index_html',
                                          self.context,
                                          self.portal_tabs)
        self.selected_portal_tab = self.selected_tabs['portal']
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
