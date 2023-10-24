"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any

from bbsurvival.bb_lib.utils.bb_sim_rabbit_hole_utils import BBSimRabbitHoleUtils
from bbsurvival.enums.rabbit_hole_ids import BBSRabbitHoleId
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.scavenging.bbs_scavenging_run_length import BBSScavengingRunLength
from bbsurvival.scavenging.scavenging_utils import BBSScavengingUtils
from bluuberrylibrary.classes.bb_test_result import BBTestResult
from bluuberrylibrary.interactions.classes.bb_super_interaction import BBSuperInteraction
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from interactions.context import InteractionContext
from sims.sim_info import SimInfo
from sims4.tuning.tunable import TunableEnumEntry


class BBSScavengeInteraction(BBSuperInteraction):
    """Scavenge quickly for supplies."""
    INSTANCE_TUNABLES = {
        'run_length': TunableEnumEntry(
            description='\n            The length of the run.\n            ',
            tunable_type=BBSScavengingRunLength,
            default=BBSScavengingRunLength.QUICK
        ),
    }

    __slots__ = {'run_length'}

    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'bbs_scavenge_quick_interaction'

    RUN_LENGTH_TO_RABBIT_HOLE = {
        BBSScavengingRunLength.QUICK: BBSRabbitHoleId.SCAVENGE_QUICK,
        BBSScavengingRunLength.MODERATE: BBSRabbitHoleId.SCAVENGE_MODERATE,
        BBSScavengingRunLength.LONG: BBSRabbitHoleId.SCAVENGE_LONG
    }

    @classmethod
    def bbl_test(cls, interaction_sim_info: SimInfo, interaction_target_sim_info: SimInfo, interaction_context: InteractionContext, *args, **kwargs) -> BBTestResult:
        if interaction_sim_info is not interaction_target_sim_info:
            cls.get_log().debug('Sim is not target', interaction_sim=interaction_sim_info, target=interaction_target_sim_info)
            return BBTestResult.NONE
        return super().bbl_test(interaction_sim_info, interaction_target_sim_info, interaction_context, *args, **kwargs)

    def bbl_started(self, interaction_sim_info: SimInfo, interaction_target_sim_info: Any) -> BBTestResult:
        def _on_leave_rabbit_hole(_sim_info: SimInfo, cancelled: bool):
            if cancelled:
                return
            try:
                BBSScavengingUtils.give_scavenge_rewards(_sim_info, self.run_length)
            except Exception as ex:
                self.get_log().error('An error occurred while giving scavenging rewards.', exception=ex)

        self.get_log().debug('Got Sim', interaction_sim=interaction_sim_info, target=interaction_target_sim_info)

        success = BBSimRabbitHoleUtils.send_into_rabbit_hole(interaction_target_sim_info, self.RUN_LENGTH_TO_RABBIT_HOLE[self.run_length], on_leave_rabbit_hole=_on_leave_rabbit_hole)

        if success:
            return BBTestResult.TRUE
        return BBTestResult(False, success.reason)
