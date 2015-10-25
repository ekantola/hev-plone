from zope.component import getMultiAdapter
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from AccessControl import getSecurityManager
from Acquisition import aq_inner

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from Products.CMFPlone import PloneMessageFactory as _

class IMyLoginPortlet(IPortletDataProvider):
    """A portlet which can render a login form.
    """

class Assignment(base.Assignment):
    implements(IMyLoginPortlet)

    title = _(u'label_log_in', default=u'Log in')

class Renderer(base.Renderer):

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)

        self.membership = getToolByName(self.context, 'portal_membership')

        self.context_state = getMultiAdapter((context, request), name=u'plone_context_state')
        self.portal_state = getMultiAdapter((context, request), name=u'plone_portal_state')
        self.pas_info = getMultiAdapter((context, request), name=u'pas_info')

    def show(self):
        return True

    @property
    def available(self):
        return True

    def login_form(self):
        return '%s/login_form' % self.portal_state.portal_url()

    def logout(self):
        return '%s/logout' % self.portal_state.portal_url()

    @memoize
    def update(self):
        context = aq_inner(self.context)

        context_state = getMultiAdapter((context, self.request),
                                        name=u'plone_context_state')

        sm = getSecurityManager()
        self.user_actions = context_state.actions('user')
        self.anonymous = self.portal_state.anonymous()
        self.navigation_root_url = self.portal_state.portal_url()

        if not self.anonymous:
            member = self.portal_state.member()
            userid = member.getId()

            if sm.checkPermission('Portlets: View dashboard', context):
                self.homelink_url = "%s/dashboard" % self.navigation_root_url
            else:
                self.homelink_url = "%s/personalize_form" % (
                                        self.navigation_root_url)

            membership = getToolByName(context, 'portal_membership')
            member_info = membership.getMemberInfo(userid)
            # member_info is None if there's no Plone user object, as when
            # using OpenID.
            if member_info:
                fullname = member_info.get('fullname', '')
            else:
                fullname = None
            if fullname:
                self.user_name = fullname
            else:
                self.user_name = userid


    render = ViewPageTemplateFile('mylogin.pt')

class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
