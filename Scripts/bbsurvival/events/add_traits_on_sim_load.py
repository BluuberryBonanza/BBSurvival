"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.enums.trait_ids import BBSTraitId
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.events.event_dispatchers.sim.events.bb_on_sim_spawned_event import BBOnSimSpawnedEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils


@BBEventHandlerRegistry.register(ModIdentity(), BBOnSimSpawnedEvent)
def _bbs_add_off_the_grid_on_zone_load(event: BBOnSimSpawnedEvent):
    return BBSimTraitUtils.add_trait(event.sim_info, BBSTraitId.MAIN_HUMAN)
