from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from izug.refegovservice import _
from izug.refegovservice.config import PROJECTNAME
from izug.refegovservice.interfaces import IEgovLeistung
from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.base import ATCTContent
from zope.interface import implements


schema = atapi.Schema((

    atapi.TextField(
        name='summary',
        searchable=True,
        storage=atapi.AnnotationStorage(),
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_input_type='text/html',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            rows=4,
            label=_(u'summary'),
            allow_file_upload=False,
        )
    ),

    atapi.TextField(
        name='generalinformation',
        searchable=True,
        storage=atapi.AnnotationStorage(),
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_input_type='text/html',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            rows=4,
            label=_(u'generalinformation'),
            allow_file_upload=False,
        )
    ),

    atapi.TextField(
        name='precondition',
        searchable=True,
        storage=atapi.AnnotationStorage(),
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_input_type='text/html',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            rows=4,
            label=_(u'precondition'),
            allow_file_upload=False,
        )
    ),

    atapi.TextField(
        name='procedure',
        searchable=True,
        storage=atapi.AnnotationStorage(),
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_input_type='text/html',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            rows=4,
            label=_(u'procedure'),
            allow_file_upload=False,
        )
    ),

    atapi.TextField(
        name='forms',
        searchable=True,
        storage=atapi.AnnotationStorage(),
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_input_type='text/html',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            rows=4,
            label=_(u'forms'),
            allow_file_upload=False,
        )
    ),

    atapi.TextField(
        name='requireddocuments',
        searchable=True,
        storage=atapi.AnnotationStorage(),
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_input_type='text/html',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            rows=4,
            label=_(u'requireddocuments'),
            allow_file_upload=False,
        )
    ),

    atapi.TextField(
        name='result',
        searchable=True,
        storage=atapi.AnnotationStorage(),
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_input_type='text/html',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            rows=4,
            label=_(u'result'),
            allow_file_upload=False,
        )
    ),

    atapi.TextField(
        name='cost',
        searchable=True,
        storage=atapi.AnnotationStorage(),
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_input_type='text/html',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            rows=4,
            label=_(u'cost'),
            allow_file_upload=False,
        )
    ),

    atapi.TextField(
        name='legalbases',
        searchable=True,
        storage=atapi.AnnotationStorage(),
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_input_type='text/html',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            rows=4,
            label=_(u'legalbases'),
            allow_file_upload=False,
        )
    ),

    atapi.TextField(
        name='additionalinformation',
        searchable=True,
        storage=atapi.AnnotationStorage(),
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_input_type='text/html',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            rows=4,
            label=_(u'additionalinformation'),
            allow_file_upload=False,
        )
    ),

    atapi.TextField(
        name='annotations',
        searchable=True,
        storage=atapi.AnnotationStorage(),
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_input_type='text/html',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            rows=4,
            label=_(u'annotations'),
            allow_file_upload=False,
        )
    ),

    atapi.TextField(
        name='address',
        searchable=True,
        storage=atapi.AnnotationStorage(),
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_input_type='text/html',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            label=_(u'address'),
            rows=5,
            allow_file_upload=False,
        ),
    ),

    atapi.ReferenceField(
        name='orgunit',
        storage=atapi.AnnotationStorage(),
        relationship='leistung_orgunit',
        widget=ReferenceBrowserWidget(
            label=_(u'orgunit'),
            default_search_index='Title',
            allow_browse=True,
        ),
    ),

),
)


EgovLeistungSchema = schemata.ATContentTypeSchema.copy() + schema.copy()
schemata.finalizeATCTSchema(EgovLeistungSchema, folderish=0)
EgovLeistungSchema.changeSchemataForField('language', 'default')


class EgovLeistung(ATCTContent):
    """
    """

    schema = EgovLeistungSchema

    implements(IEgovLeistung)


atapi.registerType(EgovLeistung, PROJECTNAME)
