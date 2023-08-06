from ftw.upgrade import UpgradeStep
from ftw.upgrade.migration import InplaceMigrator
import os


class ArchetypesToDexterity(UpgradeStep):
    """Archetypes to dexterity.
    """

    def __call__(self):
        self.install_upgrade_profile()
        self.ensure_profile_installed('profile-plone.app.relationfield:default')

        if os.environ.get('IZUG_REFEGOVSERVICE_SKIP_DEXTERITY_MIGRATION', '').lower() == 'true':
            return

        self.migrate_egovservice()
        self.migrate_refegovservice()

    def migrate_egovservice(self):

        migrator = InplaceMigrator(
            new_portal_type='izug.refegovservice.egovservice',
            ignore_fields=('allowDiscussion', 'relatedItems'),
        )

        for obj in self.objects({'portal_type': 'EgovLeistung'},
                                'Migrate EgovLeistung to dexterity type '
                                'izug.refegovservice.egovservice'):
            migrator.migrate_object(obj)

    def migrate_refegovservice(self):

        migrator = InplaceMigrator(
            new_portal_type='izug.refegovservice.refegovservice',
            ignore_fields=('allowDiscussion', 'relatedItems'),
        )

        for obj in self.objects({'portal_type': 'RefEgovService'},
                                'Migrate RefEgovService to dexterity type '
                                'izug.refegovservice.refegovservice'):
            migrator.migrate_object(obj)
