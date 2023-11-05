"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.interactions.classes.bb_super_interaction import BBSuperInteraction
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from lightonfire.mod_identity import ModIdentity


class LOFLightOnFireInteraction(BBSuperInteraction):
    """Light On Fire."""

    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'lof_light_on_fire'
