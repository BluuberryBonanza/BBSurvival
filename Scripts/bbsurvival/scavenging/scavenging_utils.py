"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from random import Random
from typing import List

from bbsurvival.bb_lib.utils.bb_sim_currency_utils import BBSimCurrencyUtils
from bbsurvival.bb_lib.utils.bb_sim_inventory_utils import BBSimInventoryUtils
from bbsurvival.enums.string_ids import BBSStringId
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.scavenging.bbs_scavenging_run_length import BBSScavengingRunLength
from bluuberrylibrary.dialogs.notifications.bb_notification import BBNotification
from bluuberrylibrary.enums.string_ids import BBStringId
from bluuberrylibrary.logs.bb_log_mixin import BBLogMixin
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.utils.bb_localization_utils import BBLocalizationUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from distributor.shared_messages import IconInfoData
from objects.game_object import GameObject
from sims.sim_info import SimInfo
from sims4.common import Pack


class BBSScavengingUtils(BBLogMixin):
    """Utilities for scavenging."""

    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'bbs_scavenging_utils'

    @classmethod
    def give_scavenge_rewards(cls, sim_info: SimInfo, run_length: BBSScavengingRunLength) -> None:
        """give_scavenge_rewards(sim_info, run_length)

        Give scavenging Rewards to a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param run_length: The length of the scavenging run.
        :type run_length: BBSScavengingRunLength
        """
        log = cls.get_log()
        log.debug('Giving scavenge rewards', sim=sim_info)
        scavenge_random = Random()
        simoleons_found = scavenge_random.randint(0, 200)
        log.debug('Simoleons found', simoleons_found=simoleons_found)
        BBSimCurrencyUtils.add_simoleons(sim_info, simoleons_found)

        received_items: List[GameObject] = list()

        def _add_received_item(_game_object: GameObject):
            received_items.append(_game_object)

        # Chance of getting an item.
        common_chance = 0.75
        uncommon_chance = 0.50
        rare_chance = 0.10
        exotic_chance = 0.03

        # Chance of getting any type
        seed_chance = 0.5
        fruit_chance = 0.5
        animal_chance = 0.1
        ingredient_chance = 0.5
        mineral_chance = 0.3

        # Amount of items given for the run
        run_length_value = int(run_length)
        seed_count = 5 * run_length_value
        fruit_count = 5 * run_length_value
        animal_count = 5 * run_length_value
        ingredient_count = 5 * run_length_value
        mineral_count = 5 * run_length_value

        from sims4.common import get_available_packs
        available_packs = get_available_packs()

        # Spawn Seeds
        seed_definition_ids = {
            59678: common_chance,  # seedPacket_Garden_Starter_Fruits
            59676: uncommon_chance,  # seedPacket_Garden_Starter_Flowers
            59679: uncommon_chance,  # seedPacket_Garden_Starter_Herbs
            59680: common_chance,  # seedPacket_Garden_Starter_Vegetables
            62723: rare_chance,  # seedPacket_Garden_Starter_Deluxe_FlowersFruit
            62724: rare_chance,  # seedPacket_Garden_Starter_Deluxe_VegetablesHerbs
            124934: exotic_chance,  # seedPacket_Garden_Start_GrowFruit
            176694: rare_chance,  # seedPacket_Garden_Starter_Catnip
            228500: exotic_chance,  # seedPacket_Garden_Starter_Magic
            193547: rare_chance,  # seedPacket_Garden_rare
            193549: uncommon_chance,  # seedPacket_Garden_uncommon
        }

        if Pack.EP05 in available_packs:
            ep5_seed_definition_ids = {
                188697: common_chance,  # seedPacket_Garden_EP05_summer
                188699: common_chance,  # seedPacket_Garden_EP05_fall
                188700: common_chance,  # seedPacket_Garden_EP05_winter
                188702: common_chance,  # seedPacket_Garden_EP05_spring
            }
            seed_definition_ids.update(ep5_seed_definition_ids)

        if Pack.EP09 in available_packs:
            ep9_seed_definition_ids = {
                244457: common_chance,  # seedPacket_Garden_EP09_grubMeal
                244874: uncommon_chance,  # seedPacket_Garden_EP09_CricketFlour
                244875: rare_chance,  # seedPacket_Garden_EP09_BeetleNugget
                244876: exotic_chance,  # seedPacket_Garden_EP09_BombardierBeetleNugget
                249967: uncommon_chance,  # seedPacket_Garden_EP09_VerticalGarden_Fruit
                249968: uncommon_chance,  # seedPacket_Garden_EP09_VerticalGarden_Herbs
                249972: uncommon_chance,  # seedPacket_Garden_EP09_VerticalGarden_Flowers
            }
            seed_definition_ids.update(ep9_seed_definition_ids)

        if Pack.EP11 in available_packs:
            ep11_seed_definition_ids = {
                272268: common_chance,  # gardenSeedPacket_EP11GENcrop_set1_aubergine
                272269: common_chance,  # gardenSeedPacket_EP11GENcrop_set2_lettuce
                272270: uncommon_chance,  # gardenSeedPacket_EP11GENcrop_set3_pumpkin
                272271: rare_chance,  # gardenSeedPacket_EP11GENcrop_set4_watermelon
                284142: exotic_chance,  # gardenSeedPacket_EP11GENcrop_set5_mushroom
            }
            seed_definition_ids.update(ep11_seed_definition_ids)

        if Pack.GP04 in available_packs:
            gp4_seed_definition_ids = {
                147519: uncommon_chance,  # gardenSeedPacket_GP04GEN_garlic
                147520: uncommon_chance,  # gardenSeedPacket_GP04GEN_wolfsbane
                147521: rare_chance,  # gardenSeedPacket_GP04GEN_plasma
                147522: uncommon_chance,  # gardenSeedPacket_GP04GEN_mosquito
            }
            seed_definition_ids.update(gp4_seed_definition_ids)

        seed_dice_roll = scavenge_random.random()
        if seed_dice_roll < seed_chance:
            log.debug('Giving random seeds.', seed_chance=seed_chance, seed_dice_roll=seed_dice_roll)
            chosen_seeds = scavenge_random.sample(tuple(seed_definition_ids.keys()), seed_count)
            to_add_seeds = list()
            for chosen_seed in chosen_seeds:
                chosen_seed_chance = seed_definition_ids[chosen_seed]
                if scavenge_random.random() < chosen_seed_chance:
                    to_add_seeds.append(chosen_seed)
            log.debug('Chose Seeds', chosen_seeds=chosen_seeds, to_add_seeds=to_add_seeds)
            for to_add_seed in to_add_seeds:
                BBSimInventoryUtils.create_in_inventory(sim_info, to_add_seed, on_added=_add_received_item)
        else:
            log.debug('Not giving Seeds', seed_chance=seed_chance, seed_dice_roll=seed_dice_roll)

        fruit_definition_ids = {
            29009: exotic_chance,  # gardenFruitGENAlien_01
            21939: common_chance,  # gardenFruitGENApple_01
            23438: common_chance,  # gardenFruitGENBlackberry_01
            45767: uncommon_chance,  # gardenFruitGENBonsai
            45299: common_chance,  # gardenFruitGENCarrot_01
            22467: common_chance,  # gardenFruitGENCherry_01
            37858: exotic_chance,  # gardenFruitGENCowplant_01
            23440: rare_chance,  # gardenFruitGENDragon_01
            23442: common_chance,  # gardenFruitGENGrapes_01
            22466: common_chance,  # gardenFruitGENLemon_01
            45311: uncommon_chance,  # gardenFruitGENMushroom_01
            23445: common_chance,  # gardenFruitGENPear_01
            22468: common_chance,  # gardenFruitGENPlantain_01
            23439: common_chance,  # gardenFruitGENPomegranate_01
            23437: common_chance,  # gardenFruitGENStrawberry_01
            46336: common_chance,  # gardenFruitGENTomato_01
            125468: common_chance,  # gardenFruit_GENGrowfruit_01
        }

        if Pack.EP05 in available_packs:
            ep5_fruit_definition_ids = {
                165689: exotic_chance,  # gardenFruitEF05GENforbiddenFruit
                188687: common_chance,  # gardenFruit_EP05GENgreenBeans
                188689: common_chance,  # gardenFruit_EP05GENgreenPeppers
                188693: exotic_chance,  # gardenFruit_EP05GENmoney
                188691: common_chance,  # gardenFruit_EP05GENpeas
            }
            fruit_definition_ids.update(ep5_fruit_definition_ids)

        if Pack.EP07 in available_packs:
            ep7_fruit_definition_ids = {
                215737: rare_chance,  # gardenFruit_EP07GENcoconut
                213665: common_chance,  # gardenFruit_EP07GENkava
                215738: rare_chance,  # gardenFruit_EP07GENpineapple
            }
            fruit_definition_ids.update(ep7_fruit_definition_ids)

        if Pack.EP09 in available_packs:
            ep7_fruit_definition_ids = {
                242040: common_chance,  # gardenFruit_EP09GENsoybean
            }
            fruit_definition_ids.update(ep7_fruit_definition_ids)

        if Pack.EP11 in available_packs:
            ep11_fruit_definition_ids = {
                270185: rare_chance,  # gardenFruitCropLarge_EP11GENAubergine_set1
                270186: rare_chance,  # gardenFruitCropLarge_EP11GENLettuce_set1
                270187: exotic_chance,  # gardenFruitCropLarge_EP11GENPumpkin_set1
                286426: exotic_chance,  # gardenFruitCropLarge_EP11GENPumpkin_set2
                286427: exotic_chance,  # gardenFruitCropLarge_EP11GENPumpkin_set3
                271873: exotic_chance,  # gardenFruitCropLarge_EP11GENWatermelon_set1
                283842: exotic_chance,  # gardenFruitCropLarge_EP11GENmushroom_set1
                270295: uncommon_chance,  # gardenFruitCropMedium_EP11GENAubergine_set1
                270297: uncommon_chance,  # gardenFruitCropMedium_EP11GENLettuce_set1
                270299: rare_chance,  # gardenFruitCropMedium_EP11GENPumpkin_set1
                286424: rare_chance,  # gardenFruitCropMedium_EP11GENPumpkin_set2
                286425: rare_chance,  # gardenFruitCropMedium_EP11GENPumpkin_set3
                271875: rare_chance,  # gardenFruitCropMedium_EP11GENWatermelon_set1
                283840: rare_chance,  # gardenFruitCropMedium_EP11GENmushroom_set1
                270289: common_chance,  # gardenFruitCropSmall_EP11GENAubergine_set1
                270291: common_chance,  # gardenFruitCropSmall_EP11GENLettuce_set1
                270293: uncommon_chance,  # gardenFruitCropSmall_EP11GENPumpkin_set1
                286422: uncommon_chance,  # gardenFruitCropSmall_EP11GENPumpkin_set2
                286423: uncommon_chance,  # gardenFruitCropSmall_EP11GENPumpkin_set3
                271877: uncommon_chance,  # gardenFruitCropSmall_EP11GENWatermelon_set1
                283838: uncommon_chance,  # gardenFruitCropSmall_EP11GENmushroom_set1
                270257: common_chance,  # gardenFruit_EP11GENBlueberry_set1
                286364: common_chance,  # gardenFruit_EP11GENMushroomWildBasic
                272255: common_chance,  # gardenFruit_EP11GENMushroomWildSpicy
                272253: common_chance,  # gardenFruit_EP11GENMushroomWildVerdant
                270259: common_chance,  # gardenFruit_EP11GENRaspberry_set1
                272254: common_chance,  # gardenFruit_EP11GENmushroomWildCharming
                272256: common_chance,  # gardenFruit_EP11GENmushroomWildLovely
                271725: common_chance,  # gardenFruit_EP11GENmushroomWildMysterious
                270260: common_chance,  # gardenFruit_EP11GENmushroomWildNightly
            }
            fruit_definition_ids.update(ep11_fruit_definition_ids)

        if Pack.GP01 in available_packs:
            gp1_fruit_definition_ids = {
                66140: exotic_chance,  # gardenFruit_GP01GENelderberry
                67556: rare_chance,  # gardenFruit_GP01GENhuckleberry
                66145: uncommon_chance,  # gardenFruit_GP01GENmushroomMorel
            }
            fruit_definition_ids.update(gp1_fruit_definition_ids)

        if Pack.GP04 in available_packs:
            gp4_fruit_definition_ids = {
                147404: common_chance,  # gardenFruit_GP04GENmosquito
                144964: exotic_chance,  # gardenFruit_GP04GENplasma
            }
            fruit_definition_ids.update(gp4_fruit_definition_ids)

        if Pack.GP06 in available_packs:
            gp6_fruit_definition_ids = {
                178855: common_chance,  # gardenFruit_GP06GENBlackBean
                187285: common_chance,  # gardenFruit_GP06GENBlackBean_01
                178801: exotic_chance,  # gardenFruit_GP06GENEmotionalBerry_confident
                178802: exotic_chance,  # gardenFruit_GP06GENEmotionalBerry_energized
                178803: exotic_chance,  # gardenFruit_GP06GENEmotionalBerry_flirty
                178804: exotic_chance,  # gardenFruit_GP06GENEmotionalBerry_focused
                178800: exotic_chance,  # gardenFruit_GP06GENEmotionalBerry_happy
                178805: exotic_chance,  # gardenFruit_GP06GENEmotionalBerry_inspired
                178806: exotic_chance,  # gardenFruit_GP06GENEmotionalBerry_playful
                178808: common_chance,  # gardenFruit_GP06GENavocado
                187283: common_chance,  # gardenFruit_GP06GENavocado_01
            }
            fruit_definition_ids.update(gp6_fruit_definition_ids)

        if Pack.GP08 in available_packs:
            gp6_fruit_definition_ids = {
                227207: common_chance,  # gardenFruit_GP08GENmandrake
                227209: common_chance,  # gardenFruit_GP08GENvalerian
            }
            fruit_definition_ids.update(gp6_fruit_definition_ids)

        fruit_dice_roll = scavenge_random.random()
        if fruit_dice_roll < fruit_chance:
            log.debug('Giving random Fruits.', fruit_chance=fruit_chance, fruit_dice_roll=fruit_dice_roll)
            chosen_fruits = scavenge_random.sample(tuple(fruit_definition_ids.keys()), fruit_count)
            to_add_fruits = list()
            for chosen_fruit in chosen_fruits:
                chosen_fruit_chance = fruit_definition_ids[chosen_fruit]
                if scavenge_random.random() < chosen_fruit_chance:
                    to_add_fruits.append(chosen_fruit)
            log.debug('Chose fruits', chosen_fruits=chosen_fruits, to_add_fruits=to_add_fruits)
            for to_add_fruit in to_add_fruits:
                BBSimInventoryUtils.create_in_inventory(sim_info, to_add_fruit, on_added=_add_received_item)
        else:
            log.debug('Not giving Fruits', fruit_chance=fruit_chance, fruit_dice_roll=fruit_dice_roll)

        animal_definition_ids = dict()

        if Pack.EP11 in available_packs:
            ep11_animal_definition_ids = {
                # Chickens
                266636: common_chance,  # animalAvianChicken_EP11GEN_set1 (White Hen)
                263031: common_chance,  # animalAvianRooster_EP11GEN_set1 (White Rooster)
                281877: uncommon_chance,  # animalAvianChicken_EP11GEN_set2 (Brown Hen)
                281880: uncommon_chance,  # animalAvianRooster_EP11GEN_set2 (Brown Rooster)
                281878: rare_chance,  # animalAvianChicken_EP11GEN_set3 (Black Hen)
                281881: rare_chance,  # animalAvianRooster_EP11GEN_set3 (Black Rooster)
                268719: common_chance,  # animalAvianChick_EP11GEN (Chick Hen)
                283181: common_chance,  # animalAvianChickRooster_EP11GEN (Chick Rooster)
                277970: exotic_chance,  # animalAvianChicken_EP11GEN_golden (Golden Hen)
                277973: exotic_chance,  # animalAvianRooster_EP11GEN_golden (Golden Rooster)
                277971: exotic_chance,  # animalAvianChicken_EP11GEN_evil (Evil Hen)
                277972: exotic_chance,  # animalAvianRooster_EP11GEN_evil (Evil Rooster)
                # Cow
                264866: uncommon_chance,  # animalCow_EP11GEN_set1 (Spotted Cow)
                279057: uncommon_chance,  # animalCow_EP11GEN_set3 (Cow)
                276585: rare_chance,  # animalCow_EP11GEN_set2 (Brown Cow)
                # Llama
                269148: common_chance,  # animalLlama_EP11GEN_set1 (White Llama)
                272077: common_chance,  # animalLlama_EP11GEN_set2 (Beige Llama)
                272078: uncommon_chance,  # animalLlama_EP11GEN_set3 (Pink Llama)
                278859: uncommon_chance,  # animalLlama_EP11GEN_set4 (Brown Llama)
                278860: rare_chance,  # animalLlama_EP11GEN_set5 (Red Llama)
                278861: rare_chance,  # animalLlama_EP11GEN_set6 (Orange Llama)
                278862: rare_chance,  # animalLlama_EP11GEN_set7 (Blue Llama)
                278863: rare_chance,  # animalLlama_EP11GEN_set8 (Green Llama)
                278864: exotic_chance,  # animalLlama_EP11GEN_set9 (Rainbow Llama)
                278865: rare_chance,  # animalLlama_EP11GEN_set10 (Orange Llama)
                278866: uncommon_chance,  # animalLlama_EP11GEN_set11 (Black Llama)
            }
            animal_definition_ids.update(ep11_animal_definition_ids)

        if Pack.EP14 in available_packs:
            ep14_animal_definition_ids = {
                # Sheep
                338596: uncommon_chance,  # animalSheepMini_EP14GEN_set1 (White Sheep)
                351751: uncommon_chance,  # animalSheepMini_EP14GEN_set2 (Cream Sheep)
                351752: rare_chance,  # animalSheepMini_EP14GEN_set3 (Pink Sheep)
                351753: uncommon_chance,  # animalSheepMini_EP14GEN_set4 (Brown Sheep)
                351754: exotic_chance,  # animalSheepMini_EP14GEN_set5 (Red Sheep)
                351755: exotic_chance,  # animalSheepMini_EP14GEN_set6 (Orange Sheep)
                351756: rare_chance,  # animalSheepMini_EP14GEN_set7 (Blue Sheep)
                351757: exotic_chance,  # animalSheepMini_EP14GEN_set8 (Green Sheep)
                351758: uncommon_chance,  # animalSheepMini_EP14GEN_set9 (Black Sheep)
                351812: exotic_chance,  # animalSheepMini_EP14GEN_set10 (Dalmatian Sheep)
                351852: rare_chance,  # animalSheepMini_EP14GEN_set11 (Mocha Sheep)
                # Goat
                328494: uncommon_chance,  # animalGoatMini_EP14GEN_set1 (White Goat)
                346691: uncommon_chance,  # animalGoatMini_EP14GEN_set2 (Gray Goat)
                346692: rare_chance,  # animalGoatMini_EP14GEN_set3 (Black Goat)
                346693: exotic_chance,  # animalGoatMini_EP14GEN_set4 (Dalmatian Goat)
                346694: uncommon_chance,  # animalGoatMini_EP14GEN_set5 (Brown Goat)
                346849: uncommon_chance,  # animalGoatMini_EP14GEN_set6 (White Belt Goat)
                347200: rare_chance,  # animalGoatMini_EP14GEN_set7 (Chamoisee Goat)
                347201: uncommon_chance,  # animalGoatMini_EP14GEN_set8 (Spotted Goat)
            }
            animal_definition_ids.update(ep14_animal_definition_ids)

        if animal_definition_ids:
            animal_dice_roll = scavenge_random.random()
            if animal_dice_roll < animal_chance:
                log.debug('Giving random Animals.', animal_chance=animal_chance, animal_dice_roll=animal_dice_roll)
                chosen_animals = scavenge_random.sample(tuple(animal_definition_ids.keys()), animal_count)
                to_add_animals = list()
                for chosen_animal in chosen_animals:
                    chosen_animal_chance = animal_definition_ids[chosen_animal]
                    if scavenge_random.random() < chosen_animal_chance:
                        to_add_animals.append(chosen_animal)
                log.debug('Chose animals', chosen_animals=chosen_animals, to_add_animals=to_add_animals)
                for to_add_animal in to_add_animals:
                    BBSimInventoryUtils.create_in_inventory(sim_info, to_add_animal, on_added=_add_received_item)
            else:
                log.debug('Not giving Animals', animal_chance=animal_chance, animal_dice_roll=animal_dice_roll)

        ingredient_definition_ids = {
            # Other
            278715: common_chance,  # foodIngredient_GENsack_flour
            278719: common_chance,  # foodIngredient_GENMeat01_whiteMeat
            278923: common_chance,  # foodIngredient_GENMeat01_redMeat
            278924: common_chance,  # foodIngredient_GENsack_sugar
        }

        if Pack.EP11 in available_packs:
            ep11_ingredient_definition_ids = {
                # Milk
                271852: common_chance,  # drinkBottle_EP11GENmilk_set1_base
                277732: uncommon_chance,  # drinkBottle_EP11GENmilk_set1_blue
                277735: rare_chance,  # drinkBottle_EP11GENmilk_set1_green
                277731: rare_chance,  # drinkBottle_EP11GENmilk_set2_black
                277733: rare_chance,  # drinkBottle_EP11GENmilk_set3_brown
                277734: exotic_chance,  # drinkBottle_EP11GENmilk_set4_gold
                277736: rare_chance,  # drinkBottle_EP11GENmilk_set5_orange
                277737: rare_chance,  # drinkBottle_EP11GENmilk_set6_pink
                277794: exotic_chance,  # drinkBottle_EP11GENmilk_set7_rainbow
                277795: rare_chance,  # drinkBottle_EP11GENmilk_set8_red
                # Eggs
                266633: common_chance,  # egg_EP11GEN_set1_white
                272308: exotic_chance,  # egg_EP11GEN_set2_Gold
                272309: rare_chance,  # egg_EP11GEN_set3_Chocolate
                272310: exotic_chance,  # egg_EP11GEN_set4_obsidian
                272311: exotic_chance,  # egg_EP11GEN_set5_Blue
                272312: rare_chance,  # egg_EP11GEN_set6_Green
                272313: rare_chance,  # egg_EP11GEN_set7_Orange
                272314: exotic_chance,  # egg_EP11GEN_set8_Rainbow
                284595: uncommon_chance,  # eggHatchable_EP11GEN_set1_white
                284596: rare_chance,  # eggHatchable_EP11GEN_set4_obsidian
                284597: exotic_chance,  # eggHatchable_EP11GEN_set2_Gold
                # Other
                270258: uncommon_chance,  # gardenFruit_EP11GENChocolateBerry_set1
            }
            ingredient_definition_ids.update(ep11_ingredient_definition_ids)

        ingredient_dice_roll = scavenge_random.random()
        if ingredient_dice_roll < ingredient_chance:
            log.debug('Giving random ingredients.', ingredient_chance=ingredient_chance, ingredient_dice_roll=ingredient_dice_roll)
            chosen_ingredients = scavenge_random.sample(tuple(ingredient_definition_ids.keys()), ingredient_count)
            to_add_ingredients = list()
            for chosen_ingredient in chosen_ingredients:
                chosen_ingredient_chance = ingredient_definition_ids[chosen_ingredient]
                if scavenge_random.random() < chosen_ingredient_chance:
                    to_add_ingredients.append(chosen_ingredient)
            log.debug('Chose ingredients', chosen_ingredients=chosen_ingredients, to_add_ingredients=to_add_ingredients)
            for to_add_ingredient in to_add_ingredients:
                BBSimInventoryUtils.create_in_inventory(sim_info, to_add_ingredient, on_added=_add_received_item)
        else:
            log.debug('Not giving ingredients', ingredient_chance=ingredient_chance, ingredient_dice_roll=ingredient_dice_roll)

        mineral_definition_ids = {
            # Metals
            28759: uncommon_chance,  # collectMetalMedGEN_01_crytunium
            28760: rare_chance,  # collectMetalMedGEN_01_furium
            28761: common_chance,  # collectMetalMedGEN_01_heavyMetal
            28764: uncommon_chance,  # collectMetalMedGEN_01_ironyum
            28771: common_chance,  # collectMetalMedGEN_01_ozinold
            28772: common_chance,  # collectMetalMedGEN_01_plathinum
            28773: rare_chance,  # collectMetalMedGEN_01_romantium
            28774: rare_chance,  # collectMetalMedGEN_01_sadnum
            28775: uncommon_chance,  # collectMetalMedGEN_01_simtanium
            28776: common_chance,  # collectMetalMedGEN_01_utranium
            28777: common_chance,  # collectMetalSmGEN_01_alcron
            28778: common_chance,  # collectMetalSmGEN_01_baconite
            28779: uncommon_chance,  # collectMetalSmGEN_01_deathMetal
            28780: uncommon_chance,  # collectMetalSmGEN_01_flamingonium
            28781: rare_chance,  # collectMetalSmGEN_01_literalite
            28782: common_chance,  # collectMetalSmGEN_01_obtainium
            28783: common_chance,  # collectMetalSmGEN_01_phozonite
            28784: common_chance,  # collectMetalSmGEN_01_punium
            28785: common_chance,  # collectMetalSmGEN_01_pyrite
            28786: uncommon_chance,  # collectMetalSmGEN_01_socialite
            # Crystals
            28727: uncommon_chance,  # collectCrystalSmGEN_01_amethyst
            28728: uncommon_chance,  # collectCrystalSmGEN_01_diamond
            28729: common_chance,  # collectCrystalSmGEN_01_emerald
            28730: uncommon_chance,  # collectCrystalSmGEN_01_hematite
            28731: rare_chance,  # collectCrystalSmGEN_01_jonquilyst
            28732: common_chance,  # collectCrystalSmGEN_01_orangeTopaz
            28733: common_chance,  # collectCrystalSmGEN_01_peach
            28734: rare_chance,  # collectCrystalSmGEN_01_rainborz
            28735: common_chance,  # collectCrystalSmGEN_01_sapphire
            28736: uncommon_chance,  # collectCrystalSmGEN_01_simanite
            28738: common_chance,  # collectCrystalMedGEN_01_alabaster
            28739: common_chance,  # collectCrystalMedGEN_01_citrine
            28740: uncommon_chance,  # collectCrystalMedGEN_01_fireOpal
            28741: rare_chance,  # collectCrystalMedGEN_01_jet
            28743: rare_chance,  # collectCrystalMedGEN_01_plumbite
            28744: common_chance,  # collectCrystalMedGEN_01_quartz
            28747: common_chance,  # collectCrystalMedGEN_01_rose
            28748: common_chance,  # collectCrystalMedGEN_01_ruby
            28749: uncommon_chance,  # collectCrystalMedGEN_01_shinalite
            28750: common_chance,  # collectCrystalMedGEN_01_turquoise
        }

        if Pack.EP01 in available_packs:
            ep01_mineral_definition_ids = {
                # Metals
                72392: exotic_chance,  # collectMetalMed_EP01GENblutonium
                72394: exotic_chance,  # collectMetalMed_EP01GENsolarium
                # Crystals
                72395: exotic_chance,  # collectCrystalMed_EP01GEN_crandestine
                72396: exotic_chance,  # collectCrystalMed_EP01GEN_nitelite
            }
            mineral_definition_ids.update(ep01_mineral_definition_ids)

        if Pack.GP06 in available_packs:
            gp06_mineral_definition_ids = {
                # Crystals
                178735: rare_chance,  # collectCrystalMed_GP06GEN_alexandrite
                178736: uncommon_chance,  # collectCrystalMed_GP06GEN_amazonite
            }
            mineral_definition_ids.update(gp06_mineral_definition_ids)

        mineral_dice_roll = scavenge_random.random()
        if mineral_dice_roll < mineral_chance:
            log.debug('Giving random minerals.', mineral_chance=mineral_chance, mineral_dice_roll=mineral_dice_roll)
            chosen_minerals = scavenge_random.sample(tuple(mineral_definition_ids.keys()), mineral_count)
            to_add_minerals = list()
            for chosen_mineral in chosen_minerals:
                chosen_mineral_chance = mineral_definition_ids[chosen_mineral]
                if scavenge_random.random() < chosen_mineral_chance:
                    to_add_minerals.append(chosen_mineral)
            log.debug('Chose minerals', chosen_minerals=chosen_minerals, to_add_minerals=to_add_minerals)
            for to_add_mineral in to_add_minerals:
                BBSimInventoryUtils.create_in_inventory(sim_info, to_add_mineral, on_added=_add_received_item)
        else:
            log.debug('Not giving minerals', mineral_chance=mineral_chance, mineral_dice_roll=mineral_dice_roll)

        try:
            if received_items:
                sim = BBSimUtils.to_sim_instance(sim_info)
                received_item_strings = list()
                if simoleons_found > 0:
                    received_item_strings.append(BBLocalizationUtils.to_localized_string(BBSStringId.STRING_SIMOLEONS, tokens=(str(simoleons_found),)))
                for received_item in received_items:
                    item_count = 1
                    catalog_name = received_item.custom_name if received_item.has_custom_name() else received_item.catalog_name
                    log.debug('Got item definition', received_item=received_item, catalog_name=catalog_name, definition_id=str(received_item.definition.id))
                    if log.is_enabled():
                        received_item_strings.append(BBLocalizationUtils.to_localized_string(BBStringId.BBL_STRING_PARENTHESIS_STRING, tokens=(BBLocalizationUtils.to_localized_string(catalog_name, tokens=(item_count,), normalize_tokens=False), str(received_item.definition.id))))
                    else:
                        received_item_strings.append(BBLocalizationUtils.to_localized_string(catalog_name))

                text = BBLocalizationUtils.combine_strings(received_item_strings, separator_text=BBStringId.BBL_STRING_NEWLINE_STRING)

                BBNotification(
                    BBSStringId.FOUND_WHILE_SCAVENGING,
                    text
                ).show(icon=IconInfoData(obj_instance=sim))
        except Exception as ex:
            log.error('An error occurred displaying notification', exception=ex)
