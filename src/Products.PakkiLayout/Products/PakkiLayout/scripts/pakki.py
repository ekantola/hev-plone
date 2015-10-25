# -*- coding: UTF-8 -*-

'''
Created on 14.5.2009

This is for the wrapper view "@@pakki", to enable access to the Pakki methods to various
other views. There is probably a better way for doing this, but this works for now.

@author: ekan
'''

import re

from zope.interface import Interface
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.browser.search import PASSearchView

from DateTime.DateTime import DateTime, DateTimeError # Zope 2's DateTime

# TODO Get rid of these and use translation_service somehow
_weekday_names_abbr_fi = (u'su', u'ma', u'ti', u'ke', u'to', u'pe', u'la')
def _getWeekdayAbbrevFi(zopeDateTime):
    return _weekday_names_abbr_fi[zopeDateTime.dow()]

_month_names_fi = map(lambda x: x+'kuu',
                      (u'Tammi', u'Helmi', u'Maalis', u'Huhti', u'Touko', u'Kesä',
                       u'Heinä', u'Elo', u'Syys', u'Loka', u'Marras', u'Joulu'))

def _compareEvents(a, b):
    if a.start == b.start:
        ret = 0
    elif a.start > b.start:
        ret = 1
    else:
        ret = -1
    return ret

# All methods of Pakki that are usable e.g. in templates should be declared here.
class IPakki(Interface):
    def searchUsersByRequestWithGroupSupport(self, request, sort_by):
        """Like IPASSearchView.searchUsersByRequest, but can also find users according to their groups.

        Interprets the request parameter 'groups' and filters the users based on that.
        """

    def getViewableGroups(self, member):
        """Return the group names (excluding AuthenticatedUsers) of a member concatenated and joined with commas."""

    # FIXME Workaround. This might be a security hole!
    # Update 2009-05-21 ekantola: fortunately not so much, because only users with the Manager role seem to be able to
    # directly access (context)/@@pakki .
    def getUserById(self, id):
        """Wrapper for acl_users.getUserById."""

    def getEventsArrangedYearlyAndMonthly(self, objects):
        """Return a structure containing all the events in the 'objects' list. Example:

        [{'year': 2009, 'months': [
            {'month': 4, 'events': [ATEvent('a'), ATEvent('b'), ...]},
            {'month': 5, 'events': [ATEvent('c'), ...]}
        ]},
        {'year': 2010, 'months': [
            {'month': 5, 'events': [ATEvent('d'), ...]}
        ]}]
        """

    def now(self):
        """Returns the current date and time as a Zope DateTime object"""

    def formatTimeForViewlet(self, start):
        """Returns time formatted for calendar-viewlet"""

    def formatCalendarDateRange(self, start, end):
        """Formats the event start and end dates in an intuitive Finnish style."""

    def chooseYearClass(self, year, referenceDate=DateTime()):
        """ """

    def chooseMonthClass(self, year_month, referenceDate=DateTime()):
        """ """

    def pGetFolderEvents(self):
        """ """

#    def parseDateTimeFi(self, datetimeStr):
#        """"""

#    def parseDateTimeRangeFi(self, datetimeStr):
#        """"""

#    def quickAddCalendarEvent(self, datetimeStr, title):
#        """"""

    def getMonthNameFi(self, month_nr):
        """ """

class Pakki(PASSearchView):
    implements(IPakki)

    def _userBelongsToGroupMatching(self, user_info, search_re):
        pas = getToolByName(self.context, 'acl_users')

        #self.context.plone_log('user_info = %s' % user_info)
        user = pas.getUserById(user_info['id'])
        if (user):
            for group_name in user.getGroupNames():
                if (search_re.search(group_name)):
                    return True
        return False

    def searchUsersByRequestWithGroupSupport(self, request, sort_by):
        criteria = self.extractCriteriaFromRequest(request)
        group_search_str = None
        if (criteria.has_key('groups')):
            group_search_str = criteria['groups']
            del criteria['groups']

        user_info_list = self.searchUsers(sort_by=sort_by, **criteria)

        if (group_search_str):
            #self.context.plone_log('group_search_str = "%s"; user_info_list = %s' % (group_search_str, user_info_list))

            # Problem: international characters and case insensitivity
            # See http://www.cmlenz.net/archives/2008/07/the-truth-about-unicode-in-python
            search_re = re.compile(group_search_str, re.IGNORECASE)
            user_info_list = filter(lambda x: self._userBelongsToGroupMatching(x, search_re), user_info_list)

        return user_info_list

    def getViewableGroups(self, member):
        return sorted(filter(lambda x: x!='AuthenticatedUsers', member.getGroups()))
        """Kaytetaan funktiota getGroups, jotta paastaisiin kasiksi myos group/email-kenttaan"""
        # return sorted(filter(lambda x: x!='AuthenticatedUsers', member.getGroupNames()))

    def getUserById(self, id):
        return getToolByName(self.context, 'acl_users').getUserById(id)

    def getEventsArrangedYearlyAndMonthly(self, objects):
        prev_year = None
        prev_month = None
        curr_month = None
        year_list = list()

        for o in objects:
            if (o.portal_type not in ('Event', 'PakkiEvent')):
                continue

            curr_year = o.start.year()
            if (curr_year != prev_year):
                prev_month = None
                curr_year_months = map(lambda x: dict({'month': x, 'events': list()}), range(1, 13))
                year_list.append({'year': curr_year, 'months': curr_year_months})
                prev_year = curr_year

            curr_month = o.start.month()
            if (curr_month != prev_month):
                curr_month_events = list()
                curr_year_months[curr_month-1]['events'] = curr_month_events
                prev_month = curr_month

            curr_month_events.append(o)

        return year_list

    def now(self):
        return DateTime()

    def formatCalendarDateRange(self, start, end):
        s = None
        if (start.year() != end.year()):
            s = u"%s %u.%u.%u – %s %u.%u.%u" % (_getWeekdayAbbrevFi(start), start.day(), start.month(), start.year(),
                                                _getWeekdayAbbrevFi(end), end.day(), end.month(), end.year())

        elif (start.dayOfYear() != end.dayOfYear()):
            s = u"%s %u.%u. – %s %u.%u." % (_getWeekdayAbbrevFi(start), start.day(), start.month(),
                                            _getWeekdayAbbrevFi(end), end.day(), end.month())

        elif (start.hour()*100+start.minute() != end.hour()*100+end.minute()):
            s = u"%s %u.%u. %u:%02u–%u:%02u" % (_getWeekdayAbbrevFi(start),
                                                start.day(), start.month(), start.hour(), start.minute(),
                                                end.hour(), end.minute())
        elif (start.hour()==0 and start.minute()==0):
            s = u"%s %u.%u." % (_getWeekdayAbbrevFi(start), start.day(), start.month())
        else:
            s = u"%s %u.%u. %u:%02u" % (_getWeekdayAbbrevFi(start), start.day(), start.month(),
                                        start.hour(), start.minute())

        return s

    def formatTimeForViewlet(self, start):
        return u"%u.%u.%u %u:%02u" % (start.day(), start.month(), start.year(),
                                       start.hour(), start.minute())

    def chooseYearClass(self, year, referenceDate=DateTime()):
        if (year < referenceDate.year()):
            return 'calendar_event_gone'
        else:
            return ''

    def chooseMonthClass(self, year_month, referenceDate=DateTime()):
        if (year_month[0] < referenceDate.year() or
            (year_month[0] == referenceDate.year() and year_month[1] < referenceDate.month())):

            return 'calendar_event_gone'
        else:
            return ''

    def pGetFolderEvents(self):
        portal_url = getToolByName(self.context, "portal_url")
        portal = portal_url.getPortalObject()

        catalog = self.context.portal_catalog.aq_inner

        # The form and other are what really matters
        contentFilter = dict(getattr(self.context.REQUEST, 'form', {}))
        contentFilter.update(dict(getattr(self.context.REQUEST, 'other', {})))

        path = dict()
        path['query'] = '/tapahtumakalenteri/'
        path['depth'] = 1
        try:
            contentFilter.set('path', path)
        except AttributeError:
            contentFilter['path'] = path

        contentFilter['portal_type']='Event'
        contentFilter['review_state']='published'

        print contentFilter

        contents = catalog.queryCatalog(contentFilter, show_all=1)
        objects = contents
        print contents
        print objects

        events = list()
        for o in objects:
            if o.portal_type != 'Event':
                print "Something's wrong."
                continue
            if o.start > DateTime():
                events.append(o)
        print events
        events.sort(_compareEvents)
        del events[4:len(events)]
        return events;

    def getMonthNameFi(self, month_nr):
        """XXX This one should not be needed. Use translation_service instead."""
        return _month_names_fi[month_nr - 1]
