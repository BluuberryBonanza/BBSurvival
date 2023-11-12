"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union

from bbsurvival.bb_lib.utils.bb_statistic_utils import BBStatisticUtils
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.classes.bb_test_result import BBTestResult
from sims.sim_info import SimInfo
from statistics.statistic_tracker import StatisticTracker


class BBSimStatisticUtils:
    """Utilities for manipulating statistics on Sims."""

    @classmethod
    def has_statistic(cls, sim_info: SimInfo, statistic: int) -> BBTestResult:
        """has_statistic(sim_info, statistic)

        Check if a Sim has a Statistic.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param statistic: The statistic to check.
        :type statistic: int
        :return: True, if the Sim has the statistic. False, if not.
        :rtype: BBTestResult
        """
        statistic_instance = BBStatisticUtils.load_statistic_by_guid(statistic)
        if statistic_instance is None:
            return BBTestResult(False, f'{sim_info} does not have {statistic} because it does not exist.')
        statistic_tracker: StatisticTracker = sim_info.get_tracker(statistic_instance)
        if statistic_tracker is None:
            return BBTestResult(False, f'{sim_info} does not have {statistic_instance} because {sim_info} does not have a Statistic Tracker.')
        result = statistic_tracker.has_statistic(statistic_instance)
        if result:
            return BBTestResult(True, f'{sim_info} had statistic {statistic_instance}.')
        return BBTestResult(False, f'{sim_info} did not have statistic {statistic_instance}.')

    @classmethod
    def get_statistic_value(cls, sim_info: SimInfo, statistic: int) -> Union[float, None]:
        """get_statistic_value(sim_info, statistic)

        Get the value of a Statistic on a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param statistic: The statistic to get the value of.
        :type statistic: int
        :return: The value of the statistic for the Sim or None if an issue happened.
        :rtype: float or None
        """
        statistic_instance = BBStatisticUtils.load_statistic_by_guid(statistic)
        if statistic_instance is None:
            return None
        statistic_tracker: StatisticTracker = sim_info.get_tracker(statistic_instance)
        if statistic_tracker is None:
            return None
        return statistic_tracker.get_value(statistic_instance)

    @classmethod
    def set_statistic_value(cls, sim_info: SimInfo, statistic: int, value: float) -> BBRunResult:
        """set_statistic_value(sim_info, statistic, value)

        Set the value of a Statistic on a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param statistic: The statistic to modify.
        :type statistic: int
        :param value: The value to set the Statistic to.
        :type value: float
        :return: The result of running. True, if successful. False, if not.
        :rtype: BBRunResult
        """
        statistic_instance = BBStatisticUtils.load_statistic_by_guid(statistic)
        if statistic_instance is None:
            return BBRunResult(False, f'Cannot set Statistic value. No Statistic exists with id {statistic}.')
        statistic_tracker: StatisticTracker = sim_info.get_tracker(statistic_instance)
        if statistic_tracker is None:
            return BBRunResult(False, f'Cannot set Statistic value. No Statistic Tracker existed on {sim_info}.')
        statistic_tracker.set_value(statistic_instance, value, add=True)
        return BBRunResult.TRUE
