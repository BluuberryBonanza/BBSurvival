"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.bb_lib.utils.bb_sim_inventory_utils import BBSimInventoryUtils
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.settlement.contexts.settlement_context_manager import BBSSettlementContextManager
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.classes.bb_test_result import BBTestResult
from bluuberrylibrary.interactions.classes.bb_social_super_interaction import BBSocialSuperInteraction
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from interactions.context import InteractionContext
from interactions.interaction_finisher import FinishingType
from sims.sim_info import SimInfo


class BBSSettlementDropOffInventoryInteraction(BBSocialSuperInteraction):
    """Drop off inventory of a Sim into another Sims inventory."""
    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'bbs_drop_off_inventory'

    @classmethod
    def bbl_test(cls, interaction_sim_info: SimInfo, interaction_target_sim_info: SimInfo, interaction_context: InteractionContext, *args, **kwargs) -> BBTestResult:
        is_autonomous = interaction_context.source == InteractionContext.SOURCE_AUTONOMY
        if is_autonomous:
            if not interaction_sim_info.is_npc:
                # cls.get_log().debug('Household Sim attempted to autonomously drop off supplies. We will ignore it.', sim=interaction_sim_info)
                return BBTestResult.NONE

        cls.get_log().debug('Sim is doing it', sim=interaction_sim_info)
        source_sim_settlement_context = BBSSettlementContextManager().get_settlement_context_by_sim_info(interaction_sim_info)
        target_sim_settlement_context = BBSSettlementContextManager().get_settlement_context_by_sim_info(interaction_target_sim_info)
        if source_sim_settlement_context is None or target_sim_settlement_context is None:
            cls.get_log().debug('No settlement context for either Sim.', sim=interaction_sim_info, target=interaction_target_sim_info)
            return BBTestResult.NONE
        if source_sim_settlement_context is not target_sim_settlement_context:
            cls.get_log().debug('Source Sim and Target Sim are not in the same settlement.', source_sim=interaction_sim_info, target_sim=interaction_target_sim_info)
            return BBTestResult.NONE
        if not BBSimInventoryUtils.has_any_inventory_items(interaction_sim_info):
            cls.get_log().debug('Source Sim has no items in their inventory.', source_sim=interaction_sim_info)
            return BBTestResult.NONE
        cls.get_log().debug('Sim is trying to drop off their inventory.', sim=interaction_sim_info, target_sim=interaction_target_sim_info)
        return BBTestResult.TRUE

    def bbl_cancelled(self, interaction_sim_info: SimInfo, interaction_target_sim_info: SimInfo, interaction_context: InteractionContext, finishing_type: FinishingType, cancel_reason: str, **kwargs) -> BBRunResult:
        log = self.get_log()
        log.debug('Cancelled because reasons', sim=interaction_sim_info, target=interaction_target_sim_info, finishing_type=finishing_type, cancel_reason=cancel_reason, kwargles=kwargs)
        return BBRunResult.TRUE