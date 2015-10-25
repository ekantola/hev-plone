# -*- coding: UTF-8 -*-

import unittest

import time
from datetime import datetime
from DateTime.DateTime import DateTime # Zope 2's DateTime
from plone.i18n.normalizer import IDNormalizer

from Products.PakkiLayout.scripts.pakki import Pakki

def toZopeDateTime(dt):
    return DateTime(time.mktime(dt.timetuple()))

class _MockEvent:
    portal_type = "Event"
    def __init__(self, start):
        """Convert the more convenient Python datetime internally into a Zope DateTime"""
        self.start = toZopeDateTime(start)

class TestPakki(unittest.TestCase):
    def setUp(self):
        self.pakki = Pakki(context=None, request=None)

    def test_getEventsArrangedYearlyAndMonthly(self):
        now = datetime(2009, 5, 21)
        today_event = _MockEvent(now)
        tomorrow_event = _MockEvent(datetime(2009, 5, 22))
        last_month_event = _MockEvent(datetime(2009, 4, 3))
        next_year_event = _MockEvent(datetime(2010, 6, 12))

        expected = [{'year': 2009, 'months': [
            {'month': 1, 'events': []},
            {'month': 2, 'events': []},
            {'month': 3, 'events': []},
            {'month': 4, 'events': [last_month_event]},
            {'month': 5, 'events': [today_event, tomorrow_event]},
            {'month': 6, 'events': []},
            {'month': 7, 'events': []},
            {'month': 8, 'events': []},
            {'month': 9, 'events': []},
            {'month': 10, 'events': []},
            {'month': 11, 'events': []},
            {'month': 12, 'events': []},
        ]},
        {'year': 2010, 'months': [
            {'month': 1, 'events': []},
            {'month': 2, 'events': []},
            {'month': 3, 'events': []},
            {'month': 4, 'events': []},
            {'month': 5, 'events': []},
            {'month': 6, 'events': [next_year_event]},
            {'month': 7, 'events': []},
            {'month': 8, 'events': []},
            {'month': 9, 'events': []},
            {'month': 10, 'events': []},
            {'month': 11, 'events': []},
            {'month': 12, 'events': []},
        ]}]

        events = [last_month_event, today_event, tomorrow_event, next_year_event]
        year_list = self.pakki.getEventsArrangedYearlyAndMonthly(events)
        self.assertEquals(expected, year_list)

    def test_formatCalendarDateRange(self):
        start = toZopeDateTime(datetime(2009, 5, 23, 8, 0))
        endSame = start
        endSameDay = toZopeDateTime(datetime(2009, 5, 23, 9, 5))
        endNextDay = toZopeDateTime(datetime(2009, 5, 24, 9, 5))
        endNextMonth = toZopeDateTime(datetime(2009, 6, 23, 9, 5))
        endNextYear = toZopeDateTime(datetime(2010, 5, 23, 9, 5))
        noTime = toZopeDateTime(datetime(2010, 5, 23))

        self.assertEquals(u"la 23.5. 8:00",
                          self.pakki.formatCalendarDateRange(start, endSame))

        self.assertEquals(u"la 23.5. 8:00–9:05",
                          self.pakki.formatCalendarDateRange(start, endSameDay))

        self.assertEquals(u"la 23.5. – su 24.5.",
                          self.pakki.formatCalendarDateRange(start, endNextDay))

        self.assertEquals(u"la 23.5. – ti 23.6.",
                          self.pakki.formatCalendarDateRange(start, endNextMonth))

        self.assertEquals(u"la 23.5.2009 – su 23.5.2010",
                          self.pakki.formatCalendarDateRange(start, endNextYear))

        self.assertEquals(u"su 23.5.",
                          self.pakki.formatCalendarDateRange(noTime, noTime))

    def test_chooseYearClass(self):
        gone = 'calendar_event_gone'
        notGone = ''
        now = DateTime(2009, 5, 24)

        self.assertEquals(gone, self.pakki.chooseYearClass(2008, now))
        self.assertEquals(notGone, self.pakki.chooseYearClass(2009, now))

    def test_chooseMonthClass(self):
        gone = 'calendar_event_gone'
        notGone = ''
        now = DateTime(2009, 5, 24)

        self.assertEquals(gone, self.pakki.chooseMonthClass((2009, 4), now))
        self.assertEquals(gone, self.pakki.chooseMonthClass((2008, 12), now))
        self.assertEquals(notGone, self.pakki.chooseMonthClass((2009, 5), now))
        self.assertEquals(notGone, self.pakki.chooseMonthClass((2010, 1), now))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPakki))
    return suite
