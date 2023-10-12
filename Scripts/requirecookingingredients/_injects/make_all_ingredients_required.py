"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from crafting.recipe import Recipe
from requirecookingingredients.mod_identity import ModIdentity


@BBInjectionUtils.inject(ModIdentity(), Recipe, 'all_ingredients_required')
def _rci_set_all_ingredients_required(original, *_, **__):
    return True
