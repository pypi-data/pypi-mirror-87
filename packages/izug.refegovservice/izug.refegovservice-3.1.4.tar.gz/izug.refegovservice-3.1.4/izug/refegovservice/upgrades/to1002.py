from ftw.upgrade import UpgradeStep


class InstallEgovLeistung(UpgradeStep):

    def __call__(self):
        self.setup_install_profile(
            'profile-izug.refegovservice.upgrades:1002')
