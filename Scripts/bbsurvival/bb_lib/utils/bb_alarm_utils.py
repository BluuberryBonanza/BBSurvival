"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Callable, Any, TypeVar, Union

import services
from alarms import AlarmHandle
from bbsurvival.bb_lib.classes.bb_alarm_handle import BBAlarmHandle
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from date_and_time import TimeSpan
from scheduling import Timeline

OwnerType = TypeVar('OwnerType', Any, Any)


class BBAlarmUtils:
    """Utilities for managing alarms."""
    @classmethod
    def schedule_alarm(
        cls,
        owning_mod_identity: BBModIdentity,
        owner: OwnerType,
        time_until_trigger: TimeSpan,
        on_triggered: Callable[[OwnerType, BBAlarmHandle], None],
        should_repeat: bool = False,
        time_until_repeat: TimeSpan = None,
        accurate_repeat: bool = True,
        keep_running_on_zone_transition: bool = False,
        timeline: Timeline = None
    ) -> Union[BBAlarmHandle, None]:
        """schedule_alarm(\
            owning_mod_identity,\
            owner,\
            time_until_trigger,\
            on_triggered,\
            should_repeat=False,\
            time_until_repeat=None,\
            accurate_repeat=True,\
            keep_running_on_zone_transition=False,\
            timeline=None\
        )

        Schedule for something to trigger at a certain Time.

        :param owning_mod_identity: The identity of the mod creating the alarm.
        :type owning_mod_identity: BBModIdentity
        :param owner: The owner of the alarm. For example, if the alarm is to make a Sim do something, this should be their Sim Info.
        :type owner: Any
        :param time_until_trigger: The amount of time to wait until the alarm should be triggered.
        :type time_until_trigger: TimeSpan
        :param on_triggered: What should happen when the alarm triggers.
        :type on_triggered: Callable[[OwnerType, BBAlarmHandle], None]
        :param should_repeat: Set to True, if the Alarm should repeat. Set to False, if the Alarm should only trigger once. Default is False.
        :type should_repeat: bool, optional
        :param time_until_repeat: The amount of time to wait after a trigger, before triggering the alarm again. Default is None.
        :type time_until_repeat: TimeSpan, optional
        :param accurate_repeat: Set to True, if the Alarm should be based on the current Sim Time. Set to False, if the Alarm should be based off a simulated current Sim Time. Default is True.
        :type accurate_repeat: bool, optional
        :param keep_running_on_zone_transition: Set to True, if the Alarm should keep running after a zone transition. Set to False, if the Alarm should stop running after a zone transition. Default is False.
        :type keep_running_on_zone_transition: bool, optional
        :param timeline: The timeline to use when calculating the trigger time. Default is the default timeline.
        :type timeline: Timeline, optional
        :return: The handle for the Alarm or None if no timeline is available.
        :rtype: BBAlarmHandle or None
        """

        if should_repeat and time_until_repeat is None:
            raise AssertionError('Alarm was created to repeat, but no "time_until_repeat" was specified!')

        if timeline is None:
            time_service = services.time_service()
            if time_service.sim_timeline is None:
                return None
            timeline = time_service.sim_timeline

        if accurate_repeat:
            initial_time = timeline.now
        else:
            initial_time = timeline.future

        def _on_alarm_triggered(handle: BBAlarmHandle):
            alarm_owner = handle.owner
            try:
                on_triggered(alarm_owner, handle)
            except Exception as ex:
                log = BBLogRegistry().register_log(handle.mod_identity, 'bb_alarm_utils')
                log.error(f'An exception occurred when triggering alarm callback for {alarm_owner}.', exception=ex, alarm_owner=alarm_owner)

        return BBAlarmHandle(
            owning_mod_identity,
            owner,
            _on_alarm_triggered,
            timeline,
            initial_time + time_until_trigger,
            should_repeat=should_repeat,
            repeat_interval=time_until_repeat or time_until_trigger,
            accurate_repeat=accurate_repeat,
            keep_running_on_zone_transition=keep_running_on_zone_transition
        )

    @classmethod
    def schedule_daily_alarm(
        cls,
        owning_mod_identity: BBModIdentity,
        owner: OwnerType,
        sim_hour: int,
        sim_minute: int,
        on_triggered: Callable[[OwnerType, BBAlarmHandle], None],
        accurate_repeat: bool = True,
        keep_running_on_zone_transition: bool = False,
        timeline: Timeline = None
    ) -> Union[BBAlarmHandle, None]:
        """schedule_daily_alarm(\
            owning_mod_identity,\
            owner,\
            sim_hour,\
            sim_minute,\
            on_triggered,\
            accurate_repeat=True,\
            keep_running_on_zone_transition=False,\
            timeline=None\
        )

        Schedule for something to trigger at a certain Time of day, every day.

        :param owning_mod_identity: The identity of the mod creating the alarm.
        :type owning_mod_identity: BBModIdentity
        :param owner: The owner of the alarm. For example, if the alarm is to make a Sim do something, this should be their Sim Info.
        :type owner: Any
        :param sim_hour: The hour of the day to repeat the alarm at. (In Sim Time)
        :type sim_hour: int
        :param sim_minute: The minute of the day to repeat the alarm at. (In Sim Time)
        :param on_triggered: What should happen when the alarm triggers.
        :type on_triggered: Callable[[OwnerType, BBAlarmHandle], None]
        :param accurate_repeat: Set to True, if the Alarm should be based on the current Sim Time. Set to False, if the Alarm should be based off a simulated current Sim Time. Default is True.
        :type accurate_repeat: bool, optional
        :param keep_running_on_zone_transition: Set to True, if the Alarm should keep running after a zone transition. Set to False, if the Alarm should stop running after a zone transition. Default is False.
        :type keep_running_on_zone_transition: bool, optional
        :param timeline: The timeline to use when calculating the trigger time. Default is the default timeline.
        :type timeline: Timeline, optional
        :return: The handle for the Alarm or None if no timeline is available.
        :rtype: BBAlarmHandle or None
        """
        if timeline is None:
            time_service = services.time_service()
            if time_service.sim_timeline is None:
                return None
            timeline = time_service.sim_timeline

        from date_and_time import create_date_and_time, sim_ticks_per_day

        if accurate_repeat:
            initial_time = timeline.now
        else:
            initial_time = timeline.future

        alarm_time_of_day = create_date_and_time(hours=sim_hour, minutes=sim_minute)
        alarm_next_trigger_time = initial_time.time_till_next_day_time(alarm_time_of_day)
        if alarm_next_trigger_time.in_ticks() == 0:
            alarm_next_trigger_time += TimeSpan(sim_ticks_per_day())

        repeat_interval = TimeSpan(sim_ticks_per_day())

        return cls.schedule_alarm(
            owning_mod_identity,
            owner,
            alarm_next_trigger_time,
            on_triggered,
            should_repeat=True,
            time_until_repeat=repeat_interval,
            accurate_repeat=accurate_repeat,
            keep_running_on_zone_transition=keep_running_on_zone_transition,
            timeline=timeline
        )

    @classmethod
    def cancel_alarm(cls, alarm_handle: Union[AlarmHandle]) -> bool:
        """cancel_alarm(alarm_handle)

        Cancel an Alarm.

        :param alarm_handle: The handle for the Alarm to cancel.
        :type alarm_handle: AlarmHandle
        :return: True, if the Alarm was cancelled successfully. False, if not.
        :rtype: bool
        """
        if alarm_handle is None:
            return False
        alarm_handle.cancel()
        return True
