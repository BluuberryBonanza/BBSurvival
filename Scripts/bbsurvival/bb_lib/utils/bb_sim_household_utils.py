from typing import Union

import services
from bbsurvival.bb_lib.utils.bb_household_utils import BBHouseholdUtils
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from sims.household import Household
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
        """move_to_household_of_sim(moving_sim_info, destination_household_sim_info)

        Move Sim A to the household of Sim B.

        """
        active_household = services.active_household()
        starting_household = moving_sim_info.household
        moving_sim = BBSimUtils.to_sim_instance(moving_sim_info)
        moving_sim_id = BBSimUtils.to_sim_id(moving_sim_info)
        moving_is_hidden = (moving_sim_id is None
                            or moving_sim is None
                            or services.hidden_sim_service().is_hidden(moving_sim_id)
                            or moving_sim.is_hidden()
                            or moving_sim.opacity == 0)
        destination_household = destination_household_sim_info.household
        if destination_household is None:
            raise AssertionError('Destination Household not specified!')
        if moving_is_hidden:
            services.hidden_sim_service().unhide_sim(moving_sim_info.id)
        if starting_household is destination_household:
            raise AssertionError('The Sim being moved is already in the destination household.')
        starting_household.remove_sim_info(moving_sim_info, destroy_if_empty_household=True)
        destination_household.add_sim_info_to_household(moving_sim_info)
        client = services.client_manager().get_first_client()
        if destination_household is active_household:
            client.add_selectable_sim_info(moving_sim_info)
        else:
            if destination_household_sim_info is moving_sim_info:
                client.set_next_sim()
            client.remove_selectable_sim_info(moving_sim_info)
        if moving_sim_info.career_tracker is not None:
            moving_sim_info.career_tracker.remove_invalid_careers()
        sim = moving_sim_info.get_sim_instance()
        if sim is not None:
            sim.update_intended_position_on_active_lot(update_ui=True)
            situation_manager = services.get_zone_situation_manager()
            for situation in situation_manager.get_situations_sim_is_in(sim):
                if destination_household is active_household and situation.is_user_facing:
                    pass
                else:
                    situation_manager.remove_sim_from_situation(sim, situation.id)
            services.daycare_service().on_sim_spawn(moving_sim_info)
        return BBRunResult(True, f'{moving_sim_info} was moved successfully to the household of {destination_household_sim_info}')
