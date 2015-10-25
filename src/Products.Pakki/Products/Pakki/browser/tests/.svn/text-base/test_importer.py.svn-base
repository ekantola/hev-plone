# -*- coding: UTF-8 -*-

import unittest

from DateTime.DateTime import DateTime # Zope 2's DateTime
from plone.i18n.normalizer import URLNormalizer

import Products.Pakki.browser.importer as importer

class _MockContext:
    def __init__(self):
        self.ids = {}
    
    def __getitem__(self, x):
        return self.ids[x]
    
    def invokeFactory(self, type, **args):
        self.type = type
        self.args = args
        self.ids[args['id']] = True 

class _MockRequest:
    def __init__(self):
        self.form = {'data': 'foo'}

class TestImportEventsView(unittest.TestCase):
    def setUp(self):
        self.import_events_view = importer.ImportEventsView(context=_MockContext(), request=_MockRequest())
        importer.queryUtility = lambda x: URLNormalizer()

    def test_parseDateTimeFi(self):
        self.assertEquals(None, self.import_events_view.parseDateTimeFi('foobarbaz'))
        self.assertEquals(None, self.import_events_view.parseDateTimeFi('1. 13:30', 2009))
        self.assertEquals(None, self.import_events_view.parseDateTimeFi('1.5. 13:', 2009))

        self.assertEquals(DateTime(2009, 5, 1, 13, 30), self.import_events_view.parseDateTimeFi('1.5.2009 13:30 ', 2009))
        self.assertEquals(DateTime(2009, 5, 1, 2, 30), self.import_events_view.parseDateTimeFi(' 1.5. 2.30', 2009))
        self.assertEquals(DateTime(2009, 5, 1, 2, 0), self.import_events_view.parseDateTimeFi(' 01.05. 02 ', 2009))
        self.assertEquals(None, self.import_events_view.parseDateTimeFi('31.6.2009 13:30', 2009))

        self.assertEquals(DateTime(2009, 5, 1), self.import_events_view.parseDateTimeFi('1.5.2009', 2009))
        self.assertEquals(DateTime(2009, 5, 1), self.import_events_view.parseDateTimeFi('1.5.', 2009))

    def test_parseDateTimeRangeFi(self):
        self.assertEquals(None, self.import_events_view.parseDateTimeRangeFi('1.-3. 13:30', 2009))
        self.assertEquals((DateTime(2009, 5, 1, 13, 30), DateTime(2009, 5, 1, 15, 30)),
                          self.import_events_view.parseDateTimeRangeFi('1.5.2009 13:30 -15.30', 2009))
        self.assertEquals((DateTime(2009, 5, 1), DateTime(2009, 5, 3)),
                          self.import_events_view.parseDateTimeRangeFi('1.5.-3.5.', 2009))
        self.assertEquals((DateTime(2009, 5, 1), DateTime(2009, 5, 3)),
                          self.import_events_view.parseDateTimeRangeFi('1.- 3.5.2009', 2009))

        self.assertEquals(None, self.import_events_view.parseDateTimeRangeFi('1.-3. 13:30', 2009))
        self.assertEquals((DateTime(2009, 5, 1, 13, 30), DateTime(2009, 5, 1, 15, 30)),
                          self.import_events_view.parseDateTimeRangeFi('1.5.2009 13:30 -15.30', 2009))
        self.assertEquals((DateTime(2009, 5, 1, 13, 30), DateTime(2009, 5, 3, 13, 30)),
                          self.import_events_view.parseDateTimeRangeFi('1.5.-3.5. 13:30', 2009))
        self.assertEquals((DateTime(2009, 5, 1, 13, 30), DateTime(2009, 5, 3, 13, 30)),
                          self.import_events_view.parseDateTimeRangeFi('1.- 3.5.2009 13:30', 2009))

    def test_quickAddCalendarEvent(self):
        new_obj = self.import_events_view.quickAddCalendarEvent('9.9. 18', 'Koe')
        self.assertEquals(new_obj, True)
        
        self.assertEquals('Event', self.import_events_view.context.type)
        self.assertEquals({'id': 'koe', 'title': 'Koe',
                           'startDate': DateTime(2009, 9, 9, 18, 0), 'endDate': DateTime(2009, 9, 9, 21, 0)},
                          self.import_events_view.context.args)

    def test_quickAddCalendarEvent_invalidDatetimeFormat(self):
        try:
            self.import_events_view.quickAddCalendarEvent(None, 'Fail')
            self.fail('quickAddCalendarEvent() should not succeed with empty dates')
        except ValueError:
            pass

        try:
            self.import_events_view.quickAddCalendarEvent('xzvf grdy', 'Fail')
            self.fail('quickAddCalendarEvent() should not succeed with garbage dates')
        except ValueError:
            pass

        try:
            self.import_events_view.quickAddCalendarEvent('12.13.', 'Fail')
            self.fail('quickAddCalendarEvent() should not succeed with nonexistent dates')
        except ValueError:
            pass

        try:
            self.import_events_view.quickAddCalendarEvent('1.1.09', 'Fail')
            self.fail('quickAddCalendarEvent() should not succeed with incomplete dates')
        except ValueError:
            pass

    def test_quickAddCalendarEvent_emptyTitle(self):
        try:
            self.import_events_view.quickAddCalendarEvent('1.1.2001', '')
            self.fail('quickAddCalendarEvent() should not succeed with an empty title')
        except ValueError:
            pass

        try:
            self.import_events_view.quickAddCalendarEvent('1.1.2001', '  \t \n ')
            self.fail('quickAddCalendarEvent() should not succeed with a whitespace-only titles')
        except ValueError:
            pass

    def test_quickAddCalendarEvent_noTime(self):
        new_obj = self.import_events_view.quickAddCalendarEvent('9.9.', 'Koe')
        self.assertEquals(new_obj, True)
        
        self.assertEquals('Event', self.import_events_view.context.type)
        self.assertEquals({'id': 'koe', 'title': 'Koe',
                           'startDate': DateTime(2009, 9, 9), 'endDate': DateTime(2009, 9, 9)},
                          self.import_events_view.context.args)

    def test_quickAddCalendarEvent_duplicateId(self):
        self.test_quickAddCalendarEvent()
        
        new_obj = self.import_events_view.quickAddCalendarEvent('10.9. 18', 'Koe')
        self.assertEquals(new_obj, True)
        
        self.assertEquals({'id': 'koe-2', 'title': 'Koe',
                           'startDate': DateTime(2009, 9, 10, 18, 0), 'endDate': DateTime(2009, 9, 10, 21, 0)},
                          self.import_events_view.context.args)
        
        self.assertEquals({'koe': True, 'koe-2': True},
                          self.import_events_view.context.ids)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestImportEventsView))
    return suite
