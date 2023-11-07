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


class BBSSettlementAssignAsJobInteraction(BBSocialMixerInteraction):
    """Assign a job to a settlement member."""
    INSTANCE_TUNABLES = {
        'settlement_job': TunableEnumEntry(
            description='\n            The job to assign.\n            ',
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
        return 'bbs_assign_as_job'

    ENABLED_JOBS = (
        BBSSettlementMemberJobFlags.COOK,
        BBSSettlementMemberJobFlags.NANNY,
        BBSSettlementMemberJobFlags.GARDENER,
        # BBSSettlementMemberJobFlags.GUARD,
        # BBSSettlementMemberJobFlags.DOCTOR,
        BBSSettlementMemberJobFlags.SCOUT,
        BBSSettlementMemberJobFlags.SANITATION,
        BBSSettlementMemberJobFlags.MAINTENANCE,
        # BBSSettlementMemberJobFlags.TEACHER,
        BBSSettlementMemberJobFlags.GATHERER,
        BBSSettlementMemberJobFlags.RANCHER,
    )

    @classmethod
    def bbl_test(cls, interaction_sim_info: SimInfo, interaction_target_sim_info: SimInfo, interaction_context: InteractionContext, *args, **kwargs) -> BBTestResult:
        log = cls.get_log()
        settlement_context = BBSSettlementContextManager().settlement_context
        if settlement_context is None:
            log.debug('No settlement context.')
            return BBTestResult.NONE
        target_context = settlement_context.get_member_context(interaction_target_sim_info)
        if target_context is None or target_context.has_any_jobs(cls.settlement_job):
            log.debug('Target already has job.', job=cls.settlement_job)
            return BBTestResult.NONE
        if cls.settlement_job not in cls.ENABLED_JOBS:
            log.debug('Job is not enabled yet.', settlement_job=cls.settlement_job)
            return BBTestResult.NONE
        return super().bbl_test(interaction_sim_info, interaction_target_sim_info, interaction_context, *args, **kwargs)
