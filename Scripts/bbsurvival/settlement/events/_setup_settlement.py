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
from bbsurvival.settlement.contexts.settlement_context_manager import BBSSettlementContextManager
from bbsurvival.settlement.utils.settlement_utils import BBSSettlementUtils
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.events.event_dispatchers.sim.events.bb_on_sim_died_event import BBOnSimDiedEvent
from bluuberrylibrary.events.event_dispatchers.sim.events.bb_on_sim_resurrected_event import BBOnSimResurrectedEvent
from bluuberrylibrary.events.event_dispatchers.sim.events.bb_on_sim_spawned_event import BBOnSimSpawnedEvent
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_end_event import BBOnZoneLoadEndEvent
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_unload_start_event import BBOnZoneUnloadStartEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils

log = BBLogRegistry().register_log(ModIdentity(), 'bbs_settlement_events')
# log.enable()


@BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadEndEvent)
def _bbs_setup_settlement_on_zone_load(event: BBOnZoneLoadEndEvent) -> BBRunResult:
    return BBSSettlementContextManager().add_missing_settlement_member_contexts()


@BBEventHandlerRegistry.register(ModIdentity(), BBOnSimSpawnedEvent)
def _bbs_add_member_context_on_sim_spawned(event: BBOnSimSpawnedEvent) -> BBRunResult:
    sim_info = event.sim_info
    settlement_context = BBSSettlementContextManager().get_settlement_context_for_current_zone()
    if settlement_context is None:
        settlement_context = BBSSettlementContextManager().setup_settlement_context_for_current_zone()
        if settlement_context is None:
            return BBRunResult.TRUE

    settlement_member_context = settlement_context.get_member_context(sim_info)
    if settlement_member_context is not None:
        if settlement_member_context.is_head_of_settlement:
            BBSimTraitUtils.add_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD)
        else:
            BBSimTraitUtils.add_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER)
        settlement_member_context.setup()
        return BBRunResult.TRUE

    sim_household = BBSimHouseholdUtils.get_household(sim_info)
    current_zone_id = services.current_zone_id()
    home_zone_id = sim_household.home_zone_id
    if current_zone_id == home_zone_id:
        if sim_info.is_npc:
            settlement_context = BBSSettlementContextManager().get_settlement_context_by_sim_info(sim_info)
            if settlement_context is not None:
                if settlement_context.home_zone_id != current_zone_id:
                    return BBRunResult.TRUE
            else:
                # This is to fix npcs that are not living on the home lot.
                for _sim_info in BBSimUtils.get_all_sim_info_gen():
                    if BBSSettlementUtils.has_head_of_settlement_relationship(_sim_info, sim_info):
                        other_sim_household = BBSimHouseholdUtils.get_household(_sim_info)
                        if current_zone_id != other_sim_household.home_zone_id:
                            return BBRunResult.TRUE
        BBSSettlementContextManager().add_settlement_member_context(sim_info)
        return BBRunResult.TRUE

    head_of_settlement_sim_info = settlement_context.get_head_of_settlement_context().sim_info
    if BBSSettlementUtils.has_head_of_settlement_relationship(head_of_settlement_sim_info, sim_info):
        BBSSettlementContextManager().add_settlement_member_context(sim_info)
        return BBRunResult.TRUE
    return BBRunResult.TRUE


@BBEventHandlerRegistry.register(ModIdentity(), BBOnSimDiedEvent)
def _bbs_remove_member_context_on_sim_died(event: BBOnSimDiedEvent) -> BBRunResult:
    sim_info = event.sim_info
    log.debug('Sim has died, we are going to remove them from the settlement.', sim=sim_info)
    BBSSettlementUtils.retire_settlement_member(sim_info)
    return BBRunResult.TRUE


@BBEventHandlerRegistry.register(ModIdentity(), BBOnSimResurrectedEvent)
def _bbs_remove_member_context_on_sim_resurrect(event: BBOnSimResurrectedEvent) -> BBRunResult:
    sim_info = event.sim_info
    sim_household = BBSimHouseholdUtils.get_household(sim_info)
    current_zone_id = services.current_zone_id()
    home_zone_id = sim_household.home_zone_id
    if current_zone_id == home_zone_id:
        BBSSettlementContextManager().add_settlement_member_context(sim_info)
        return BBRunResult.TRUE
    return BBRunResult.TRUE


@BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneUnloadStartEvent)
def _bbs_teardown_settlement_on_settlement_unload(event: BBOnZoneUnloadStartEvent) -> BBRunResult:
    return BBSSettlementContextManager().teardown_settlement_context()
