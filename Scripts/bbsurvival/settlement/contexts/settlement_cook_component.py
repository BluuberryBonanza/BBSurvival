"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Dict, Union

import services
from bbsurvival.bb_lib.classes.bb_alarm_handle import BBAlarmHandle
from bbsurvival.bb_lib.utils.bb_alarm_utils import BBAlarmUtils
from bbsurvival.bb_lib.utils.bb_sim_interaction_utils import BBSimInteractionUtils
from bbsurvival.bb_lib.utils.bb_sim_statistic_utils import BBSimStatisticUtils
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.settlement.enums.cook_time_slot import BBSSettlementCookTimeSlot
from bbsurvival.settlement.enums.interaction_ids import BBSSettlementInteractionId
from bbsurvival.settlement.enums.string_ids import BBSSettlementStringIds
from bluuberrylibrary.dialogs.notifications.bb_notification import BBNotification
from bluuberrylibrary.dialogs.icons.bb_sim_icon_info import BBSimIconInfo
from bluuberrylibrary.logs.bb_log_mixin import BBLogMixin
from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from objects.game_object import GameObject
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
        hour_result = BBSimStatisticUtils.set_statistic_value(self.sim_info, hour_statistic, new_hour)
        log = self.get_log()
        log.debug('Set hour result', hour_result=hour_result)
        minute_statistic = BBSSettlementCookTimeSlot.get_minute_statistic(time_slot)
        BBSimStatisticUtils.set_statistic_value(self.sim_info, minute_statistic, new_minute)
        log.debug('Set minute result', hour_result=hour_result)

        self._setup_cook_times()

    def _trigger_cook(self, sim_info: SimInfo, alarm_handle: BBAlarmHandle):
        log = self.get_log()
        log.debug(f'Triggering Sim to cook. {sim_info}.')
        fridge_object = self._find_fridge_object()
        if fridge_object is None:
            BBNotification(
                self.get_mod_identity(),
                BBLocalizedStringData(BBSSettlementStringIds.FAILED_TO_COOK, tokens=(sim_info,)),
                BBLocalizedStringData(BBSSettlementStringIds.FAILED_TO_COOK_NO_FRIDGE_DESCRIPTION, tokens=(sim_info,)),
            ).show(icon=BBSimIconInfo(sim_info))
            return
        enqueue_result_normal = BBSimInteractionUtils.push_interaction(self.get_mod_identity(), sim_info, BBSSettlementInteractionId.SETTLEMENT_COOK_COOK_GROUP_MEAL_AUTONOMOUSLY_REQUIRED_INGREDIENTS, target=fridge_object)
        if not enqueue_result_normal:
            enqueue_result_vegetarian = BBSimInteractionUtils.push_interaction(self.get_mod_identity(), sim_info, BBSSettlementInteractionId.SETTLEMENT_COOK_COOK_GROUP_MEAL_AUTONOMOUSLY_VEGETARIAN_REQUIRED_INGREDIENTS, target=fridge_object)
            if not enqueue_result_vegetarian:
                enqueue_result_health_nut = BBSimInteractionUtils.push_interaction(self.get_mod_identity(), sim_info, BBSSettlementInteractionId.SETTLEMENT_COOK_COOK_GROUP_MEAL_AUTONOMOUSLY_HEALTH_NUT_REQUIRED_INGREDIENTS, target=fridge_object)
                if not enqueue_result_health_nut:
                    enqueue_result_junk_food = BBSimInteractionUtils.push_interaction(self.get_mod_identity(), sim_info, BBSSettlementInteractionId.SETTLEMENT_COOK_COOK_GROUP_MEAL_AUTONOMOUSLY_JUNK_FOOD_REQUIRED_INGREDIENTS, target=fridge_object)
                    if not enqueue_result_junk_food:
                        BBNotification(
                            self.get_mod_identity(),
                            BBLocalizedStringData(BBSSettlementStringIds.FAILED_TO_COOK, tokens=(sim_info,)),
                            BBLocalizedStringData(BBSSettlementStringIds.FAILED_TO_COOK_NO_AVAILABLE_RECIPES_DESCRIPTION, tokens=(sim_info,)),
                        ).show(icon=BBSimIconInfo(sim_info))
                    else:
                        log.debug('Queued junk food group meal')
                else:
                    log.debug('Queued health nut group meal')
            else:
                log.debug('Queued vegetarian group meal')
        else:
            log.debug('Queued normal group meal')

    def _find_fridge_object(self) -> GameObject:
        game_object_list = tuple(services.object_manager().get_all())
        tags = (
            1002,  # Fridge
            2233,  # Fridge Mini
        )
        for game_object in game_object_list:
            if game_object is None:
                continue
            if not game_object.has_any_tag(tuple(tags)):
                continue
            return game_object

    def _setup_cook_times(self):
        self._teardown_cook_times()
        log = self.get_log()
        log.debug(f'Setting up cook times for {self.sim_info}')
        has_cook_time = False
        for time_slot in (BBSSettlementCookTimeSlot.SLOT_ONE, BBSSettlementCookTimeSlot.SLOT_TWO, BBSSettlementCookTimeSlot.SLOT_THREE):
            hour_statistic = BBSSettlementCookTimeSlot.get_hour_statistic(time_slot)
            cook_hour = BBSimStatisticUtils.get_statistic_value(self.sim_info, hour_statistic)
            minute_statistic = BBSSettlementCookTimeSlot.get_minute_statistic(time_slot)
            if BBSimStatisticUtils.has_statistic(self.sim_info, minute_statistic):
                cook_minute = BBSimStatisticUtils.get_statistic_value(self.sim_info, minute_statistic)
            else:
                cook_minute = 0

            if cook_hour is not None and cook_hour != -1.0:
                cook_alarm = BBAlarmUtils.schedule_daily_alarm(
                    ModIdentity(),
                    self.sim_info,
                    int(cook_hour),
                    int(cook_minute),
                    self._trigger_cook,
                    keep_running_on_zone_transition=False
                )
                if cook_alarm is not None:
                    self._cook_time_alarms[time_slot] = cook_alarm
                    has_cook_time = True

        if not has_cook_time:
            log.debug(f'{self.sim_info} had no predefined cook times specified. Setting them to default cook times.')
            for time_slot in (BBSSettlementCookTimeSlot.SLOT_ONE, BBSSettlementCookTimeSlot.SLOT_TWO, BBSSettlementCookTimeSlot.SLOT_THREE):
                cook_hour = BBSSettlementCookTimeSlot.get_default_cook_hour(time_slot)
                cook_minute = BBSSettlementCookTimeSlot.get_default_cook_minute(time_slot)

                if cook_hour is not None and cook_hour != -1.0:
                    cook_alarm = BBAlarmUtils.schedule_daily_alarm(
                        ModIdentity(),
                        self.sim_info,
                        int(cook_hour),
                        int(cook_minute),
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
