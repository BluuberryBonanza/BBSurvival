from typing import Union

import services
from bbsurvival.bb_lib.utils.bb_household_utils import BBHouseholdUtils
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from sims.household import Household
from sims.household_enums import HouseholdChangeOrigin
from sims.sim_info import SimInfo


class BBSimHouseholdUtils:
    """Utilities for manipulating households of Sims."""

    @classmethod
    def has_household(cls, sim_info: SimInfo) -> bool:
        """has_household(sim_info)

        Check if a Sim has a Household or not.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a Household. False, if the Sim does not have a Household.
        :rtype: bool
        """
        return hasattr(sim_info, 'household') and sim_info.household is not None

    @classmethod
    def get_household(cls, sim_info: SimInfo) -> Union[Household, None]:
        """get_household(sim_info)

        Get the household of a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: The Household of the Sim or None if not found.
        :rtype: Household or None
        """
        if not cls.has_household(sim_info):
            return None
        return BBHouseholdUtils.get_household_manager().get(sim_info.household.id)

    @classmethod
    def move_to_household_of_sim(cls, moving_sim_info: SimInfo, destination_household_sim_info: SimInfo) -> BBRunResult:
        household_manager = services.household_manager()
        result = household_manager.switch_sim_household(moving_sim_info, target_sim_info=destination_household_sim_info, reason=HouseholdChangeOrigin.LIVE_TRANSFER_DIALOG)
        if result:
            return BBRunResult(True, f'{moving_sim_info} was moved successfully to the household of {destination_household_sim_info}')
        return BBRunResult(False, f'Failed to move {moving_sim_info} to the household of {destination_household_sim_info}')

