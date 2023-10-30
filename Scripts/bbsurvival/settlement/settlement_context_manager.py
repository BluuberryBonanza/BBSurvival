from bbsurvival.settlement.enums.settlement_member_job import BBSSettlementMemberJobFlags
from bbsurvival.settlement.enums.trait_ids import BBSSettlementTraitId
from bbsurvival.settlement.settlement_context import BBSSettlementContext
from bbsurvival.settlement.settlement_member_context import BBSSettlementMemberContext
from bluuberrylibrary.classes.bb_singleton import BBSingleton
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from sims.sim_info import SimInfo


class BBSSettlementContextManager(metaclass=BBSingleton):
    def __init__(self):
        super().__init__()
        self._settlement_context = None

    @property
    def settlement_context(self):
        return self._settlement_context

    def setup_settlement_context(self, head_of_settlement_sim_info: SimInfo):
        if self.settlement_context is not None:
            return
        member_contexts = list()
        member_contexts.append(BBSSettlementMemberContext(
            head_of_settlement_sim_info,
            BBSSettlementMemberJobFlags.NONE,
            True
        ))
        for sim_info in BBSimUtils.get_all_sim_info_gen():
            if BBSimTraitUtils.has_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER):
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
