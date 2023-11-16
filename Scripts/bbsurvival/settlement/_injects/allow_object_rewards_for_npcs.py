"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import random
from collections import Counter

import build_buy
import element_utils
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.settlement.utils.settlement_utils import BBSSettlementUtils
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from fishing.fish_trap_interactions import FishingTrapCatchMixerInteraction
from fishing.fishing_interactions import FishingCatchMixerInteractionMixin, FishingLocationCatchMixerInteraction, \
    FishingLocationCatchOutcome
from fishing.fishing_tuning import FishingTuning
from interactions.object_rewards import ObjectRewardsOperation
from interactions.utils.outcome import InteractionOutcomeSingle
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


@BBInjectionUtils.inject(ModIdentity(), FishingCatchMixerInteractionMixin, FishingCatchMixerInteractionMixin.create_object_and_add_to_inventory.__name__)
def _bbs_override_create_object_and_add_to_inventory(original, self, sim, object_to_create, is_fish):
    sim = sim
    if not sim.is_npc:
        return original(self, sim, object_to_create, is_fish)

    sim_info = BBSimUtils.to_sim_info(sim)
    if not BBSSettlementUtils.is_settlement_member(sim_info) and not BBSSettlementUtils.is_head_of_settlement(sim_info):
        return original(self, sim, object_to_create, is_fish)

    if object_to_create is not None:
        from objects.system import create_object
        created_object = create_object(object_to_create)
        if created_object is not None:
            created_object.update_ownership(sim)
            if is_fish:
                created_object.initialize_fish(sim)
            if sim.inventory_component.can_add(created_object):
                sim.inventory_component.player_try_add_object(created_object)
            elif not build_buy.move_object_to_household_inventory(created_object):
                pass
        return created_object
    return original(self, sim, object_to_create, is_fish)


@BBInjectionUtils.inject(ModIdentity(), FishingLocationCatchMixerInteraction, FishingLocationCatchMixerInteraction._build_outcome_sequence.__name__)
def _bbs_fishing_location_catch_build_outcome_sequence(original, self):
    sim = self.sim
    if not sim.is_npc:
        return original(self)

    sim_info = BBSimUtils.to_sim_info(sim)
    if not BBSSettlementUtils.is_settlement_member(sim_info) and not BBSSettlementUtils.is_head_of_settlement(sim_info):
        return original(self)

    succeeded = self._is_successful_catch()
    object_to_create = None
    created_object = None
    sim = self.sim
    outcome_type = self.OUTCOME_TYPE_OTHER
    outcome_actions = self.fishing_outcomes.catch_nothing_outcome_actions
    prop_override = None
    pond_throw_vfx = None
    if succeeded:
        weighted_outcomes = self._get_weighted_choices()
        import sims4.random
        outcome_actions = sims4.random.weighted_random_item(weighted_outcomes)
        if outcome_actions is self.fishing_outcomes.catch_junk_outcome_actions:
            junk_info = self._get_random_junk_info()
            prop_override = junk_info.definition
            pond_throw_vfx = junk_info.throw_into_pond_vfx
        else:
            if outcome_actions is self.fishing_outcomes.catch_treasure_outcome_actions:
                object_to_create = self._get_individual_treasure_catch()
                prop_override = self.TREASURE_PROP_OBJECT
                outcome_type = self.OUTCOME_TYPE_TREASURE
            else:
                object_to_create = self._get_individual_fish_catch()
                prop_override = object_to_create
                if object_to_create is not None:
                    outcome_type = self.OUTCOME_TYPE_FISH
            if not object_to_create:
                outcome_actions = self.fishing_outcomes.catch_nothing_outcome_actions
        from objects.system import create_object
        created_object = create_object(object_to_create)
        if created_object is not None:
            created_object.update_ownership(sim)
            self.context.create_target_override = created_object
    bait_ids = None
    if self.bait is not None:
        bait_ids = (self.bait.id,)
    self.interaction_parameters['picked_item_ids'] = bait_ids
    is_fish = outcome_actions is self.fishing_outcomes.catch_fish_outcome_actions
    outcome = FishingLocationCatchOutcome(outcome_actions, prop_override, is_fish, pond_throw_vfx)

    def end(_):
        if created_object is None:
            return
        is_dialog_show = False
        if outcome_type == self.OUTCOME_TYPE_FISH:
            created_object.initialize_fish(sim)
            self._apply_caught_fish_buff(created_object)
            self._show_catch_fish_notification(sim, created_object)
            self.super_interaction.kill_and_try_reapply_bait()
            resolver = self.get_resolver()
            if self.CATCH_ENDANGERED_FISH.dialog is not None and self.CATCH_ENDANGERED_FISH.tests.run_tests(resolver):
                is_dialog_show = True
                dialog = self.CATCH_ENDANGERED_FISH.dialog(sim, resolver=resolver)

                def on_response(_dialog):
                    if _dialog.accepted:
                        for loot in self.CATCH_ENDANGERED_FISH.loots_on_ok:
                            loot.apply_to_resolver(resolver)
                        created_object.destroy(source=self, cause='Released endangered fish.')
                    else:
                        for loot in self.CATCH_ENDANGERED_FISH.loots_on_cancel:
                            loot.apply_to_resolver(resolver)
                        self._add_fish_to_inventory(created_object)

                dialog.show_dialog(on_response=on_response)
        elif outcome_type == self.OUTCOME_TYPE_TREASURE:
            self._show_catch_treasure_notification(sim, created_object)
        if not is_dialog_show:
            self._add_fish_to_inventory(created_object)

    return element_utils.build_critical_section_with_finally(outcome.build_elements(self, update_global_outcome_result=True), end)


@BBInjectionUtils.inject(ModIdentity(), FishingTrapCatchMixerInteraction, FishingTrapCatchMixerInteraction._build_outcome_sequence.__name__)
def _bbs_override_fishing_rewards(original, self):
    sim = self.sim
    if not sim.is_npc:
        return original(self)

    sim_info = BBSimUtils.to_sim_info(sim)
    if not BBSSettlementUtils.is_settlement_member(sim_info) and not BBSSettlementUtils.is_head_of_settlement(sim_info):
        return original(self)

    return _build_elements(self)


def _build_elements(the_interaction: FishingTrapCatchMixerInteraction):
    (min_catch, max_catch) = the_interaction._get_min_max_catch()
    if min_catch <= 0:
        return
    actual_catch = random.randint(min_catch, max_catch)
    sim = the_interaction.sim
    junk_count = 0
    fish_caught = []
    treasure_caught = []
    weighted_outcomes = the_interaction._get_weighted_choices()
    import sims4.random
    while len(fish_caught) + len(treasure_caught) + junk_count < actual_catch:
        outcome_actions = sims4.random.weighted_random_item(weighted_outcomes)
        if outcome_actions is the_interaction.fishing_outcomes.catch_junk_outcome_actions:
            junk_count += 1
        elif outcome_actions is the_interaction.fishing_outcomes.catch_fish_outcome_actions:
            fish = the_interaction._get_individual_fish_catch()
            if fish is not None:
                fish_caught.append(fish)
                if outcome_actions is the_interaction.fishing_outcomes.catch_treasure_outcome_actions:
                    treasure = the_interaction._get_individual_treasure_catch()
                    if treasure is not None:
                        treasure_caught.append(treasure)
        elif outcome_actions is the_interaction.fishing_outcomes.catch_treasure_outcome_actions:
            treasure = the_interaction._get_individual_treasure_catch()
            if treasure is not None:
                treasure_caught.append(treasure)
    if treasure_caught:
        outcome = InteractionOutcomeSingle(the_interaction.fishing_outcomes.catch_treasure_outcome_actions)
    elif fish_caught:
        outcome = InteractionOutcomeSingle(the_interaction.fishing_outcomes.catch_fish_outcome_actions)
    elif junk_count:
        outcome = InteractionOutcomeSingle(the_interaction.fishing_outcomes.catch_junk_outcome_actions)
    else:
        outcome = InteractionOutcomeSingle(the_interaction.fishing_outcomes.catch_nothing_outcome_actions)

    def end(_):
        resolver = the_interaction.get_resolver()
        fish_objects = []
        treasure_objects = []
        for _treasure in treasure_caught:
            treasure_object = the_interaction.create_object_and_add_to_inventory(sim, _treasure, False)
            if treasure_object is not None:
                the_interaction._apply_loots(the_interaction.per_item_loots.each_treasure_loot, resolver)
                treasure_objects.append(treasure_object)
        for _fish in fish_caught:
            fish_object = the_interaction.create_object_and_add_to_inventory(sim, _fish, True)
            if fish_object is not None:
                the_interaction._apply_loots(the_interaction.per_item_loots.each_fish_loot, resolver)
                FishingTuning.add_bait_notebook_entry(the_interaction.sim, _fish, the_interaction.get_bait())
                fish_objects.append(fish_object)
        for _ in range(junk_count):
            the_interaction._apply_loots(the_interaction.per_item_loots.each_junk_loot, resolver)
        the_interaction._trap_catch_notification(fish_objects, treasure_objects, junk_count)

    return element_utils.build_critical_section_with_finally(outcome.build_elements(the_interaction, update_global_outcome_result=True), end)