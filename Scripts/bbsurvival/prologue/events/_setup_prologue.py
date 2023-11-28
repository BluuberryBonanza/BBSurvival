"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.bb_lib.utils.bb_sim_inventory_utils import BBSimInventoryUtils
from bbsurvival.bb_lib.utils.bb_sim_species_utils import BBSimSpeciesUtils
from bbsurvival.enums.object_definition_ids import BBSObjectDefinitionId
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_end_event import BBOnZoneLoadEndEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils


@BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadEndEvent)
def _bbs_setup_settlement_on_zone_load(event: BBOnZoneLoadEndEvent) -> BBRunResult:
    survival_manual_definition_id = BBSObjectDefinitionId.SURVIVAL_MANUAL
    for sim_info in BBSimUtils.get_all_sim_info_gen():
        if not BBSimSpeciesUtils.is_human(sim_info):
            continue
        if BBSimInventoryUtils.has_inventory_item_by_definition(sim_info, survival_manual_definition_id):
            continue
        BBSimInventoryUtils.create_in_inventory(sim_info, survival_manual_definition_id)
    return BBRunResult.TRUE
