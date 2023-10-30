from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from sims.household_utilities.utilities_manager import UtilityInfo

log = BBLogRegistry().register_log(ModIdentity(), 'bbs_utilities_effect_all_lots')
log.enable()


# @BBInjectionUtils.inject(ModIdentity(), UtilityInfo, UtilityInfo.add_shutoff_reason.__name__)
def _bbs_add_reason(original, self, *_, **__):
    log.log_stack()
    log.debug('Adding shut off reason', argles=_, kwargles=__)
    return original(self, *_, **__)


# @BBInjectionUtils.inject(ModIdentity(), UtilityInfo, UtilityInfo.remove_shutoff_reason.__name__)
def _bbs_remove_reason(original, self, *_, **__):
    log.log_stack()
    log.debug('Removing shut off reason', argles=_, kwargles=__)
    return original(self, *_, **__)


# TODO: This is a temporary fix. We should really look into why OFF_THE_GRID is not properly staying in the _shutoff_reasons
@BBInjectionUtils.inject(ModIdentity(), UtilityInfo, 'active')
def _bbs_utility_info_active(original, self, *_, **__):
    # We override this so that power and water being active only applies when there is a surplus of power.
    return self.surplus


@BBInjectionUtils.inject(ModIdentity(), UtilityInfo, UtilityInfo.get_priority_shutoff_tooltip.__name__)
def _bbs_fix_priority_shutoff_tooltip(original, self, shutoff_tooltip_override, *_, **__):
    if self.active:
        return
    valid_reasons = [reason for reason in self._shutoff_reasons if reason is not None]
    if not valid_reasons:
        return
    return original(self, shutoff_tooltip_override, *_, **__)
