"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.settlement.enums.settlement_member_job import BBSSettlementMemberJobFlags
from bbsurvival.settlement.contexts.settlement_context_manager import BBSSettlementContextManager
from bluuberrylibrary.classes.bb_test_result import BBTestResult
from bluuberrylibrary.interactions.classes.bb_social_mixer_interaction import BBSocialMixerInteraction
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from interactions.context import InteractionContext
from sims.sim_info import SimInfo
from sims4.tuning.tunable import TunableEnumEntry


class BBSSettlementUnassignFromJobInteraction(BBSocialMixerInteraction):
    """Unassign a job from a settlement member."""
    INSTANCE_TUNABLES = {
        'settlement_job': TunableEnumEntry(
            description='\n            The job to unassign.\n            ',
            tunable_type=BBSSettlementMemberJobFlags,
            default=BBSSettlementMemberJobFlags.NONE
        ),
    }

    __slots__ = {'settlement_job'}

    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'bbs_unassign_from_job'

    @classmethod
    def bbl_test(cls, interaction_sim_info: SimInfo, interaction_target_sim_info: SimInfo, interaction_context: InteractionContext, *args, **kwargs) -> BBTestResult:
        log = cls.get_log()
        settlement_context = BBSSettlementContextManager().get_settlement_context_by_sim_info(interaction_target_sim_info)
        if settlement_context is None:
            log.debug('No settlement context.')
            return BBTestResult.NONE
        if not settlement_context.has_member_context(interaction_sim_info):
            log.debug('Source Sim is not a part of the target Sims settlement.', sim=interaction_sim_info, target=interaction_target_sim_info)
            return BBTestResult.NONE
        target_context = settlement_context.get_member_context(interaction_target_sim_info)
        if target_context is None or not target_context.has_any_jobs(cls.settlement_job):
            return BBTestResult.NONE
        return super().bbl_test(interaction_sim_info, interaction_target_sim_info, interaction_context, *args, **kwargs)
