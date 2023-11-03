"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.bb_lib.utils.bb_instance_utils import BBInstanceUtils
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from objects.components.affordance_tuning import AffordanceTuningComponent
from sims4.resources import Types

log = BBLogRegistry().register_log(ModIdentity(), 'bbs_override_affordance_tuning')


# @BBInjectionUtils.inject(ModIdentity(), AffordanceTuningComponent, '__init__')
def _bbs_add_harvestable_eating_to(original, self, *_, **__):
    original_result = original(self, *_, **__)
    interaction_id = 103820  # Gardening_EatHarvestable
    eat_harvestable_interaction = BBInstanceUtils.get_instance(Types.INTERACTION, interaction_id)
    harvestable_interaction_mapping = self._affordance_map.get(eat_harvestable_interaction, None)
    log.debug('Got mapping', mapping=harvestable_interaction_mapping, interaction=eat_harvestable_interaction)
    if harvestable_interaction_mapping is not None:
        custom_interaction_id = 3558233205551617596  # BBS_Food_Interaction_EatHarvestable
        eat_harvestable_interaction = BBInstanceUtils.get_instance(Types.INTERACTION, custom_interaction_id)
        self._affordance_map.set(eat_harvestable_interaction, harvestable_interaction_mapping)
    return original_result
