from ftw.upgrade import UpgradeStep
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations


class RenameDescriptionField(UpgradeStep):
    """Rename description field.
    """

    def __call__(self):
        cat = getToolByName(self.portal, 'portal_catalog')
        results = cat({'portal_type': 'EgovLeistung'})
        for item in results:
            obj = item.getObject()
            annos = IAnnotations(obj)
            key = annos.get('Archetypes.storage.AnnotationStorage-description')
            if not key:
                continue
            value = key.getRaw()
            obj.getField('summary').set(obj, value)
