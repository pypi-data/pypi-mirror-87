from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.table.helper import readable_date_time_text
from ftw.testbrowser import browsing
from izug.refegovservice.testing import IZUG_REFEGOVSERVICE_FUNCTIONAL_TESTING
from unittest import TestCase
import transaction


class TestOverview(TestCase):

    layer = IZUG_REFEGOVSERVICE_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestOverview, self).setUp()

        self.to_reference = create(Builder('document').titled(u'B\xe4m'))
        self.folder = create(Builder('folder'))

        self.modification_date = DateTime()
        self.leistung1 = create(Builder('egov service')
                                .titled(u'Z Leistung')
                                .within(self.folder)
                                .having(orgunit=self.to_reference,
                                        modificationDate=self.modification_date))
        self.leistung2 = create(Builder('egov service')
                                .titled(u'A Leistung')
                                .within(self.folder)
                                .having(orgunit=self.to_reference,
                                        modificationDate=self.modification_date))

    @browsing
    def test_overview_lists_services_sorted_as_table(self, browser):

        browser.login().visit(self.folder, view='egovleistung_overview')

        self.assertEquals(
            [['Title', 'OrgUnit', 'Modified'],
             ['A Leistung', u'B\xe4m', readable_date_time_text(
                 None, self.modification_date)],
             ['Z Leistung', u'B\xe4m', readable_date_time_text(
                 None, self.modification_date)]],
            browser.css('table.listing').first.lists())

    @browsing
    def test_overview_lists_services_does_not_break_if_orgunit_is_deleted(self, browser):

        self.to_reference.aq_parent.manage_delObjects(ids=[self.to_reference.id])
        transaction.commit()

        browser.login().visit(self.folder, view='egovleistung_overview')

        self.assertEquals(
            [['Title', 'OrgUnit', 'Modified'],
             ['A Leistung', u'', readable_date_time_text(
                 None, self.modification_date)],
             ['Z Leistung', u'', readable_date_time_text(
                 None, self.modification_date)]],
            browser.css('table.listing').first.lists())

    @browsing
    def test_overview_lists_nested_services_sorted_as_table(self, browser):
        sub_folder = create(Builder('folder').within(self.folder))

        create(Builder('egov service')
               .titled(u'B Leistung')
               .within(sub_folder)
               .having(orgunit=self.to_reference,
                       modificationDate=self.modification_date))

        browser.login().visit(self.folder, view='egovleistung_overview')

        self.assertEquals(
            [['Title', 'OrgUnit', 'Modified'],
             ['A Leistung', u'B\xe4m', readable_date_time_text(
                 None, self.modification_date)],
             ['B Leistung', u'B\xe4m', readable_date_time_text(
                 None, self.modification_date)],
             ['Z Leistung', u'B\xe4m', readable_date_time_text(
                 None, self.modification_date)]],
            browser.css('table.listing').first.lists())

    @browsing
    def test_services_are_linked(self, browser):

        browser.login().visit(self.folder, view='egovleistung_overview')

        self.assertEquals(
            self.leistung2.absolute_url(),
            browser.css('table.listing tr a').first.attrib['href'])

    @browsing
    def test_orgunits_are_linked(self, browser):

        browser.login().visit(self.folder, view='egovleistung_overview')

        self.assertEquals(
            self.to_reference.absolute_url(),
            browser.css('table.listing tr a')[1].attrib['href'])
