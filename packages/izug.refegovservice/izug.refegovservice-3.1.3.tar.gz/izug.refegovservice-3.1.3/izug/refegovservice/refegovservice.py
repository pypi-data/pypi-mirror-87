from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from izug.refegovservice.config import PROJECTNAME
from izug.refegovservice.interfaces import IRefEgovService
from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.base import ATCTContent
from zope.interface import implements


schema = atapi.Schema((
    atapi.ReferenceField(
        'referencedService',
        required=True,
        relationship='pointstoservice',
        allowed_types=('EgovLeistung', ),
        widget=ReferenceBrowserWidget(
            label='Service Referenz',
            default_search_index='Title'
        ),
    ),
),
)


RefEgovServiceSchema = schemata.ATContentTypeSchema.copy() + schema.copy()
RefEgovServiceSchema['description'].widget.visible = -1
schemata.finalizeATCTSchema(RefEgovServiceSchema, folderish=0)


class RefEgovService(ATCTContent):
    """
    """

    schema = RefEgovServiceSchema

    implements(IRefEgovService)


atapi.registerType(RefEgovService, PROJECTNAME)
