"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Iterable, Union

import services
from bbsurvival.bb_lib.utils.bb_sim_household_utils import BBSimHouseholdUtils
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.settlement.enums.settlement_member_job import BBSSettlementMemberJobFlags
from bbsurvival.settlement.enums.trait_ids import BBSSettlementTraitId
from bbsurvival.settlement.contexts.settlement_context import BBSSettlementContext
from bbsurvival.settlement.contexts.settlement_member_context import BBSSettlementMemberContext
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.classes.bb_singleton import BBSingleton
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from sims.sim_info import SimInfo

log = BBLogRegistry().register_log(ModIdentity(), 'bbs_settlement_context_manager')


class BBSSettlementContextManager(metaclass=BBSingleton):
    def __init__(self):
        super().__init__()
        self._settlement_context = None

    @property
    def settlement_context(self) -> BBSSettlementContext:
        return self._settlement_context

    def setup_settlement_context(self, head_of_settlement_sim_info: SimInfo) -> BBRunResult:
        if self.settlement_context is not None and self.settlement_context.is_running:
            return BBRunResult(True, 'Settlement context already running.')
        elif self.settlement_context is not None:
            self.settlement_context.setup()
            return BBRunResult(True, 'Settlement context was not previously running.')
        member_contexts = list()
        if head_of_settlement_sim_info is None:
            head_of_settlement_sim_info = self._find_settlement_head_sim_info()
        log.debug('Adding head of household Sim.', head_of_settlement_sim_info=head_of_settlement_sim_info)
        member_contexts.append(BBSSettlementMemberContext(
            head_of_settlement_sim_info,
            BBSSettlementMemberJobFlags.NONE,
            True
        ))
        for sim_info in self._find_settlement_member_sim_infos_gen():
            log.debug('Adding settlement member', settlement_member=sim_info)
            member_contexts.append(BBSSettlementMemberContext(
                sim_info,
                BBSSettlementMemberJobFlags.NONE,
                False
            ))
        for household_sim_info in self._find_household_members_not_in_settlement_already_gen(head_of_settlement_sim_info):
            log.debug('Adding household member', household_sim_info=household_sim_info)
            result = BBSimTraitUtils.add_trait(household_sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER)
            log.debug('Trait add result', result=result, sim_info=household_sim_info)
            member_contexts.append(BBSSettlementMemberContext(
                household_sim_info,
                BBSSettlementMemberJobFlags.NONE,
                False
            ))
        settlement_context = BBSSettlementContext(
            member_contexts
        )
        settlement_context.setup()
        self._settlement_context = settlement_context
        return BBRunResult(True, 'Settle context setup properly.')

    def add_settlement_member_context(self, sim_info: SimInfo, head_of_settlement_sim_info: SimInfo = None) -> BBRunResult:
        if self.settlement_context is None or not self.settlement_context.is_running:
            if head_of_settlement_sim_info is None:
                head_of_settlement_sim_info = self._find_settlement_head_sim_info()
                if head_of_settlement_sim_info is None:
                    return BBRunResult(False, 'No head of household found for current lot.')
            setup_result = self.setup_settlement_context(head_of_settlement_sim_info=head_of_settlement_sim_info)
            if not setup_result:
                return setup_result

        result = BBSimTraitUtils.add_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER)
        log.debug('Trait add result as result of adding settlement member context', result=result, sim_info=sim_info)

        if self.settlement_context.has_member_context(sim_info):
            return BBRunResult(False, f'{sim_info} was already in the settlement context.')

        member_context = BBSSettlementMemberContext(
            sim_info,
            BBSSettlementMemberJobFlags.NONE,
            False
        )
        self.settlement_context.add_member_context(
            member_context
        )
        member_context.setup()
        return BBRunResult(True, 'Finished setting up context.')

    def teardown_settlement_context(self) -> BBRunResult:
        if self.settlement_context is None:
            return BBRunResult(True, 'Settlement context not even setup yet.')
        self.settlement_context.teardown()
        self._settlement_context = None
        return BBRunResult(True, 'Successfully tore down settlement context.')

    def _find_settlement_head_sim_info(self) -> Union[SimInfo, None]:
        current_zone_id = services.current_zone_id()
        for sim_info in BBSimUtils.get_all_sim_info_gen():
            sim_household = BBSimHouseholdUtils.get_household(sim_info)
            if BBSimTraitUtils.has_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD):
                home_zone_id = sim_household.home_zone_id
                if current_zone_id == home_zone_id:
                    return sim_info

    def _find_settlement_member_sim_infos_gen(self) -> Iterable[SimInfo]:
        for sim_info in BBSimUtils.get_all_sim_info_gen():
            if BBSimTraitUtils.has_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER):
                yield sim_info

    def _find_household_members_not_in_settlement_already_gen(self, head_of_household_sim_info: SimInfo) -> Iterable[SimInfo]:
        for sim_info in BBSimUtils.get_all_sim_info_gen():
            if (BBSimHouseholdUtils.is_in_same_household_of_sim(sim_info, head_of_household_sim_info)
                    and not BBSimTraitUtils.has_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER)
                    and not BBSimTraitUtils.has_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD)):
                yield sim_info

