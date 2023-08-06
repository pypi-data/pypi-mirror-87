from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from izug.refegovservice.testing import IZUG_REFEGOVSERVICE_FUNCTIONAL_TESTING
from plone.app.testing import login
from plone.app.textfield.value import RichTextValue
from unittest import TestCase


class TestCreation(TestCase):

    layer = IZUG_REFEGOVSERVICE_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestCreation, self).setUp()

        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

        self.leistung = create(Builder('egov service')
                               .titled(u'Leistung')
                               .having(description=u'The Description',
                                       generalinformation=RichTextValue('Some infos'),
                                       result=RichTextValue('A result')))
        self.refservice = create(Builder('ref egov service')
                                 .titled(u'Reference')
                                 .having(referencedService=self.leistung))

        self.leistungde = create(Builder('egov service')
                                 .titled(u'Leistung DE')
                                 .having(generalinformation=RichTextValue('Einige Infos'),
                                         result=RichTextValue('Ein Resultat'),
                                         language='de'))
        self.refservicede = create(Builder('ref egov service')
                                   .titled(u'Referenz')
                                   .having(referencedService=self.leistungde))

    def test_fti(self):
        self.assertIn(
            'izug.refegovservice.egovservice',
            self.portal.portal_types.objectIds()
        )
        self.assertIn(
            'izug.refegovservice.refegovservice',
            self.portal.portal_types.objectIds()
        )

    @browsing
    def test_description_is_not_rendered(self, browser):
        browser.login().visit(self.refservice)
        self.assertNotIn('The Description',
                         browser.css('h2'),
                         'Description should not be rendered.')

    @browsing
    def test_creation_render(self, browser):
        browser.login().visit(self.refservice)

        self.assertEquals('Leistung',
                          browser.css('.documentFirstHeading').first.text)

        fields = browser.css('h2')
        self.assertIn('A result',
                      fields.pop().parent().text)

        self.assertIn('Some infos',
                      fields.pop().parent().text)

    @browsing
    def test_correct_language_is_picked(self, browser):
        browser.login().visit(self.refservice)
        self.assertEquals('General Information',
                          browser.css('.webContent h2').first.text)

        browser.visit(self.leistung)
        self.assertEquals('General Information',
                          browser.css('.webContent h2').first.text)

        browser.visit(self.leistungde)
        self.assertEquals('Generelle Information',
                          browser.css('.webContent h2').first.text)

        browser.visit(self.refservicede)
        self.assertEquals('Generelle Information',
                          browser.css('.webContent h2').first.text)

    @browsing
    def test_byline_of_current_item_is_displayed_not_referenced_byline(self, browser):

        self.user2 = create(Builder('user')
            .named('Hugo', 'Boss')
            .with_email('hugo.boss@4teamwork.ch')
            .with_password('demo14')
            .with_roles('Manager'))

        self.leistung = create(Builder('egov service')
                         .titled(u'Leistung'))

        login(self.portal, self.user2.getUser().getName())

        self.refservice = create(Builder('ref egov service')
                           .titled(u'Referenz')
                           .having(referencedService=self.leistung))

        browser.login().visit(self.leistung)
        self.assertIn('test_user_1_', browser.contents)
        self.assertNotIn('Boss Hugo', browser.contents)

        browser.visit(self.refservice)
        self.assertIn('Boss Hugo', browser.contents)
