"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import functools
from typing import List

import services
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from crafting.crafting_ingredients import IngredientTuning, IngredientTooltipStyle
from crafting.crafting_interactions import StartCraftingMixin, StartCraftingAutonomouslySuperInteraction, \
    StartCraftingSuperInteraction, StartCraftingOrderSuperInteraction
from crafting.crafting_process import CraftingProcess
from crafting.crafting_tunable import CraftingTuning
from crafting.recipe import Recipe
from event_testing.results import TestResult
from requirecookingingredients.mod_identity import ModIdentity
from sims4.localization import LocalizationHelperTuning
from sims4.utils import classproperty, flexmethod
from singletons import DEFAULT

original_start_crafting_super_interaction_picker_rows_gen = StartCraftingSuperInteraction.picker_rows_gen

log = BBLogRegistry().register_log(ModIdentity(), 'rci_ingredients')

class _NewRecipeClass:
    excluded_recipes = (
        236756,  # recipe_Drink_JuiceFizzing_FizzyJuice_Single_Confident
        236746,  # recipe_Drink_JuiceFizzing_FizzyJuice_Multi_Confident
        236757,  # recipe_Drink_JuiceFizzing_FizzyJuice_Single_Energized
        236747,  # recipe_Drink_JuiceFizzing_FizzyJuice_Multi_Energized
        236758,  # recipe_Drink_JuiceFizzing_FizzyJuice_Single_Flirty
        236748,  # recipe_Drink_JuiceFizzing_FizzyJuice_Multi_Flirty
        236759,  # recipe_Drink_JuiceFizzing_FizzyJuice_Single_Focused
        236750,  # recipe_Drink_JuiceFizzing_FizzyJuice_Multi_Focused
        233721,  # recipe_Drink_JuiceFizzing_FizzyJuice_Single_Happy
        233720,  # recipe_Drink_JuiceFizzing_FizzyJuice_Multi_Happy
        236760,  # recipe_Drink_JuiceFizzing_FizzyJuice_Single_Honey
        236754,  # recipe_Drink_JuiceFizzing_FizzyJuice_Multi_Honey
        236761,  # recipe_Drink_JuiceFizzing_FizzyJuice_Single_Inspired
        236749,  # recipe_Drink_JuiceFizzing_FizzyJuice_Multi_Inspired
        236762,  # recipe_Drink_JuiceFizzing_FizzyJuice_Single_Plasma
        236752,  # recipe_Drink_JuiceFizzing_FizzyJuice_Multi_Plasma
        236763,  # recipe_Drink_JuiceFizzing_FizzyJuice_Single_Playful
        236751,  # recipe_Drink_JuiceFizzing_FizzyJuice_Multi_Playful
        236764,  # recipe_Drink_JuiceFizzing_FizzyJuice_Single_Strange
        236753,  # recipe_Drink_JuiceFizzing_FizzyJuice_Multi_Strange
        236765,  # recipe_Drink_JuiceFizzing_FizzyJuice_Single_Tofizz
        236755,  # recipe_Drink_JuiceFizzing_FizzyJuice_Multi_Tofizz
        236798,  # recipe_Drink_JuiceFizzing_Kombucha_Single_Floral
        236801,  # recipe_Drink_JuiceFizzing_Kombucha_Multi_Floral
        236799,  # recipe_Drink_JuiceFizzing_Kombucha_Single_Herbal
        236802,  # recipe_Drink_JuiceFizzing_Kombucha_Multi_Herbal
        236800,  # recipe_Drink_JuiceFizzing_Kombucha_Single_Grimbucha
        236803,  # recipe_Drink_JuiceFizzing_Kombucha_Multi_Grimbucha
        236823,  # recipe_Drink_JuiceFizzing_SuspiciousFizz_Single
        236822,  # recipe_Drink_JuiceFizzing_SuspiciousFizz_Multi
    )

    EXCLUDED_INTERACTION_IDS = (
        237125,  # juiceFizzer_StartCrafting_StartFizzing
        237209,  # juiceFizzer_StartCrafting_StartFizzingSeltzer
    )

    def all_ingredients_required(cls):  # cls here is actually "Recipe" and not "_NewRecipeClass
        recipe_id = getattr(cls, 'guid64', None)
        if recipe_id in _NewRecipeClass.excluded_recipes:
            if cls.use_ingredients is None:
                return False
            from crafting.recipe import debug_ingredient_requirements
            return cls.use_ingredients.all_ingredients_required and debug_ingredient_requirements
        return True

    def rci_picker_rows_gen(cls, inst, target, context, crafter=DEFAULT, order_count=1, recipe_ingredients_map=None, funds_source=None, **kwargs):
        original_result = None
        try:
            interaction_id = getattr(cls, 'guid64', None)
            log.debug('Got it', clas=cls, inst=inst, interaction_id=interaction_id)
            kwargs_to_pass = original_start_crafting_super_interaction_picker_rows_gen.keywords
            original_result = original_start_crafting_super_interaction_picker_rows_gen.func(
                cls,
                inst,
                target,
                context,
                **kwargs_to_pass,
                crafter=crafter,
                order_count=order_count,
                recipe_ingredients_map=recipe_ingredients_map,
                funds_source=funds_source,
                **kwargs
            )
            if interaction_id in _NewRecipeClass.EXCLUDED_INTERACTION_IDS:
                yield from original_result
            else:
                log.debug('original result', original_result=original_result)

                crafter_other = context.sim
                is_ingredients_only = cls.ingredient_cost_only
                subclass_of_order_interaction = issubclass(cls, StartCraftingOrderSuperInteraction)
                inventory_target = target
                if crafter_other is DEFAULT and subclass_of_order_interaction and cls.ingredient_source and inst is not None:
                    recipe_list = inst.get_valid_recipe_list()
                else:
                    recipe_list = cls.recipes
                candidate_ingredients = cls._get_ingredient_candidates(crafter_other, crafting_target=inventory_target)
                hashable_recipe_list = tuple(recipe_list)
                hashable_candidate_ingredients = tuple(candidate_ingredients)
                (recipe_to_requirements_map, requirements_to_candidates_map) = cls._prebuild_recipe_requirement_candidate_maps(hashable_recipe_list, hashable_candidate_ingredients, is_ingredients_only)
                recipe_ingredients_map_other = {}
                for recipe_picker_row in original_result:
                    recipe = recipe_picker_row.tag
                    log.debug('Original val', original_result_val=recipe_picker_row, recipe=recipe, recipe_to_requirements_map=recipe_to_requirements_map.get(recipe, tuple()))
                    has_required_ingredients = True
                    requirements_for_recipe = cls._try_build_ingredient_requirements_for_recipe(recipe, recipe_to_requirements_map, requirements_to_candidates_map)
                    recipe_ingredients_map_other[recipe] = requirements_for_recipe
                    if recipe.use_ingredients is not None or is_ingredients_only:
                        ingredient_requirements = tuple(ingredient_requirement() for ingredient_requirement in recipe_to_requirements_map.get(recipe, tuple()))
                        ingredients_used = {}
                        ingredients_found_count = 0
                        ingredients_needed_count = 0
                        for ingredient_requirement in ingredient_requirements:
                            ingredient_requirement.attempt_satisfy_ingredients(candidate_ingredients, ingredients_used)
                            ingredients_found_count += ingredient_requirement.count_satisfied
                            ingredients_needed_count += ingredient_requirement.count_required

                        if ingredients_found_count < ingredients_needed_count:
                            has_required_ingredients = False
                            recipe_picker_row.is_enable = False
                        ingredients_display_data = tuple(ingredient_requirement.get_display_data() for ingredient_requirement in ingredient_requirements)
                        recipe_picker_row.ingredients = ingredients_display_data
                        tooltip_ingredients = [ingredient.ingredient_name for ingredient in recipe_picker_row.ingredients]
                        ingredients_comma_list = LocalizationHelperTuning.get_comma_separated_list(*tooltip_ingredients)
                        ingredients_list_string = LocalizationHelperTuning.get_bulleted_list((None,), *tooltip_ingredients)
                        tooltip = functools.partial(IngredientTuning.REQUIRED_INGREDIENT_LIST_STRING, ingredients_list_string)
                        if not has_required_ingredients:
                            tooltip_style = None
                            if is_ingredients_only and recipe.ingredient_cost_only_ingredients is not None:
                                tooltip_style = recipe.ingredient_cost_only_ingredients.missing_ingredient_tooltip_style
                            elif recipe.use_ingredients is not None:
                                tooltip_style = recipe.use_ingredients.missing_ingredient_tooltip_style
                            log.debug('Got tooltip style', tooltip_style)
                            recipe_picker_row.row_description = IngredientTuning.REQUIRED_INGREDIENT_LIST_STRING(ingredients_list_string)
                        if recipe.recipe_description:
                            tooltip = functools.partial(LocalizationHelperTuning.RAW_TEXT, LocalizationHelperTuning.get_new_line_separated_strings(recipe.recipe_description(crafter), tooltip()))
                        recipe_picker_row.row_tooltip = tooltip
                        recipe_picker_row.ingredients_list = ingredients_comma_list
                    else:
                        log.debug('Not making required', recipe=recipe)
                    yield recipe_picker_row
        except Exception as ex:
            log.error('An error occurred while generating crafting recipes', interaction=cls, exception=ex)
            if original_result is not None:
                yield from original_result


StartCraftingSuperInteraction.picker_rows_gen = flexmethod(_NewRecipeClass.rci_picker_rows_gen)


# Recipe.all_ingredients_required = classproperty(_NewRecipeClass.all_ingredients_required)

original_start_crafting_function = StartCraftingMixin.get_default_candidate_ingredients


def _start_crafting_override(crafter, check_sim_inventory=True, check_fridge_shared_inventory=True):
    original_result = list(original_start_crafting_function(crafter, check_sim_inventory=check_sim_inventory, check_fridge_shared_inventory=check_fridge_shared_inventory))
    log.debug('Got things', crafter=crafter, check_sim_inventory=check_sim_inventory, check_fridge_shared_inventory=check_fridge_shared_inventory, original_ingredients=original_result)
    if check_sim_inventory and check_fridge_shared_inventory:
        fridge_inventory = services.active_lot().get_object_inventories(CraftingTuning.SHARED_FRIDGE_INVENTORY_TYPE)[0]
        if fridge_inventory is not None:
            for obj in fridge_inventory:
                if obj.definition.has_build_buy_tag(IngredientTuning.INGREDIENT_TAG):
                    original_result.append(obj)
    return original_result


# StartCraftingMixin.get_default_candidate_ingredients = _start_crafting_override


autonomous_log = BBLogRegistry().register_log(ModIdentity(), 'rci_ingredients_autonomously')


@BBInjectionUtils.inject(ModIdentity(), StartCraftingAutonomouslySuperInteraction, StartCraftingAutonomouslySuperInteraction._autonomous_test.__name__)
def _rci_override_autonomous_crafting_interaction(original, cls, target, context, who):
    # original_result = original(target, context, who)
    # autonomous_log.debug('Original result', clas=cls, original_result=original_result, target=target, context=context, who=who)
    # return original_result
    interaction_id = getattr(cls, 'guid64', None)
    autonomous_log.debug('Got it', clas=cls, interaction_id=interaction_id)
    if interaction_id in _NewRecipeClass.EXCLUDED_INTERACTION_IDS:
        return original(target, context, who)
    food_restriction_tracker = who.sim_info.food_restriction_tracker
    candidate_ingredients = cls._get_ingredient_candidates(who, crafting_target=target)
    for recipe in cls.recipes:
        if food_restriction_tracker is not None and food_restriction_tracker.recipe_has_restriction(recipe):
            pass
        else:
            result = CraftingProcess.recipe_test(target, context, recipe, who, 0, build_error_list=False, from_autonomy=True, check_bucks_costs=False)
            if cls.ingredient_cost_only and not recipe.all_ingredients_available(candidate_ingredients, cls.ingredient_cost_only):
                # autonomous_log.debug('Did autonomous test, but not all ingredients were available.', ingredient_cost_only=cls.ingredient_cost_only, recipe=recipe)
                pass
            elif result:
                # autonomous_log.debug('Dis autonomous test, success', recipe=recipe)
                return TestResult.TRUE
            else:
                # autonomous_log.debug('Did autonomous test, result failed', recipe=recipe, result=result)
                pass
    return TestResult(False, 'There are no autonomously completable recipes.')
    # original_result = original(target, context, who)
    #
    # return original_result


@BBInjectionUtils.inject(ModIdentity(), StartCraftingMixin, StartCraftingMixin.find_best_recipe.__name__)
def _rci_handle_begin_crafting(original, self, valid_recipes: List[Recipe]):
    weights = []
    for recipe in valid_recipes:
        result = CraftingProcess.recipe_test(self.target, self.context, recipe, self.sim, 0, build_error_list=autonomous_log.is_enabled(), from_autonomy=True, check_bucks_costs=False)
        if result:
            autonomous_log.debug('Tested recipe and passed.', recipe=recipe, result=result)
            weights.append((recipe.calculate_autonomy_weight(self.sim), recipe))
        else:
            autonomous_log.debug('Failed recipe', recipe=recipe, result=result, result_errors=result.errors)
    if not weights:
        autonomous_log.debug('Unable to "find best recipe".', valid_recipes=valid_recipes)
        return
    import sims4.random
    recipe = sims4.random.pop_weighted(weights)
    return recipe
