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
from sims.sim_info import SimInfo


class BBSScavengeQuickInteraction(BBSuperInteraction):
    """Scavenge quickly for supplies."""

    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'bbs_scavenge_quick_interaction'

    def bbl_started(self, interaction_sim_info: SimInfo, interaction_target: Any) -> BBTestResult:
        def _on_leave_rabbit_hole(_sim_info: SimInfo, cancelled: bool):
            if cancelled:
                return
            try:
                BBSScavengingUtils.give_scavenge_rewards(_sim_info, BBSScavengingRunLength.QUICK)
            except Exception as ex:
                self.get_log().error('An error occurred while giving scavenging rewards.', exception=ex)

        success = BBSimRabbitHoleUtils.send_into_rabbit_hole(interaction_sim_info, BBSRabbitHoleId.SCAVENGE_QUICK, on_leave_rabbit_hole=_on_leave_rabbit_hole)

        if success:
            return BBTestResult.TRUE
        return BBTestResult(False, success.reason)
