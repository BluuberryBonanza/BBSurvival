"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from protocolbuffers.Localization_pb2 import LocalizedString


class BBSimDialog:
    """BBSimDialog(\
        mod_identity,\
        title,\
        description\
    )

    A dialog for displaying Sims to choose from.

    :param mod_identity: The identity of the mod that owns this dialog.
    :type mod_identity: BBModIdentity
    :param title: The title to show in the dialog.
    :type title: BBLocalizedStringData
    :param description: The description to show in the dialog.
    :type description: BBLocalizedStringData
    """
    def __init__(
        self,
        mod_identity: BBModIdentity,
        title: BBLocalizedStringData,
        description: BBLocalizedStringData,
    ):
        self._mod_identity = mod_identity
        self._title = title.localize()
        self._description = description.localize()

    @property
    def mod_identity(self) -> BBModIdentity:
        return self._mod_identity

    @property
    def title(self) -> LocalizedString:
        return self._title

    @property
    def description(self) -> LocalizedString:
        return self._description
