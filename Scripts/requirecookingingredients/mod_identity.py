"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity


class ModIdentity(BBModIdentity):
    _FILE_PATH: str = str(__file__)

    @property
    def mod_name(self) -> str:
        return 'RequireCookingIngredients'

    @property
    def mod_author(self) -> str:
        return 'BluuberryBonanza'

    @property
    def module_namespace(self) -> str:
        return 'requirecookingingredients'

    @property
    def script_file_path(self) -> str:
        return self.__class__._FILE_PATH

    @property
    def mod_version(self) -> str:
        return '1.0'
