"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union

from bbsurvival.bb_lib.utils.bb_instance_utils import BBInstanceUtils
from sims4.resources import Types
from statistics.statistic import Statistic


class BBStatisticUtils:
    """Utilities for manipulating statistics."""

    @classmethod
    def load_statistic_by_guid(cls, statistic: int) -> Union[Statistic, None]:
        """load_statistic_by_guid(statistic)

        Load a Statistic by its GUID

        :param statistic: The GUID of the Statistic to load.
        :type statistic: int
        :return: The loaded Statistic or None if not found.
        :rtype: Statistic or None
        """
        if isinstance(statistic, Statistic) or statistic is Statistic:
            return statistic

        return BBInstanceUtils.get_instance(Types.STATISTIC, statistic, return_type=Statistic)
