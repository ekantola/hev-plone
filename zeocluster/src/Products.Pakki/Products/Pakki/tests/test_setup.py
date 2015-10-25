# -*- coding: UTF-8 -*-

import unittest
from Products.CMFCore.utils import getToolByName

from Products.Pakki.tests.base import PakkiTestCase

class TestSetup(PakkiTestCase):
    def afterSetUp(self):
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.properties = getToolByName(self.portal, 'portal_properties')
        self.skins = getToolByName(self.portal, 'portal_skins')
        self.types = getToolByName(self.portal, 'portal_types')
        self.workflow = getToolByName(self.portal, 'portal_workflow')

    def test_portal_default_charset(self):
        self.assertEquals(u"utf-8", self.properties.site_properties.getProperty('default_charset'))

    def test_workflow_installed(self):
        self.assertTrue('pakki_workflow' in self.workflow.objectIds())

    def test_workflow_permissions_etc(self):
        self.fail("FIXME Write the tests! (Prerequisite: add a folder and set its default workflow)")

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
