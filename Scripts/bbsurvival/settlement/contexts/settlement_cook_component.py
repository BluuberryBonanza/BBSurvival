"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Dict, Union

from bbsurvival.bb_lib.classes.bb_alarm_handle import BBAlarmHandle
from bbsurvival.bb_lib.utils.bb_alarm_utils import BBAlarmUtils
from bbsurvival.bb_lib.utils.bb_sim_statistic_utils import BBSimStatisticUtils
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.settlement.enums.cook_time_slot import BBSSettlementCookTimeSlot
from bluuberrylibrary.logs.bb_log_mixin import BBLogMixin
from sims.sim_info import SimInfo


class BBSettlementMemberCookComponent(BBLogMixin):
    """A component used to keep track and manage Settlement Cooks."""
    @classmethod
    def get_mod_identity(cls) -> ModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'bbs_settlement_member'

    def __init__(self, sim_info: SimInfo):
        self._sim_info = sim_info
        self._cook_time_alarms: Dict[BBSSettlementCookTimeSlot, Union[BBAlarmHandle, None]] = {
            BBSSettlementCookTimeSlot.SLOT_ONE: None,
            BBSSettlementCookTimeSlot.SLOT_TWO: None,
            BBSSettlementCookTimeSlot.SLOT_THREE: None
        }

    @property
    def sim_info(self) -> SimInfo:
        return self._sim_info

    def setup(self):
        self._setup_cook_times()

    def teardown(self):
        self._teardown_cook_times()

    def set_cook_time_slot(self, time_slot: BBSSettlementCookTimeSlot, new_hour: int, new_minute: int):
        hour_statistic = BBSSettlementCookTimeSlot.get_hour_statistic(time_slot)
        BBSimStatisticUtils.set_statistic_value(self.sim_info, hour_statistic, new_hour)

        self._setup_cook_times()

    def _trigger_cook(self, sim_info: SimInfo, alarm_handle: BBAlarmHandle):
        log = self.get_log()
        log.debug(f'Triggering Sim to cook. {sim_info}.')

    def _setup_cook_times(self):
        self._teardown_cook_times()
        log = self.get_log()
        log.debug(f'Setting up cook times for {self.sim_info}')
        has_cook_time = False
        for time_slot in (BBSSettlementCookTimeSlot.SLOT_ONE, BBSSettlementCookTimeSlot.SLOT_TWO, BBSSettlementCookTimeSlot.SLOT_THREE):
            hour_statistic = BBSSettlementCookTimeSlot.get_hour_statistic(time_slot)
            cook_hour = BBSimStatisticUtils.get_statistic_value(self.sim_info, hour_statistic)
            cook_minute = 0

            if cook_hour is not None and cook_hour != -1.0:
                cook_alarm = BBAlarmUtils.schedule_daily_alarm(
                    ModIdentity(),
                    self.sim_info,
                    int(cook_hour),
                    cook_minute,
                    self._trigger_cook,
                    keep_running_on_zone_transition=False
                )
                if cook_alarm is not None:
                    self._cook_time_alarms[time_slot] = cook_alarm
                    has_cook_time = True

        if not has_cook_time:
            log.debug(f'{self.sim_info} had no predefined cook times specified. Setting them to default cook times.')
            time_slot_to_hour = {
                BBSSettlementCookTimeSlot.SLOT_ONE: 6,
                BBSSettlementCookTimeSlot.SLOT_TWO: 12,
                BBSSettlementCookTimeSlot.SLOT_THREE: 18
            }

            for time_slot in (BBSSettlementCookTimeSlot.SLOT_ONE, BBSSettlementCookTimeSlot.SLOT_TWO, BBSSettlementCookTimeSlot.SLOT_THREE):
                cook_hour = time_slot_to_hour[time_slot]
                cook_minute = 0

                if cook_hour is not None and cook_hour != -1.0:
                    cook_alarm = BBAlarmUtils.schedule_daily_alarm(
                        ModIdentity(),
                        self.sim_info,
                        int(cook_hour),
                        cook_minute,
                        self._trigger_cook,
                        keep_running_on_zone_transition=False
                    )
                    if cook_alarm is not None:
                        self._cook_time_alarms[time_slot] = cook_alarm

    def _teardown_cook_times(self):
        for (cook_time_slot, cook_alarm) in self._cook_time_alarms.items():
            if cook_alarm is not None:
                BBAlarmUtils.cancel_alarm(cook_alarm)

        self._cook_time_alarms: Dict[BBSSettlementCookTimeSlot, Union[BBAlarmHandle, None]] = {
            BBSSettlementCookTimeSlot.SLOT_ONE: None,
            BBSSettlementCookTimeSlot.SLOT_TWO: None,
            BBSSettlementCookTimeSlot.SLOT_THREE: None
        }
