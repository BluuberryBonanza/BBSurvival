"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from crafting.crafting_ingredients import IngredientRequirement
from crafting.crafting_interactions import StartCraftingMixin
from crafting.recipe import Recipe


# @BBInjectionUtils.inject(ModIdentity(), StartCraftingMixin, StartCraftingMixin.validate_and_satisfy_ingredients.__name__)
def _bbs_make_all_ingredients_required(original, self, crafter, ingredient_requirements, all_ingredients_required=False, crafting_target=None):
    return original(self, crafter, ingredient_requirements, all_ingredients_required=True, crafting_target=crafting_target)


@BBInjectionUtils.inject(ModIdentity(), Recipe, 'all_ingredients_required')
def _bbs_set_all_ingredients_required(original, *_, **__):
    return True

# @BBInjectionUtils.inject(ModIdentity(), IngredientRequirement, 'count_required')
def _bbs_make_all_ingredients_required(original, self):
    original_value = original()
    return original_value - self.count_using
