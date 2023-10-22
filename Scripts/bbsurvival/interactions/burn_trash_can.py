"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import services
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.interactions.classes.bb_super_interaction import BBSuperInteraction
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from objects.game_object import GameObject
from scheduling import Timeline
from sims.sim_info import SimInfo


class BBSLightOnFireInteraction(BBSuperInteraction):
    """Light On Fire."""

    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'bbs_light_on_fire'
