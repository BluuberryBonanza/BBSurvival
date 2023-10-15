"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import services
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.mod_identity import ModIdentity
from objects.components.statistic_component import StatisticComponent
from sims.household_utilities.utilities_manager import ZoneUtilitiesManager, UtilityInfo
from sims.household_utilities.utility_types import Utilities
from sims4.commands import CommandType, Command
from sims4.resources import Types

log = BBLogRegistry().register_log(ModIdentity(), 'bbl_print_utilities')
log.enable()


@Command(
    'bbl.print_utilities',
    command_type=CommandType.Live
)
def _bbl_command_print_utilities(_connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    output('Printing utility info.')
    try:
        current_zone_id = services.current_zone_id()
        zone = services.get_zone(current_zone_id)
        lot = zone.lot
        import objects.components.types
        statistic_component: StatisticComponent = None if lot is None else lot.get_component(objects.components.types.STATISTIC_COMPONENT)
        instance_manager = services.get_instance_manager(Types.STATISTIC)
        statistic_power = instance_manager.get(233027)  # commodity_Utilities_Power
        statistic_water = instance_manager.get(233028)  # commodity_Utilities_Water
        power_value = statistic_component.get_stat_value(statistic_power)
        water_value = statistic_component.get_stat_value(statistic_water)
        output(f'POWER: {power_value}.')
        output(f'WATER: {water_value}.')
        utilities_manager: ZoneUtilitiesManager = services.get_utilities_manager_by_zone_id(current_zone_id)
        power_utility_info: UtilityInfo = utilities_manager.get_utility_info(Utilities.POWER)
        power_surplus = power_utility_info.surplus
        power_active = power_utility_info.active
        power_shut_off_reason = power_utility_info._shutoff_reasons
        output(f'SURPLUS POWER: {power_surplus} ACTIVE: {power_active} SHUT OFF REASONS: {power_shut_off_reason}')
        water_utility_info: UtilityInfo = utilities_manager.get_utility_info(Utilities.WATER)
        surplus_water = water_utility_info.surplus
        water_active = water_utility_info.active
        water_shut_off_reasons = water_utility_info._shutoff_reasons
        output(f'SURPLUS WATER: {surplus_water} ACTIVE: {water_active} SHUT OFF REASONS: {water_shut_off_reasons}')
    except Exception as ex:
        output('Error happened')
        log.error('Error happened', exception=ex)


@Command(
    'bbl.set_power_level',
    command_type=CommandType.Live
)
def _bbl_command_set_power_level(amount: float, _connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    output(f'Setting power level of current lot to {amount}.')

    current_zone_id = services.current_zone_id()
    zone = services.get_zone(current_zone_id)
    lot = zone.lot
    import objects.components.types
    statistic_component: StatisticComponent = None if lot is None else lot.get_component(
        objects.components.types.STATISTIC_COMPONENT)
    instance_manager = services.get_instance_manager(Types.STATISTIC)
    statistic_power = instance_manager.get(233027)  # commodity_Utilities_Power
    statistic_component.set_stat_value(statistic_power, amount)


@Command(
    'bbl.set_water_level',
    command_type=CommandType.Live
)
def _bbl_command_set_water_level(amount: float, _connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    output(f'Setting water level of current lot to {amount}.')

    current_zone_id = services.current_zone_id()
    zone = services.get_zone(current_zone_id)
    lot = zone.lot
    import objects.components.types
    statistic_component: StatisticComponent = None if lot is None else lot.get_component(
        objects.components.types.STATISTIC_COMPONENT)
    instance_manager = services.get_instance_manager(Types.STATISTIC)
    statistic_water = instance_manager.get(233028)  # commodity_Utilities_Water
    statistic_component.set_stat_value(statistic_water, amount)
