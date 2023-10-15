import services
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from objects.components.statistic_component import StatisticComponent
from sims.household_utilities.utilities_manager import ZoneUtilitiesManager, UtilityInfo
from sims.household_utilities.utility_types import Utilities
from sims4.commands import Command, CommandType
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


# @BBInjectionUtils.inject(ModIdentity(), UtilityInfo, UtilityInfo.add_shutoff_reason.__name__)
def _bbl_add_reason(original, self, *_, **__):
    log.log_stack()
    log.debug('Adding shut off reason', argles=_, kwargles=__)
    return original(self, *_, **__)


# @BBInjectionUtils.inject(ModIdentity(), UtilityInfo, UtilityInfo.remove_shutoff_reason.__name__)
def _bbl_remove_reason(original, self, *_, **__):
    log.log_stack()
    log.debug('Removing shut off reason', argles=_, kwargles=__)
    return original(self, *_, **__)


# This is a temporary fix. We should really look into why OFF_THE_GRID is not properly staying in the _shutoff_reasons
@BBInjectionUtils.inject(ModIdentity(), UtilityInfo, 'active')
def _bbl_utility_info_active(original, self, *_, **__):
    # We override this so that power and water being active only applies when there is a surplus of power.
    return self.surplus
