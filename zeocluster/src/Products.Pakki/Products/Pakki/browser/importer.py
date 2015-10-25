# -*- coding: utf-8 -*-
'''
Created on 17.10.2009

@author: ekan
'''

import sys
import re

from Products.Five.browser import BrowserView
from plone.i18n.normalizer.interfaces import IURLNormalizer
from zope.component import queryUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from DateTime.DateTime import DateTime, DateTimeError # Zope 2's DateTime

DATE_PATTERN = re.compile('^(\d{1,2})\.((\d{1,2})\.(\d{4})?)?$')
TIME_PATTERN = re.compile('^(\d{1,2})((\.|:)(\d{2}))?$')

class WrapperException(Exception):
    def __init__(self, exception):
        self.exception = exception
    
    def __str__(self):
        return '%s: %s' % (self.exception.__class__, self.exception)

class ImportEventsView(BrowserView):
    '''
    ATEvent importer view
    '''
    template = ViewPageTemplateFile('import_events.pt')

    def __init__(self, context, request):
        self.__parent__ = context
        super(BrowserView, self).__init__(context, request)

    def __call__(self):
        data = self.request.form.get('data')
        self.imported = []
        if data:
            self._import(data.decode('utf-8').split('\n'))
        return self.template()

    def _import(self, lines):
         for line in lines:
             tokens = line.split('\t')
             if len(tokens) != 2:
                 continue
             
             datetimeStr, title = tokens
             event = self.quickAddCalendarEvent(datetimeStr, title)
             if event:
                 self.imported.append(event)

             #except Exception, e:
             #    raise WrapperException(e), None, sys.exc_info()[2]
    
    def get_imported(self):
        return self.imported

    def getDateTimeFiParts(self, datetimeStr):
        parts = re.split('\s+', datetimeStr.strip(), 2)
        if (len(parts) == 1):
            parts += (None,)
        left, right = parts
        
        match = re.match(DATE_PATTERN, left)
        if (match is None):
            if (right):
                return (None,)*5
            else:
                right = left
                day = month = year = None
        else:
            day, mon_yr_group, month, year = match.groups()
        
        hour = minute = None
        if (right):
            match = re.match(TIME_PATTERN, right)
            if (match is None):
                return (None,)*5
            hour, minute_group, time_sep, minute = match.groups()
        
        return (year, month, day, hour, minute)

    def parseDateTimeFi(self, datetimeStr, currentYear=DateTime().year()):
        if not isinstance(datetimeStr, basestring):
            raise ValueError('datetimeStr must be a string')
        
        year, month, day, hour, minute = self.getDateTimeFiParts(datetimeStr)
        if (year is None):
            year = currentYear
        
        try:
            if (hour is None):
                hour = minute = 0
                
            return DateTime(int(year), int(month), int(day), int(hour), int(minute or 0))
        except (DateTimeError, TypeError):
            return None
    
    def parseDateTimeRangeFi(self, datetimeRangeStr, currentYear=DateTime().year()):
        if not isinstance(datetimeRangeStr, basestring):
            raise ValueError('datetimeRangeStr must be a string')
        
        parts = datetimeRangeStr.split('-', 2)
        if (len(parts) == 1):
            return self.parseDateTimeFi(parts[0], currentYear)
        
        year, month, day, hour, minute = self.getDateTimeFiParts(parts[0])
        year2, month2, day2, hour2, minute2 = self.getDateTimeFiParts(parts[1])
        if (not (year or year2)):
            year = year2 = currentYear

        try:
            if (hour is None and hour2 is None):
                hour = hour2 = minute = minute2 = 0
                
            dt = DateTime(int(year or year2), int(month or month2), int(day or day2),
                          int(hour or hour2), int(minute or minute2 or 0))
            dt2 = DateTime(int(year2 or year), int(month2 or month), int(day2 or day),
                           int(hour2 or hour), int(minute2 or minute or 0))
            
            return (dt, dt2)
        except (DateTimeError, TypeError):
            return None
    
    def quickAddCalendarEvent(self, datetimeStr, title, normalizer=None):
        '''Adding an event with Clouseau:
        
        from Products.Pakki.browser.importer import ImportEventsView
        iev=ImportEventsView(portal, None)
        e=iev.quickAddCalendarEvent('9.9. 18', 'Äyh öh!'.decode('utf-8')); print "%s '%s', '%s'-'%s'" % (e.id, e.title.encode('utf-8'), e.startDate, e.endDate)
        transaction_manager.commit()
        '''
        
        datetime = self.parseDateTimeRangeFi(datetimeStr)
        if datetime == None:
            raise ValueError('Invalid datetime format: "%s"' % datetimeStr)
        if len(str(title.encode('utf-8')).strip()) == 0:
            raise ValueError('Title may not be empty')
        
        if isinstance(datetime, DateTime):
            startDate = endDate = datetime
            if (startDate.hour()!=0 or startDate.minute()!=0):
                endDate += 0.125 # = 1 day/8 = 3 hours
        else:
            startDate, endDate = datetime

        normalizer = normalizer or queryUtility(IURLNormalizer)
        id_base = normalizer.normalize(title, locale='fi')
        id = id_base
        i = 1
        unique = False
        
        # XXX This is not thread safe
        while (id in self.context.keys()): # find a non-conflicting id
            id = '%s-%i' % (id_base, i)
            i += 1
        
        self.context.invokeFactory('Event', id=id, title=title, startDate=startDate, endDate=endDate)
        return self.context.get(id)
