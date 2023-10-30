"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.settlement.enums.trait_ids import BBSSettlementTraitId
from bbsurvival.settlement.settlement_context_manager import BBSSettlementContextManager
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.events.event_dispatchers.sim.events.bb_on_sim_spawned_event import BBOnSimSpawnedEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils


@BBEventHandlerRegistry.register(ModIdentity(), BBOnSimSpawnedEvent)
def _bbs_setup_settlement_on_settlement_head_spawned(event: BBOnSimSpawnedEvent) -> BBRunResult:
    if BBSimTraitUtils.has_trait(event.sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD):
        BBSSettlementContextManager().setup_settlement_context(event.sim_info)
    return BBRunResult.TRUE
