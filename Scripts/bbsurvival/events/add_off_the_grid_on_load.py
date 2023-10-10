"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.bb_lib.utils.bb_zone_modifier_utils import BBZoneModifierUtils
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_end_event import BBOnZoneLoadEndEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from event_testing.results import TestResult


@BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadEndEvent)
def _bbs_add_off_the_grid_on_zone_load(event: BBOnZoneLoadEndEvent):
    zone_modifier_id = 206665  # zoneModifier_lotTrait_OffTheGrid
    BBZoneModifierUtils.add_zone_modifier_to_current_lot(zone_modifier_id)
    return TestResult.TRUE
