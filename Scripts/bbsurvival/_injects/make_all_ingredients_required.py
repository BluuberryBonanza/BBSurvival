"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
try:
    import requirecookingingredients
except:
    # Require Cooking Ingredients not installed.
    from bbsurvival.mod_identity import ModIdentity
    from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
    from crafting.recipe import Recipe

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

    @BBInjectionUtils.inject(ModIdentity(), Recipe, 'all_ingredients_required')
    def _bbs_set_all_ingredients_required(original, cls, *_, **__):
        global excluded_recipes
        recipe_id = getattr(cls, 'guid64')
        if recipe_id in excluded_recipes:
            return original(*_, **__)
        return True
