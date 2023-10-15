"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import services
from bbsurvival.bb_lib.utils.bb_zone_modifier_utils import BBZoneModifierUtils
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_end_event import BBOnZoneLoadEndEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from event_testing.results import TestResult
from objects.components.statistic_component import StatisticComponent
from sims4.resources import Types


@BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadEndEvent)
def _bbs_add_off_the_grid_on_zone_load(event: BBOnZoneLoadEndEvent):
    zone_modifier_id = 206665  # zoneModifier_lotTrait_OffTheGrid
    BBZoneModifierUtils.add_zone_modifier_to_current_lot(zone_modifier_id)

    # We set the power and water to -1 if it was below that because we don't want it to drop too far.
    current_zone_id = services.current_zone_id()
    zone = services.get_zone(current_zone_id)
    lot = zone.lot
    import objects.components.types
    statistic_component: StatisticComponent = None if lot is None else lot.get_component(
        objects.components.types.STATISTIC_COMPONENT)
    instance_manager = services.get_instance_manager(Types.STATISTIC)
    statistic_power = instance_manager.get(233027)  # commodity_Utilities_Power
    current_power_amount = statistic_component.get_stat_value(statistic_power)
    if current_power_amount < -1:
        statistic_component.set_stat_value(statistic_power, -1.0)

    statistic_water = instance_manager.get(233028)  # commodity_Utilities_Water
    current_water_amount = statistic_component.get_stat_value(statistic_water)
    if current_water_amount < -1:
        statistic_component.set_stat_value(statistic_water, -1.0)
    return TestResult.TRUE
