from typing import Iterable, Union

from bbsurvival.settlement.enums.settlement_member_job import BBSSettlementMemberJobFlags
from bbsurvival.settlement.enums.trait_ids import BBSSettlementTraitId
from bbsurvival.settlement.settlement_context import BBSSettlementContext
from bbsurvival.settlement.settlement_member_context import BBSSettlementMemberContext
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.classes.bb_singleton import BBSingleton
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from sims.sim_info import SimInfo


class BBSSettlementContextManager(metaclass=BBSingleton):
    def __init__(self):
        super().__init__()
        self._settlement_context = None

    @property
    def settlement_context(self) -> BBSSettlementContext:
        return self._settlement_context

    def setup_settlement_context(self, head_of_settlement_sim_info: SimInfo) -> BBRunResult:
        if self.settlement_context is not None:
            return BBRunResult(True, 'Settlement context already running.')
        member_contexts = list()
        member_contexts.append(BBSSettlementMemberContext(
            head_of_settlement_sim_info,
            BBSSettlementMemberJobFlags.NONE,
            True
        ))
        for sim_info in self._find_settlement_member_sim_infos_gen():
            member_contexts.append(BBSSettlementMemberContext(
                sim_info,
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
        if self.settlement_context is None:
            if head_of_settlement_sim_info is None:
                head_of_settlement_sim_info = self._find_settlement_head_sim_info()
            setup_result = self.setup_settlement_context(head_of_settlement_sim_info or sim_info)
            if not setup_result:
                return setup_result

        self.settlement_context.add_member_context(
            BBSSettlementMemberContext(
                sim_info,
                BBSSettlementMemberJobFlags.NONE,
                False
            )
        )
        return BBRunResult(True, 'Finished setting up context.')

    def _find_settlement_head_sim_info(self) -> Union[SimInfo, None]:
        for sim_info in BBSimUtils.get_all_sim_info_gen():
            if BBSimTraitUtils.has_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD):
                return sim_info

    def _find_settlement_member_sim_infos_gen(self) -> Iterable[SimInfo]:
        for sim_info in BBSimUtils.get_all_sim_info_gen():
            if BBSimTraitUtils.has_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER):
                yield sim_info
