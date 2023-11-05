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
from crafting.crafting_ingredients import IngredientTuning
from crafting.crafting_interactions import StartCraftingMixin, StartCraftingAutonomouslySuperInteraction, \
    StartCraftingSuperInteraction, StartCraftingOrderSuperInteraction
from crafting.crafting_process import CraftingProcess
from crafting.crafting_tunable import CraftingTuning
from crafting.recipe import Recipe
from event_testing.results import TestResult
from requirecookingingredients.mod_identity import ModIdentity
from sims4.localization import LocalizationHelperTuning
from sims4.utils import flexmethod
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

    INCLUDED_INTERACTION_IDS = (
        # Manual
        13387,  # fridge_Cook
        13389,  # fridge_CookGourmet
        75761,  # fridge_Cook_Emotional
        74162,  # fridge_Cook_PieMenu_Breakfast_8Servings
        74163,  # fridge_Cook_PieMenu_Breakfast_1Serving
        74164,  # fridge_Cook_PieMenu_Breakfast_4Servings
        74166,  # fridge_Cook_PieMenu_Brunch_1Serving
        74167,  # fridge_Cook_PieMenu_Brunch_4Servings
        74168,  # fridge_Cook_PieMenu_Brunch_8Servings
        74171,  # fridge_Cook_PieMenu_Lunch_1Serving
        74172,  # fridge_Cook_PieMenu_Lunch_4Servings
        74173,  # fridge_Cook_PieMenu_Lunch_8Servings
        74175,  # fridge_Cook_PieMenu_Dinner_1Serving
        74176,  # fridge_Cook_PieMenu_Dinner_4Servings
        74177,  # fridge_Cook_PieMenu_Dinner_8Servings
        76891,  # fridge_Cook_PieMenu_Breakfast_1Serving_Ingredients
        76893,  # fridge_Cook_PieMenu_Breakfast_8Servings_Ingredients
        76895,  # fridge_Cook_PieMenu_Brunch_1Serving_Ingredients
        76897,  # fridge_Cook_PieMenu_Brunch_8Servings_Ingredients
        76899,  # fridge_Cook_PieMenu_Dinner_1Serving_Ingredients
        76901,  # fridge_Cook_PieMenu_Dinner_8Servings_Ingredients
        76903,  # fridge_Cook_PieMenu_Lunch_1Serving_Ingredients
        76905,  # fridge_Cook_PieMenu_Lunch_8Servings_Ingredients
        108665,  # fridge_Bake_StartCrafting
        262028,  # fridge_Bake_StartCrafting_RequiredIngredients
        164448,  # fridge_GrabSackLunch
        270682,  # fridge_GrabSackLunch_RequiredIngredients
        159768,  # fridge_Cook_PetRecipe_Homestyle
        159769,  # fridge_Cook_PetRecipe_Gourmet
        180825,  # fridge_Cook_GrandMeal_startCrafting
        261839,  # fridge_Cook_GrandMeal_startCrafting_RequiredIngredients
        247628,  # fridge_Cook_LifeStyles_HealthyFood
        261844,  # fridge_Cook_LifeStyles_HealthyFood_RequiredIngredients
        256443,  # fridge_Canning
        261810,  # fridge_Cook_RequiredIngredients
        261824,  # fridge_CookGourmet_RequiredIngredients
        261829,  # fridge_Cook_Emotional_RequiredIngredients
        258986,  # fridge_Cook_AnimalObject_Create_LivestockFeed
        261924,  # fridge_Cook_PieMenu_Breakfast_1Serving_RequiredIngredients
        261925,  # fridge_Cook_PieMenu_Breakfast_8Servings_RequiredIngredients
        261929,  # fridge_Cook_PieMenu_Brunch_1Serving_RequiredIngredients
        261930,  # fridge_Cook_PieMenu_Brunch_8Servings_RequiredIngredients
        261931,  # fridge_Cook_PieMenu_Dinner_1Serving_RequiredIngredients
        261932,  # fridge_Cook_PieMenu_Dinner_8Servings_RequiredIngredients
        261935,  # fridge_Cook_PieMenu_Lunch_1Serving_RequiredIngredients
        261936,  # fridge_Cook_PieMenu_Lunch_8Servings_RequiredIngredients
        278191,  # fridge_CookGourmet_WeddingCake
        10163,  # stove_CookGourmet
        14344,  # stove_StartCrafting
        74310,  # stove_Cook_PieMenu_Breakfast_1Serving
        74311,  # stove_Cook_PieMenu_Breakfast_4Servings
        74312,  # stove_Cook_PieMenu_Breakfast_8Servings
        74314,  # stove_Cook_PieMenu_Brunch_1Serving
        74315,  # stove_Cook_PieMenu_Brunch_4Servings
        74316,  # stove_Cook_PieMenu_Brunch_8Servings
        74318,  # stove_Cook_PieMenu_Dinner_1Serving
        74319,  # stove_Cook_PieMenu_Dinner_4Servings
        74320,  # stove_Cook_PieMenu_Dinner_8Servings
        74322,  # stove_Cook_PieMenu_Lunch_1Serving
        74323,  # stove_Cook_PieMenu_Lunch_4Servings
        74324,  # stove_Cook_PieMenu_Lunch_8Servings
        76907,  # stove_Cook_PieMenu_Breakfast_1Serving_Ingredients
        76909,  # stove_Cook_PieMenu_Breakfast_8Servings_Ingredients
        76911,  # stove_Cook_PieMenu_Brunch_1Serving_Ingredients
        76913,  # stove_Cook_PieMenu_Brunch_8Servings_Ingredients
        76915,  # stove_Cook_PieMenu_Dinner_1Serving_Ingredients
        76917,  # stove_Cook_PieMenu_Dinner_8Servings_Ingredients
        76919,  # stove_Cook_PieMenu_Lunch_1Serving_Ingredients
        76921,  # stove_Cook_PieMenu_Lunch_8Servings_Ingredients
        75766,  # stove_Craft_Emotional
        108243,  # stove_Bake_StartCrafting
        261956,  # stove_Bake_StartCrafting_RequiredIngredients
        135398,  # stove_CookExperimental
        261880,  # stove_CookExperimental_RequiredIngredients
        185049,  # stove_Cook_GrandMeal_startCrafting
        261870,  # stove_Cook_GrandMeal_startCrafting_RequiredIngredients
        261408,  # stove_Canning
        212301,  # stove_StartCrafting_OffTheGrid
        261850,  # stove_StartCrafting_RequiredIngredients
        261868,  # stove_Craft_Emotional_RequiredIngredients
        261881,  # stove_CookGourmet_RequiredIngredients
        261888,  # stove_StartCrafting_OffTheGrid_RequiredIngredients
        267673,  # stove_Canning_OffTheGrid
        280422,  # stove_CookGourmet_WeddingCake
        261938,  # stove_Cook_PieMenu_Breakfast_1Serving_RequiredIngredients
        261940,  # stove_Cook_PieMenu_Breakfast_8Servings_RequiredIngredients
        261941,  # stove_Cook_PieMenu_Brunch_1Serving_RequiredIngredients
        261942,  # stove_Cook_PieMenu_Brunch_8Servings_RequiredIngredients
        261945,  # stove_Cook_PieMenu_Dinner_1Serving_RequiredIngredients
        261946,  # stove_Cook_PieMenu_Dinner_8Servings_RequiredIngredients
        261948,  # stove_Cook_PieMenu_Lunch_1Serving_RequiredIngredients
        261949,  # stove_Cook_PieMenu_Lunch_8Servings_RequiredIngredients
        13293,  # cupcakemaker_StartCrafting
        261960,  # cupcakemaker_StartCrafting_RequiredIngredients
        112202,  # cupcakemaker_StartBaking
        261964,  # cupcakemaker_StartBaking_RequiredIngredients
        35026,  # grill_StartCrafting
        261962,  # grill_StartCrafting_RequiredIngredients
        105165,  # campfire_startCrafting
        262116,  # campfire_startCrafting_RequiredIngredients
        120921,  # iceCream_StartCrafting_Carton
        215889,  # cauldron_Food_StartCrafting
        261958,  # cauldron_Food_StartCrafting_RequiredIngredients
        170438,  # petRecipes_StartCrafting_ForPickedPet_HomeStyle
        170439,  # petRecipes_StartCrafting_ForPickedPet_Gourmet
        210815,  # pitBBQ_StartCrafting_Grand
        261968,  # pitBBQ_StartCrafting_Grand_RequiredIngredients
        204971,  # pitBBQ_StartCrafting
        261966,  # pitBBQ_StartCrafting_RequiredIngredients
        # 213438,  # cauldron_Potion_StartCrafting
        # 103875,  # herbalism_BrewPotion_Grill
        # 103876,  # herbalism_BrewPotion_Stove
        # 241823,  # herbalism_BrewPotion_Stove_Offthegrid
        # 104954,  # scsi_ChemistryTable_Serum_Standard
        # 104955,  # scsi_ChemistryTable_Serum_Tainted
        # 109143,  # scsi_InventionConstructor_Device
        # 225825,  # Fabricator_StartCrafting
        # 315774,  # ranchNectarMaker_StartCrafting
        # 188410,  # flowerArrangement_StartCrafting_All
        # 190101,  # flowerArrangement_StartCrafting_Daisy
        # 190102,  # flowerArrangement_StartCrafting_Chrysanthemum
        # 190103,  # flowerArrangement_StartCrafting_Rose
        # 190104,  # flowerArrangement_StartCrafting_Lily
        # 190105,  # flowerArrangement_StartCrafting_ChristmasRose
        # 190106,  # flowerArrangement_StartCrafting_Crocus
        # 190107,  # flowerArrangement_StartCrafting_Holly
        # 190108,  # flowerArrangement_StartCrafting_Snowdrop
        # 190109,  # flowerArrangement_StartCrafting_Dahlia
        # 190110,  # flowerArrangement_StartCrafting_Begonia
        # 190111,  # flowerArrangement_StartCrafting_Bluebell
        # 190112,  # flowerArrangement_StartCrafting_Snapdragon
        # 190113,  # flowerArrangement_StartCrafting_Orchid
        # 190114,  # flowerArrangement_StartCrafting_BirdOfParadise
        # 190115,  # flowerArrangement_StartCrafting_Tulip
        # 278540,  # flowerArrangement_StartCrafting_WeddingBouquets
        # 218779,  # roboticsTable_CraftingPicker_Bots_Cleaner
        # 221264,  # roboticsTable_CraftingPicker_BehaviorBombs
        # 221265,  # roboticsTable_CraftingPicker_ToyRobot
        # 221699,  # roboticsTable_CraftingPicker_HumanoidRobot
        # 222709,  # roboticsTable_CraftingPicker_QuadCopter
        # 223404,  # roboticsTable_CraftingPicker_Bots_Party
        # 223405,  # roboticsTable_CraftingPicker_Bots_Gardening
        # 223406,  # roboticsTable_CraftingPicker_Bots_Repair
        # 223462,  # roboticsTable_CraftingPicker_RoboticArm
        # 223573,  # roboticsTable_CraftingPicker_Materials
        # 223584,  # roboticsTable_CraftingPicker_MechanicalSuit
        # 223586,  # roboticsTable_CraftingPicker_ComputerGlasses
        # 223599,  # roboticsTable_CraftingPicker_MechanicalHelmet
        # 233168,  # candleMakingStation_StartCrafting_Candle
        # 239529,  # Knitting_StartCrafting_Beanies
        # 239797,  # knitting_StartCrafting_Socks
        # 240538,  # knitting_StartCrafting_Furnishings
        # 240539,  # knitting_StartCrafting_Rugs
        # 240540,  # knitting_StartCrafting_Sweaters
        # 240541,  # knitting_StartCrafting_Pouffes
        # 240542,  # knitting_StartCrafting_Decorations
        # 240543,  # knitting_StartCrafting_Onesies
        # 240544,  # knitting_StartCrafting_SweaterScarfs
        # 240545,  # knitting_StartCrafting_ChildToys
        # 243582,  # knitting_StartCrafting_Beanies_Inventory
        # 243584,  # knitting_StartCrafting_ChildToys_Inventory
        # 243586,  # knitting_StartCrafting_Decorations_Inventory
        # 243588,  # knitting_StartCrafting_Furnishings_Inventory
        # 243590,  # knitting_StartCrafting_Onesies_Inventory
        # 243592,  # knitting_StartCrafting_Pouffes_Inventory
        # 243594,  # knitting_StartCrafting_Rugs_Inventory
        # 243596,  # knitting_StartCrafting_Socks_Inventory
        # 243598,  # knitting_StartCrafting_Sweaters_Inventory
        # 243600,  # knitting_StartCrafting_SweaterScarfs_Inventory
        # 243771,  # knitting_StartCrafting_SuperFail
        # 243773,  # knitting_StartCrafting_SuperFail_Inventory
        # 244901,  # knitting_StartCrafting_Mailboxes
        # 244902,  # knitting_StartCrafting_Mailboxes_Inventory
        # 245830,  # knitting_StartCrafting_BabyOnesies
        # 245831,  # knitting_StartCrafting_BabyOnesies_Inventory
        # 266571,  # knitting_StartCrafting_AnimalClothing
        # 266572,  # knitting_StartCrafting_AnimalClothing_Inventory
        # 260218,  # crossStitch_StartCrafting_Kit_SmallHoop_Simple
        # 260415,  # crossStitch_StartCrafting_Kit_SmallHoop_Animals
        # 260416,  # crossStitch_StartCrafting_Kit_SmallHoop_Foods
        # 260417,  # crossStitch_StartCrafting_Kit_SmallHoop_Nature
        # 260418,  # crossStitch_StartCrafting_Kit_SmallHoop_Words
        # 260422,  # crossStitch_StartCrafting_Kit_MediumHoop_Animals
        # 260423,  # crossStitch_StartCrafting_Kit_MediumHoop_Foods
        # 260424,  # crossStitch_StartCrafting_Kit_MediumHoop_Nature
        # 260425,  # crossStitch_StartCrafting_Kit_MediumHoop_Simple
        # 260426,  # crossStitch_StartCrafting_Kit_MediumHoop_Words
        # 260427,  # crossStitch_StartCrafting_Kit_LargeHoop_Animals
        # 260428,  # crossStitch_StartCrafting_Kit_LargeHoop_Foods
        # 260429,  # crossStitch_StartCrafting_Kit_LargeHoop_Nature
        # 260430,  # crossStitch_StartCrafting_Kit_LargeHoop_Simple
        # 260431,  # crossStitch_StartCrafting_Kit_LargeHoop_Words
        # 260441,  # crossStitch_StartCrafting_Hoop_Small_Animals
        # 260442,  # crossStitch_StartCrafting_Hoop_Small_Foods
        # 260443,  # crossStitch_StartCrafting_Hoop_Small_Nature
        # 260444,  # crossStitch_StartCrafting_Hoop_Small_Simple
        # 260445,  # crossStitch_StartCrafting_Hoop_Small_Words
        # 260446,  # crossStitch_StartCrafting_Hoop_Medium_Animals
        # 260447,  # crossStitch_StartCrafting_Hoop_Medium_Foods
        # 260448,  # crossStitch_StartCrafting_Hoop_Medium_Nature
        # 260449,  # crossStitch_StartCrafting_Hoop_Medium_Simple
        # 260450,  # crossStitch_StartCrafting_Hoop_Medium_Words
        # 260451,  # crossStitch_StartCrafting_Hoop_Large_Animals
        # 260452,  # crossStitch_StartCrafting_Hoop_Large_Foods
        # 260453,  # crossStitch_StartCrafting_Hoop_Large_Nature
        # 260454,  # crossStitch_StartCrafting_Hoop_Large_Simple
        # 260455,  # crossStitch_StartCrafting_Hoop_Large_Words
        # 263068,  # crossStitch_StartCrafting_HoopLarge_FromReference
        # 263069,  # crossStitch_StartCrafting_HoopMedium_FromReference
        # 263070,  # crossStitch_StartCrafting_HoopSmall_FromReference
        # 263071,  # crossStitch_StartCrafting_KitLarge_FromReference
        # 263072,  # crossStitch_StartCrafting_KitMedium_FromReference
        # 263073,  # crossStitch_StartCrafting_KitSmall_FromReference
        # Autonomous
        13388,  # fridge_CookAutonomously
        13390,  # fridge_CookGourmetAutonomously
        26331,  # fridge_CookGroupDessert_Autonomously
        26361,  # fridge_CookGroupMeal_Autonomously
        31030,  # fridge_BakeCake_Autonomously
        37404,  # fridge_Cook_CostumePartyFood_Autonomously
        37405,  # fridge_Cook_BlackAndWhitePartyFood_Autonomously
        152488,  # fridge_CookAutonomously_Vegetarian
        152489,  # fridge_CookGourmetAutonomously_Vegetarian
        152490,  # fridge_CookGroupMeal_Autonomously_Vegetarian
        106195,  # fridge_CookGroupMeal_MindControlled
        112476,  # fridge_StartBakingAutonomously
        126096,  # fridge_Cook_SpookyPartyFood_Autonomously
        140852,  # fridge_CookExperimentalFoodAutonomously
        145871,  # fridge_Butler_CookGourmetFamilyMeal
        145872,  # fridge_Butler_CookPartyMeal
        145873,  # fridge_Butler_CookGourmetPartyMeal
        217536,  # fridge_Cook_MindControl_Autonomously
        248563,  # fridge_CookAutonomously_JunkFood
        248564,  # fridge_CookAutonomously_HealthNut
        248570,  # fridge_CookGroupMeal_Autonomously_JunkFood
        248571,  # fridge_CookGroupMeal_Autonomously_HealthNut
        269881,  # fridge_CookAutonomously_JunkFood_RequiredIngredients
        269882,  # fridge_CookAutonomously_HealthNut_RequiredIngredients
        266482,  # fridge_CookAutonomously_LactoseIntolerant
        269874,  # fridge_CookAutonomously_RequiredIngredients
        269879,  # fridge_CookAutonomously_Vegetarian_RequiredIngredients
        269880,  # fridge_CookAutonomously_LactoseIntolerant_RequiredIngredients
        38875,  # grill_StartCraftingAutonomously
        152492,  # grill_StartCraftingAutonomously_Vegetarian
        97627,  # cupcakeMachine_CookCupcake_Autonomously
        112479,  # cupcakeMachine_StartBakingAutonomously
        126020,  # iceCreamMachine_CookIceCream_Autonomously
        105902,  # campfire_StartCraftingAutonomously
        219898,  # cauldron_CookAutonomously
        212046,  # pitBBQ_StartCrafting_Autonomously
        # 245590,  # Knitting_CraftingAutonomously
        # 348378,  # crossStitch_StartCrafting_Autonomously
        # 348579,  # crossStitch_NPCStartCrafting_Autonomously_ClubFromHoop
    )

    def all_ingredients_required(cls):  # cls here is actually "Recipe" and not "_NewRecipeClass
        recipe_id = getattr(cls, 'guid64', None)
        if recipe_id in _NewRecipeClass.excluded_recipes:
            if cls.use_ingredients is None:
                return False
            from crafting.recipe import debug_ingredient_requirements
            return cls.use_ingredients.all_ingredients_required and debug_ingredient_requirements
        return True

    def rci_picker_rows_gen(cls: StartCraftingSuperInteraction, inst, target, context, crafter=DEFAULT, order_count=1, recipe_ingredients_map=None, funds_source=None, **kwargs):
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
            if interaction_id not in _NewRecipeClass.INCLUDED_INTERACTION_IDS:
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
                (recipe_to_requirements_map, requirements_to_candidates_map) = _NewRecipeClass._prebuild_recipe_requirement_candidate_maps(cls, hashable_recipe_list, hashable_candidate_ingredients, is_ingredients_only)
                recipe_ingredients_map_other = {}
                for recipe_picker_row in original_result:
                    recipe = recipe_picker_row.tag
                    log.debug('Original val', original_result_val=recipe_picker_row, recipe=recipe, recipe_to_requirements_map=recipe_to_requirements_map.get(recipe, tuple()))
                    has_required_ingredients = True
                    requirements_for_recipe = cls._try_build_ingredient_requirements_for_recipe(recipe, recipe_to_requirements_map, requirements_to_candidates_map)
                    recipe_ingredients_map_other[recipe] = requirements_for_recipe
                    if recipe.use_ingredients is not None or recipe.ingredient_cost_only_ingredients is not None or is_ingredients_only:
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
                            if recipe.ingredient_cost_only_ingredients is not None:
                                tooltip_style = recipe.ingredient_cost_only_ingredients.missing_ingredient_tooltip_style
                            elif recipe.use_ingredients is not None:
                                tooltip_style = recipe.use_ingredients.missing_ingredient_tooltip_style
                            log.debug('Got tooltip style', tooltip_style=tooltip_style)
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

    @staticmethod
    def _prebuild_recipe_requirement_candidate_maps(interaction_class, recipe_list, candidate_ingredients, is_ingredients_only):
        recipe_to_requirements = {}
        requirement_to_ingredients = {}
        for recipe in recipe_list:
            ingredients_requirements_to_use = _NewRecipeClass._get_requirement_factories_for_recipe(recipe, is_ingredients_only)
            if ingredients_requirements_to_use is None:
                pass
            else:
                recipe_to_requirements[recipe] = ingredients_requirements_to_use
                for requirement in ingredients_requirements_to_use:
                    if requirement not in requirement_to_ingredients:
                        requirement_to_ingredients[requirement] = []
        for (requirement, ingredients) in requirement_to_ingredients.items():
            ingredients.extend(interaction_class.get_valid_ingredients_from_list_for_requirement_factory(requirement, candidate_ingredients))
        return (recipe_to_requirements, requirement_to_ingredients)

    @staticmethod
    def _get_requirement_factories_for_recipe(recipe, is_ingredients_only):
        if recipe.ingredient_cost_only_ingredients is not None:
            ingredients_requirements_to_use = recipe.sorted_ingredients_only_requirements
        elif recipe.use_ingredients is not None:
            ingredients_requirements_to_use = recipe.sorted_ingredient_requirements
        else:
            return

        if ingredients_requirements_to_use is None or len(ingredients_requirements_to_use) <= 0:
            return
        return ingredients_requirements_to_use


StartCraftingSuperInteraction.picker_rows_gen = flexmethod(_NewRecipeClass.rci_picker_rows_gen)


# Recipe.all_ingredients_required = classproperty(_NewRecipeClass.all_ingredients_required)

original_start_crafting_function = StartCraftingMixin.get_default_candidate_ingredients


def _start_crafting_override(crafter, check_sim_inventory=True, check_fridge_shared_inventory=True):
    original_result = list(original_start_crafting_function(crafter, check_sim_inventory=check_sim_inventory, check_fridge_shared_inventory=check_fridge_shared_inventory))
    # log.debug('Got things', crafter=crafter, check_sim_inventory=check_sim_inventory, check_fridge_shared_inventory=check_fridge_shared_inventory, original_ingredients=original_result)
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
    # autonomous_log.debug('Got it', clas=cls, interaction_id=interaction_id)
    if interaction_id not in _NewRecipeClass.INCLUDED_INTERACTION_IDS:
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
