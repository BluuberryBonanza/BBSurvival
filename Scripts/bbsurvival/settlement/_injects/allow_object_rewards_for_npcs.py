"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from collections import Counter
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.settlement.utils.settlement_utils import BBSSettlementUtils
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from interactions.object_rewards import ObjectRewardsOperation
from sims.sim import Sim
from sims4.localization import LocalizationHelperTuning


@BBInjectionUtils.inject(ModIdentity(), ObjectRewardsOperation, ObjectRewardsOperation._apply_to_subject_and_target.__name__)
def _bbs_override_object_rewards_operation(original, self, subject: Sim, target, resolver, placement_override_func=None, post_object_create_func=None):
    if not subject.is_npc:
        return original(self, subject, target, resolver, placement_override_func=placement_override_func, post_object_create_func=post_object_create_func)

    subject_sim_info = BBSimUtils.to_sim_info(subject)
    if not BBSSettlementUtils.is_settlement_member(subject_sim_info) and not BBSSettlementUtils.is_head_of_settlement(subject_sim_info):
        return original(self, subject, target, resolver, placement_override_func=placement_override_func, post_object_create_func=post_object_create_func)

    obj_counter = Counter()
    for object_reward in self._object_rewards:
        quantity = object_reward.quantity
        quantity += object_reward.tested_bonus_quantity.get_modified_value(resolver)
        for _ in range(int(quantity)):
            weight_pairs = [(data.weight, (data.reward, data.states_on_reward_object, data.quantity)) for data in object_reward.reward_objects]
            self._create_object_rewards(
                weight_pairs,
                obj_counter,
                resolver,
                subject=subject,
                placement_override_func=placement_override_func,
                post_object_create_func=post_object_create_func
            )
    if obj_counter and self._notification is not None:
        obj_names = [LocalizationHelperTuning.get_object_count(count, obj) for (obj, count) in obj_counter.items()]
        dialog = self._notification(subject, resolver=resolver)
        dialog.show_dialog(additional_tokens=(LocalizationHelperTuning.get_bulleted_list((None,), *obj_names),))
    return True
