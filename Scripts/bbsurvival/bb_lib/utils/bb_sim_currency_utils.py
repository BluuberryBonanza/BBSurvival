"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union

from bbsurvival.bb_lib.enums.bb_currency_modify_reasons import BBCurrencyModifyReason
from bbsurvival.bb_lib.utils.bb_sim_household_utils import BBSimHouseholdUtils
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from sims.funds import FamilyFunds
from sims.sim_info import SimInfo


class BBSimCurrencyUtils:
    """Utilities for manipulating currency of Sims."""

    @classmethod
    def add_simoleons(cls, sim_info: SimInfo, amount: int, reason: BBCurrencyModifyReason = BBCurrencyModifyReason.CHEAT, **kwargs) -> BBRunResult:
        """add_simoleons(sim_info, amount, reason=BBCurrencyModifyReason.CHEAT, **kwargs)

        Give simoleons to a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param amount: The amount to add.
        :type amount: int
        :param reason: The reason the simoleons are being added. Default is CHEAT.
        :type reason: CommonCurrencyModifyReason, optional
        :return: The result of adding simoleons.
        :rtype: BBRunResult
        """
        family_funds = cls.get_family_funds(sim_info)
        if family_funds is None:
            return BBRunResult(False, reason='The Sim had no household and thus no funds to add to.')
        family_funds.add(amount, reason, **kwargs)
        return BBRunResult.TRUE

    @classmethod
    def get_family_funds(cls, sim_info: SimInfo) -> Union[FamilyFunds, None]:
        """get_family_funds(sim_info)

        Get the funds for a Family.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: The funds of the Sims Family or None if not found.
        :rtype: FamilyFunds or None
        """
        household = BBSimHouseholdUtils.get_household(sim_info)
        if household is None:
            return None
        return household.funds
