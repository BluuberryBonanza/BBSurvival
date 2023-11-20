"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any, List, Union

from bbsurvival.mod_identity import ModIdentity
from bbsurvival.prologue.bbs_prologue_data import BBSPrologueData
from bbsurvival.settlement.enums.trait_ids import BBSSettlementTraitId
from bluuberrylibrary.classes.bb_test_result import BBTestResult
from bluuberrylibrary.interactions.classes.bb_super_interaction import BBSuperInteraction
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from crafting.crafting_interactions import StartCraftingAutonomouslySuperInteraction
from crafting.crafting_process import CraftingProcess
from crafting.recipe import Recipe
from event_testing.results import TestResult
from interactions.context import InteractionContext
from objects.game_object import GameObject
from sims.sim import Sim
from sims.sim_info import SimInfo


class BBSSettlementCookAutonomouslyInteraction(StartCraftingAutonomouslySuperInteraction, BBSuperInteraction):
    """Cook autonomously"""

    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'bbs_cook_autonomously'

    def __init__(self, *_, **__):
        super().__init__(*_, **__)
        BBSuperInteraction.__init__(self, *_, **__)

    @classmethod
    def bbl_test(cls, interaction_sim_info: SimInfo, interaction_target: GameObject, interaction_context: InteractionContext, *args, **kwargs) -> BBTestResult:
        if not BBSPrologueData().is_mod_fully_active():
            return BBTestResult.NONE
        log = cls.get_log()
        if not BBSimTraitUtils.has_trait(interaction_sim_info, BBSSettlementTraitId.SETTLEMENT_COOK):
            return BBTestResult.NONE
        # log.debug('Sim tried to do this', clas=cls, sim=interaction_sim_info)
        return BBTestResult.TRUE

    @classmethod
    def _test(cls, target: Any, context: InteractionContext, **kwargs) -> TestResult:
        log = cls.get_log()
        try:
            sim_info = BBSimUtils.to_sim_info(context.sim)
            target_sim_info = target
            if target_sim_info is not None and isinstance(target_sim_info, Sim):
                target_sim_info = BBSimUtils.to_sim_info(target_sim_info)
            test_result = cls.bbl_test(sim_info, target_sim_info, context, **kwargs)
            if not test_result:
                return test_result.to_base()
        except Exception as ex:
            log.error(f'Error happened while running bbl_test of \'{cls.__name__}\'.', exception=ex)
            return TestResult(False, f'An error happened running bbl_test {ex}.')

        try:
            super_result = super()._test(target, context, **kwargs)
            log.debug('Got super result', super_result=super_result, me=cls)
            return super_result
        except Exception as ex:
            log.error(f'Error happened while running _test of \'{cls.__name__}\'.', exception=ex)
            return TestResult(False, f'An error happened running _test {ex}.')

    def _run_interaction_gen(self, timeline):
        log = self.get_log()
        self._set_orderers(self.sim)
        candidate_ingredients = self._get_ingredient_candidates(self.sim, crafting_target=self.target)
        valid_recipes = self.get_valid_recipe_list(candidate_ingredients=candidate_ingredients, ingredient_cost_only=self.ingredient_cost_only)
        recipe = self.find_best_recipe(valid_recipes)
        if recipe is None:
            log.debug('No valid recipe found.')
            return False
        handle_result = self._handle_begin_crafting(recipe, self.sim, orderer_ids=self.orderer_ids, funds_source=self.funds_source, ingredient_cost_only=self.ingredient_cost_only)
        log.debug('Got handle result', handle_result=handle_result)
        return handle_result

    def find_best_recipe(self, valid_recipes: List[Recipe]) -> Union[Recipe, None]:
        log = self.get_log()
        weights = []
        for recipe in valid_recipes:
            result = CraftingProcess.recipe_test(self.target, self.context, recipe, self.sim, 0, build_error_list=False, from_autonomy=True, check_bucks_costs=False)
            if result:
                log.debug('Tested recipe and passed.', recipe=recipe, result=result)
                # The "or 1" part is to fix recipes that SHOULD be able to be done autonomously, but for some reason EA set the autonomy_weight to zero!
                weights.append(((recipe.calculate_autonomy_weight(self.sim) or 0) + 1, recipe))
            else:
                log.debug('Failed recipe', recipe=recipe, result=result, result_errors=result.errors)
        if not weights:
            log.debug('Failed to find recipes to pick for', me=self)
            return
        import sims4.random
        recipe = sims4.random.pop_weighted(weights)
        return recipe
