"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import services
from bbsurvival.bb_lib.utils.bb_sim_household_utils import BBSimHouseholdUtils
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.settlement.enums.trait_ids import BBSSettlementTraitId
from bbsurvival.settlement.settlement_context_manager import BBSSettlementContextManager
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.events.event_dispatchers.sim.events.bb_on_sim_spawned_event import BBOnSimSpawnedEvent
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_end_event import BBOnZoneLoadEndEvent
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_unload_start_event import BBOnZoneUnloadStartEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils


@BBEventHandlerRegistry.register(ModIdentity(), BBOnSimSpawnedEvent)
def _bbs_setup_settlement_on_settlement_head_spawned(event: BBOnSimSpawnedEvent) -> BBRunResult:
    sim_household = BBSimHouseholdUtils.get_household(event.sim_info)
    current_zone_id = services.current_zone_id()
    home_zone_id = sim_household.home_zone_id
    if BBSimTraitUtils.has_trait(event.sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD):
        if current_zone_id == home_zone_id:
            BBSSettlementContextManager().setup_settlement_context(head_of_settlement_sim_info=event.sim_info)
    elif current_zone_id == home_zone_id:
        BBSSettlementContextManager().add_settlement_member_context(event.sim_info)
    return BBRunResult.TRUE


# @BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneUnloadStartEvent)
def _bbs_setup_settlement_on_settlement_load(event: BBOnZoneLoadEndEvent) -> BBRunResult:
    current_zone_id = services.current_zone_id()
    for sim_info in BBSimUtils.get_all_sim_info_gen():
        if BBSimTraitUtils.has_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD):
            sim_household = BBSimHouseholdUtils.get_household(sim_info)
            home_zone_id = sim_household.home_zone_id
            if current_zone_id == home_zone_id:
                BBSSettlementContextManager().setup_settlement_context(sim_info)
                BBSSettlementContextManager().settlement_context.setup()
    return BBRunResult.TRUE


@BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneUnloadStartEvent)
def _bbs_teardown_settlement_on_settlement_unload(event: BBOnZoneUnloadStartEvent) -> BBRunResult:
    return BBSSettlementContextManager().teardown_settlement_context()
