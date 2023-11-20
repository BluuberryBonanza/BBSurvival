"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.bb_lib.utils.bb_eco_lifestyle_utility_utils import BBEcoLifestyleUtilityUtils
from bbsurvival.bb_lib.utils.bb_zone_modifier_utils import BBZoneModifierUtils
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.prologue.bbs_prologue_data import BBSPrologueData
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_end_event import BBOnZoneLoadEndEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from zone import Zone


class _BBSLotChallenges:

    @classmethod
    def add_lot_challenges(cls, zone_id: int):
        zone_modifier_ids = (
            206665,  # zoneModifier_lotTrait_OffTheGrid (Off-the-grid)
            230867,  # zoneModifier_LotTrait_TrashUpdate (Reduce and Recycle)
            258836,  # zoneModifiers_lotTrait_RequiredIngredients (Simple Living)
        )
        for zone_modifier_id in zone_modifier_ids:
            BBZoneModifierUtils.add_zone_modifier(zone_id, zone_modifier_id)

        # We set the power and water to -1 if it was below that because we don't want it to drop too far.
        current_power_amount = BBEcoLifestyleUtilityUtils.get_power_level(zone_id)
        if current_power_amount < -1:
            BBEcoLifestyleUtilityUtils.set_power_level(zone_id, -1.0)

        current_water_amount = BBEcoLifestyleUtilityUtils.get_water_level(zone_id)
        if current_water_amount < -1:
            BBEcoLifestyleUtilityUtils.set_water_level(zone_id, -1.0)


@BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadEndEvent)
def _bbs_add_off_the_grid_on_zone_load(event: BBOnZoneLoadEndEvent):
    if not BBSPrologueData().is_mod_fully_active():
        def _add_lot_challenges(_zone: Zone):
            def _add():
                zone_id = _zone.id
                _BBSLotChallenges.add_lot_challenges(zone_id)
            return _add

        BBSPrologueData().register_on_activate(_add_lot_challenges(event.zone))
        return BBRunResult.TRUE

    _BBSLotChallenges.add_lot_challenges(event.zone.id)
    return BBRunResult.TRUE
