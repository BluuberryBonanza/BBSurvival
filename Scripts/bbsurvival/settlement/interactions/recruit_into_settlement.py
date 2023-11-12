"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.settlement.contexts.settlement_context_manager import BBSSettlementContextManager
from bluuberrylibrary.classes.bb_test_result import BBTestResult
from bluuberrylibrary.interactions.classes.bb_social_mixer_interaction import BBSocialMixerInteraction
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from interactions.context import InteractionContext
from sims.sim_info import SimInfo


class BBSSettlementRecruitInteraction(BBSocialMixerInteraction):
    """Recruit a Sim into the Settlement."""
    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'bbs_recruit'

    @classmethod
    def bbl_test(cls, interaction_sim_info: SimInfo, interaction_target_sim_info: SimInfo, interaction_context: InteractionContext, *args, **kwargs) -> BBTestResult:
        settlement_context = BBSSettlementContextManager().get_settlement_context_by_sim_info(interaction_target_sim_info)
        if settlement_context is not None:
            cls.get_log().debug(f'Target Sim {interaction_target_sim_info} is already in a Settlement.')
            return BBTestResult.NONE
        cls.get_log().debug('No settlement context.')
        return super().bbl_test(interaction_sim_info, interaction_target_sim_info, interaction_context, *args, **kwargs)
