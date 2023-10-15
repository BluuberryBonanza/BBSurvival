"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import services
from sims.household_manager import HouseholdManager


class BBHouseholdUtils:
    """Utilities for manipulating households."""

    @classmethod
    def get_household_manager(cls) -> HouseholdManager:
        """get_household_manager()

        Get the Household Manager

        :return: The Household Manager
        :rtype: HouseholdManager
        """
        return services.household_manager()
