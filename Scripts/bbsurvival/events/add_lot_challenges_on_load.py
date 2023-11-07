"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import services
from bbsurvival.bb_lib.utils.bb_eco_lifestyle_utility_utils import BBEcoLifestyleUtilityUtils
from bbsurvival.bb_lib.utils.bb_zone_modifier_utils import BBZoneModifierUtils
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_end_event import BBOnZoneLoadEndEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from event_testing.results import TestResult


@BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadEndEvent)
def _bbs_add_off_the_grid_on_zone_load(event: BBOnZoneLoadEndEvent):
    zone_modifier_ids = (
        206665,  # zoneModifier_lotTrait_OffTheGrid (Off-the-grid)
        230867,  # zoneModifier_LotTrait_TrashUpdate (Reduce and Recycle)
        258836,  # zoneModifiers_lotTrait_RequiredIngredients (Simple Living)
    )
    for zone_modifier_id in zone_modifier_ids:
        BBZoneModifierUtils.add_zone_modifier_to_current_lot(zone_modifier_id)

    # We set the power and water to -1 if it was below that because we don't want it to drop too far.
    current_zone_id = services.current_zone_id()
    current_power_amount = BBEcoLifestyleUtilityUtils.get_power_level(current_zone_id)
    if current_power_amount < -1:
        BBEcoLifestyleUtilityUtils.set_power_level(current_zone_id, -1.0)

    current_water_amount = BBEcoLifestyleUtilityUtils.get_water_level(current_zone_id)
    if current_water_amount < -1:
        BBEcoLifestyleUtilityUtils.set_water_level(current_zone_id, -1.0)
    return TestResult.TRUE
