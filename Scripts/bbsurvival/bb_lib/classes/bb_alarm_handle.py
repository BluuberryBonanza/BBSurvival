"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Callable, TypeVar, Any

from alarms import AlarmHandle
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from date_and_time import TimeSpan
from scheduling import ElementHandle, Timeline

OwnerType = TypeVar('OwnerType', Any, Any)


class BBAlarmHandle(AlarmHandle):
    """BBAlarmHandle(\
        owning_mod_identity,\
        owner,\
        on_triggered,\
        timeline,\
        when_to_trigger,\
        should_repeat=False,\
        repeat_interval=None,\
        accurate_repeat=True,\
        keep_running_on_zone_transition=False\
    )

    A handle for an Alarm.

    :param owning_mod_identity: The identity of the mod creating the alarm.
    :type owning_mod_identity: BBModIdentity
    :param owner: The owner of the alarm. For example, if the alarm is to make a Sim do something, this should be their Sim Info.
    :type owner: Any
    :param when_to_trigger: The amount of time to wait until the alarm should be triggered.
    :type when_to_trigger: TimeSpan
    :param on_triggered: What should happen when the alarm triggers.
    :type on_triggered: Callable[[OwnerType, BBAlarmHandle], None]
    :param should_repeat: Set to True, if the Alarm should repeat. Set to False, if the Alarm should only trigger once. Default is False.
    :type should_repeat: bool, optional
    :param repeat_interval: The amount of time to wait after a trigger, before triggering the alarm again. Default is None.
    :type repeat_interval: TimeSpan, optional
    :param accurate_repeat: Set to True, if the Alarm should be based on the current Sim Time. Set to False, if the Alarm should be based off a simulated current Sim Time. Default is True.
    :type accurate_repeat: bool, optional
    :param keep_running_on_zone_transition: Set to True, if the Alarm should keep running after a zone transition. Set to False, if the Alarm should stop running after a zone transition. Default is False.
    :type keep_running_on_zone_transition: bool, optional
    :param timeline: The timeline to use when calculating the trigger time. Default is the default timeline.
    :type timeline: Timeline, optional
    """
    def __init__(
        self,
        owning_mod_identity: BBModIdentity,
        owner: OwnerType,
        on_triggered: Callable[[OwnerType, 'BBAlarmHandle'], None],
        timeline: Timeline,
        when_to_trigger: TimeSpan,
        should_repeat: bool = False,
        repeat_interval: TimeSpan = None,
        accurate_repeat: bool = True,
        keep_running_on_zone_transition: bool = False
    ):
        self.mod_identity = owning_mod_identity
        self.started_at_time = when_to_trigger
        super().__init__(
            owner,
            on_triggered,
            timeline,
            when_to_trigger,
            repeating=should_repeat,
            repeat_interval=repeat_interval,
            accurate_repeat=accurate_repeat,
            cross_zone=keep_running_on_zone_transition
        )

    @property
    def is_running(self) -> bool:
        """Check if the alarm is currently running."""
        if self._element_handle is None:
            return False
        element_handle: ElementHandle = self._element_handle
        # noinspection PyPropertyAccess
        return element_handle.is_active and element_handle.is_scheduled
