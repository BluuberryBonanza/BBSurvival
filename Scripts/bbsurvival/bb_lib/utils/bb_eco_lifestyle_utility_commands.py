"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import services
from bbsurvival.bb_lib.utils.bb_eco_lifestyle_utility_utils import BBEcoLifestyleUtilityUtils
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.mod_identity import ModIdentity
from sims.household_utilities.utilities_manager import ZoneUtilitiesManager, UtilityInfo
from sims.household_utilities.utility_types import Utilities
from sims4.commands import CommandType, Command

log = BBLogRegistry().register_log(ModIdentity(), 'bbl_print_utilities')
# log.enable()


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
        power_value = BBEcoLifestyleUtilityUtils.get_power_level(current_zone_id)
        water_value = BBEcoLifestyleUtilityUtils.get_water_level(current_zone_id)
        eco_footprint_value = BBEcoLifestyleUtilityUtils.get_eco_footprint_level(current_zone_id)
        output(f'POWER: {power_value}.')
        output(f'WATER: {water_value}.')
        output(f'ECO FOOTPRINT: {eco_footprint_value}.')
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
    BBEcoLifestyleUtilityUtils.set_power_level(current_zone_id, amount)


@Command(
    'bbl.set_water_level',
    command_type=CommandType.Live
)
def _bbl_command_set_water_level(amount: float, _connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    output(f'Setting water level of current lot to {amount}.')

    current_zone_id = services.current_zone_id()
    BBEcoLifestyleUtilityUtils.set_water_level(current_zone_id, amount)


@Command(
    'bbl.set_eco_footprint_level',
    command_type=CommandType.Live
)
def _bbl_command_set_eco_footprint_level(amount: float, _connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    output(f'Setting eco footprint level of current lot to {amount}.')

    current_zone_id = services.current_zone_id()
    BBEcoLifestyleUtilityUtils.set_eco_footprint_level(current_zone_id, amount)
