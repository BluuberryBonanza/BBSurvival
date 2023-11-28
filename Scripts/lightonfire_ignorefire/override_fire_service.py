"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from broadcasters.broadcaster import Broadcaster
from lightonfire.mod_identity import ModIdentity
from services.fire_service import FireService


@BBInjectionUtils.inject(ModIdentity(), FireService, FireService._start_fire_situations.__name__)
def _lof_override_start_fire_situations(original, *_, **__):
    return


@BBInjectionUtils.inject(ModIdentity(), FireService, FireService._start_fire_brigade_situation.__name__)
def _lof_override_start_fire_brigade_situation(original, *_, **__):
    return


@BBInjectionUtils.inject(ModIdentity(), FireService, FireService.alert_all_sims.__name__)
def _lof_override_alert_all_sims(original, *_, **__):
    return


# @BBInjectionUtils.inject(ModIdentity(), FireService, 'fire_is_active')
def _lof_override_fire_is_active(original, *_, **__):
    return False


FireService.INTERACTION_UNAVAILABLE_DUE_TO_FIRE_TOOLTIP = lambda *_, **__: None


@BBInjectionUtils.inject(ModIdentity(), Broadcaster, Broadcaster.can_affect.__name__)
def _lof_override_broadcaster_can_effect(original, self, obj, *_, **__):
    fire_ids = (
        75066,  # broadcaster_Reaction_Fire
        178672,  # broadcaster_Fear_Pet_FireObject
        266543,  # broadcaster_Reaction_Fire_AnimalObjects
    )
    broadcaster_id = getattr(self, 'guid64', None)
    if broadcaster_id not in fire_ids:
        return original(self, obj, *_, **__)
    return False
