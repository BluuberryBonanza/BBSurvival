"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from crafting.recipe import Recipe
from requirecookingingredients.mod_identity import ModIdentity


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

log = BBLogRegistry().register_log(ModIdentity(), 'rci_ingredients_required_test')
log.enable()


@BBInjectionUtils.inject(ModIdentity(), Recipe, 'all_ingredients_required')
def _rci_set_all_ingredients_required(original, cls, *_, **__):
    global excluded_recipes
    log.debug('wasadsadasdasdas')
    recipe_id = getattr(cls, 'guid64', None)
    log.debug('Got id', recipe_id=recipe_id, class_name=cls, class_dir=dir(cls))
    if recipe_id in excluded_recipes:
        return original(*_, **__)
    return False


# @BBInjectionUtils.inject(ModIdentity(), Recipe, Recipe._tuning_loaded_callback.__name__)
def _rci_make_ingredients_required(original, cls, *_, **__):
    recipe_id = getattr(cls, 'guid64', None)
    log.debug('Got id', recipe_id=recipe_id, class_name=cls, class_dir=dir(cls))
    # if recipe_id in excluded_recipes:
    #     return original(*_, **__)
    if cls.use_ingredients is not None:
        cls.use_ingredients.all_ingredients_required = True
    return original(*_, **__)
