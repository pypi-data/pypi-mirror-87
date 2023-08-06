# -*- coding: utf-8 -*-
from ftw.referencewidget.sources import DefaultSelectable
from ftw.referencewidget.sources import ReferenceObjSourceBinder
from ftw.referencewidget.widget import ReferenceWidgetFactory
from izug.refegovservice.interfaces import IEGovService
from plone.app.textfield import RichText
from plone.autoform import directives as form
from plone.dexterity.content import Item
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implements

from izug.refegovservice import _
try:
    from plone.app.dexterity import MessageFactory as DXMF
except ImportError:
    from plone.app.dexterity import _ as DXMF


class FilterByPathSelectable(DefaultSelectable):

    def is_selectable(self):
        """ Allow to reference any path"""
        return True


class IEGovServiceSchema(model.Schema):
    """ Marker interface and Dexterity Python Schema for EGovService
    """
    # Copy IBasic behavior to change description title to 'description'!
    title = schema.TextLine(
        title=DXMF(u'label_title', default=u'Title'),
        required=True
    )

    description = schema.Text(
        title=DXMF(u'label_description', default=u'Description'),
        description=DXMF(
            u'help_description',
            default=u'Used in item listings and search results.'
        ),
        required=False,
        missing_value=u'',
    )

    form.order_before(description='*')
    form.order_before(title='*')

    form.omitted('title', 'description')
    form.no_omit(IEditForm, 'title', 'description')
    form.no_omit(IAddForm, 'title', 'description')

    summary = RichText(
        title=_(u'summary', default=u'Summary'),
        required=False
    )

    generalinformation = RichText(
        title=_(u'generalinformation'),
        required=False
    )

    precondition = RichText(
        title=_(u'precondition'),
        required=False
    )

    procedure = RichText(
        title=_(u'procedure'),
        required=False
    )

    forms = RichText(
        title=_(u'forms'),
        required=False
    )

    requireddocuments = RichText(
        title=_(u'requireddocuments'),
        required=False
    )

    result = RichText(
        title=_(u'result'),
        required=False
    )

    cost = RichText(
        title=_(u'cost'),
        required=False
    )

    legalbases = RichText(
        title=_(u'legalbases'),
        required=False
    )

    additionalinformation = RichText(
        title=_(u'additionalinformation'),
        required=False
    )

    annotations = RichText(
        title=_(u'annotations'),
        required=False
    )

    address = RichText(
        title=_(u'address'),
        required=False,
    )

    form.widget(orgunit=ReferenceWidgetFactory)
    orgunit = RelationChoice(
        title=_(u'orgunit', default=u'OrgUnit'),
        required=False,
        source=ReferenceObjSourceBinder(
            selectable_class=FilterByPathSelectable),
        default=None,
    )


class EGovService(Item):
    """
    """
    implements(IEGovService)
