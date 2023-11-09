"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import services
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from situations.npc_hosted_situations import NPCHostedSituationService


@BBInjectionUtils.inject(ModIdentity(), NPCHostedSituationService, NPCHostedSituationService._start_welcome_wagon.__name__)
def _bbs_start_welcome_wagon(original, *_, **__):
    active_household = services.active_household()
    active_household.needs_welcome_wagon = False
    return
