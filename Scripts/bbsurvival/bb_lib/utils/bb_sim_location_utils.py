"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union

from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from sims.sim_info import SimInfo
from sims4.math import Location


class BBSimLocationUtils:
    """Utilities for manipulating households."""

    @classmethod
    def get_location(cls, sim_info: SimInfo) -> Union[Location, None]:
        """get_location()

        Get the location of a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: The location of the Sim or None if the Sim does not have a location.
        :rtype: Location or None
        """
        sim = BBSimUtils.to_sim_instance(sim_info)
        if sim is None:
            return None
        return sim.location
