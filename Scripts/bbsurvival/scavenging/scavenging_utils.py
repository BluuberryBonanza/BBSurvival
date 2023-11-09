"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from random import Random
from typing import List, Dict, Callable, Tuple

from bbsurvival.bb_lib.utils.bb_sim_currency_utils import BBSimCurrencyUtils
from bbsurvival.bb_lib.utils.bb_sim_inventory_utils import BBSimInventoryUtils
from bbsurvival.enums.item_rarity import BBSItemRarity
from bbsurvival.enums.scavenged_item_type import BBSScavengedItemType
from bbsurvival.enums.string_ids import BBSStringId
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.scavenging.bbs_scavenging_run_length import BBSScavengingRunLength
from bluuberrylibrary.dialogs.notifications.bb_notification import BBNotification
from bluuberrylibrary.enums.string_ids import BBStringId
from bluuberrylibrary.dialogs.icons.bb_sim_icon_info import BBSimIconInfo
from bluuberrylibrary.logs.bb_log_mixin import BBLogMixin
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.utils.text.bb_localization_utils import BBLocalizationUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from objects.game_object import GameObject
from sims.sim_info import SimInfo
from sims4.common import Pack


class BBSScavengingUtils(BBLogMixin):
    """Utilities for scavenging."""
    RARITY_CHANCES: Dict[BBSItemRarity, float] = {
        BBSItemRarity.COMMON: 0.75,
        BBSItemRarity.UNCOMMON: 0.50,
        BBSItemRarity.RARE: 0.10,
        BBSItemRarity.EXOTIC: 0.03
    }

    ITEM_CHANCE = {
        BBSScavengedItemType.SEED: 0.1,
        BBSScavengedItemType.FRUIT: 0.5,
        BBSScavengedItemType.ANIMAL: 0.1,
        BBSScavengedItemType.INGREDIENT: 0.5,
        BBSScavengedItemType.MINERAL: 0.3
    }

    ITEMS_PER_QUICK_RUN = {
        BBSScavengedItemType.SEED: 1,
        BBSScavengedItemType.FRUIT: 1,
        BBSScavengedItemType.ANIMAL: 1,
        BBSScavengedItemType.INGREDIENT: 1,
        BBSScavengedItemType.MINERAL: 1
    }

    MIN_SIMOLEONS_PER_QUICK_RUN = 0
    MAX_SIMOLEONS_PER_QUICK_RUN = 200

    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'bbs_scavenging_utils'

    @classmethod
    def get_available_seeds(cls) -> Dict[int, BBSItemRarity]:
        """get_available_seeds()

        Retrieve available seeds for scavenging.

        :return: A dictionary of object definition ids to the rarity of the item being obtained.
        :rtype: Dict[int, BBSItemRarity]
        """
        from sims4.common import get_available_packs
        available_packs = get_available_packs()

        # Spawn Seeds
        seed_definition_ids = {
            59678: BBSItemRarity.COMMON,  # seedPacket_Garden_Starter_Fruits
            59676: BBSItemRarity.UNCOMMON,  # seedPacket_Garden_Starter_Flowers
            59679: BBSItemRarity.UNCOMMON,  # seedPacket_Garden_Starter_Herbs
            59680: BBSItemRarity.COMMON,  # seedPacket_Garden_Starter_Vegetables
            62723: BBSItemRarity.RARE,  # seedPacket_Garden_Starter_Deluxe_FlowersFruit
            62724: BBSItemRarity.RARE,  # seedPacket_Garden_Starter_Deluxe_VegetablesHerbs
            124934: BBSItemRarity.EXOTIC,  # seedPacket_Garden_Start_GrowFruit
            176694: BBSItemRarity.RARE,  # seedPacket_Garden_Starter_Catnip
            228500: BBSItemRarity.EXOTIC,  # seedPacket_Garden_Starter_Magic
            193547: BBSItemRarity.RARE,  # seedPacket_Garden_rare
            193549: BBSItemRarity.UNCOMMON,  # seedPacket_Garden_uncommon
        }

        if Pack.EP05 in available_packs:
            ep5_seed_definition_ids = {
                188697: BBSItemRarity.COMMON,  # seedPacket_Garden_EP05_summer
                188699: BBSItemRarity.COMMON,  # seedPacket_Garden_EP05_fall
                188700: BBSItemRarity.COMMON,  # seedPacket_Garden_EP05_winter
                188702: BBSItemRarity.COMMON,  # seedPacket_Garden_EP05_spring
            }
            seed_definition_ids.update(ep5_seed_definition_ids)

        if Pack.EP09 in available_packs:
            ep9_seed_definition_ids = {
                244457: BBSItemRarity.COMMON,  # seedPacket_Garden_EP09_grubMeal
                244874: BBSItemRarity.UNCOMMON,  # seedPacket_Garden_EP09_CricketFlour
                244875: BBSItemRarity.RARE,  # seedPacket_Garden_EP09_BeetleNugget
                244876: BBSItemRarity.EXOTIC,  # seedPacket_Garden_EP09_BombardierBeetleNugget
                249967: BBSItemRarity.UNCOMMON,  # seedPacket_Garden_EP09_VerticalGarden_Fruit
                249968: BBSItemRarity.UNCOMMON,  # seedPacket_Garden_EP09_VerticalGarden_Herbs
                249972: BBSItemRarity.UNCOMMON,  # seedPacket_Garden_EP09_VerticalGarden_Flowers
            }
            seed_definition_ids.update(ep9_seed_definition_ids)

        if Pack.EP11 in available_packs:
            ep11_seed_definition_ids = {
                272268: BBSItemRarity.COMMON,  # gardenSeedPacket_EP11GENcrop_set1_aubergine
                272269: BBSItemRarity.COMMON,  # gardenSeedPacket_EP11GENcrop_set2_lettuce
                272270: BBSItemRarity.UNCOMMON,  # gardenSeedPacket_EP11GENcrop_set3_pumpkin
                272271: BBSItemRarity.RARE,  # gardenSeedPacket_EP11GENcrop_set4_watermelon
                284142: BBSItemRarity.EXOTIC,  # gardenSeedPacket_EP11GENcrop_set5_mushroom
            }
            seed_definition_ids.update(ep11_seed_definition_ids)

        if Pack.GP04 in available_packs:
            gp4_seed_definition_ids = {
                147519: BBSItemRarity.UNCOMMON,  # gardenSeedPacket_GP04GEN_garlic
                147520: BBSItemRarity.UNCOMMON,  # gardenSeedPacket_GP04GEN_wolfsbane
                147521: BBSItemRarity.RARE,  # gardenSeedPacket_GP04GEN_plasma
                147522: BBSItemRarity.UNCOMMON,  # gardenSeedPacket_GP04GEN_mosquito
            }
            seed_definition_ids.update(gp4_seed_definition_ids)

        return seed_definition_ids

    @classmethod
    def get_available_fruits(cls) -> Dict[int, BBSItemRarity]:
        """get_available_fruits()

        Retrieve available Fruits for scavenging.

        :return: A dictionary of object definition ids to the rarity of the item being obtained.
        :rtype: Dict[int, BBSItemRarity]
        """
        from sims4.common import get_available_packs
        available_packs = get_available_packs()

        fruit_definition_ids = {
            29009: BBSItemRarity.EXOTIC,  # gardenFruitGENAlien_01
            21939: BBSItemRarity.COMMON,  # gardenFruitGENApple_01
            23438: BBSItemRarity.COMMON,  # gardenFruitGENBlackberry_01
            45767: BBSItemRarity.UNCOMMON,  # gardenFruitGENBonsai
            45299: BBSItemRarity.COMMON,  # gardenFruitGENCarrot_01
            22467: BBSItemRarity.COMMON,  # gardenFruitGENCherry_01
            37858: BBSItemRarity.EXOTIC,  # gardenFruitGENCowplant_01
            23440: BBSItemRarity.RARE,  # gardenFruitGENDragon_01
            23442: BBSItemRarity.COMMON,  # gardenFruitGENGrapes_01
            22466: BBSItemRarity.COMMON,  # gardenFruitGENLemon_01
            45311: BBSItemRarity.UNCOMMON,  # gardenFruitGENMushroom_01
            23445: BBSItemRarity.COMMON,  # gardenFruitGENPear_01
            22468: BBSItemRarity.COMMON,  # gardenFruitGENPlantain_01
            23439: BBSItemRarity.COMMON,  # gardenFruitGENPomegranate_01
            23437: BBSItemRarity.COMMON,  # gardenFruitGENStrawberry_01
            46336: BBSItemRarity.COMMON,  # gardenFruitGENTomato_01
            125468: BBSItemRarity.COMMON,  # gardenFruit_GENGrowfruit_01
        }

        if Pack.EP05 in available_packs:
            ep5_fruit_definition_ids = {
                165689: BBSItemRarity.EXOTIC,  # gardenFruitEF05GENforbiddenFruit
                188687: BBSItemRarity.COMMON,  # gardenFruit_EP05GENgreenBeans
                188689: BBSItemRarity.COMMON,  # gardenFruit_EP05GENgreenPeppers
                188693: BBSItemRarity.EXOTIC,  # gardenFruit_EP05GENmoney
                188691: BBSItemRarity.COMMON,  # gardenFruit_EP05GENpeas
            }
            fruit_definition_ids.update(ep5_fruit_definition_ids)

        if Pack.EP07 in available_packs:
            ep7_fruit_definition_ids = {
                215737: BBSItemRarity.RARE,  # gardenFruit_EP07GENcoconut
                213665: BBSItemRarity.COMMON,  # gardenFruit_EP07GENkava
                215738: BBSItemRarity.RARE,  # gardenFruit_EP07GENpineapple
            }
            fruit_definition_ids.update(ep7_fruit_definition_ids)

        if Pack.EP09 in available_packs:
            ep7_fruit_definition_ids = {
                242040: BBSItemRarity.COMMON,  # gardenFruit_EP09GENsoybean
            }
            fruit_definition_ids.update(ep7_fruit_definition_ids)

        if Pack.EP11 in available_packs:
            ep11_fruit_definition_ids = {
                270185: BBSItemRarity.RARE,  # gardenFruitCropLarge_EP11GENAubergine_set1
                270186: BBSItemRarity.RARE,  # gardenFruitCropLarge_EP11GENLettuce_set1
                270187: BBSItemRarity.EXOTIC,  # gardenFruitCropLarge_EP11GENPumpkin_set1
                286426: BBSItemRarity.EXOTIC,  # gardenFruitCropLarge_EP11GENPumpkin_set2
                286427: BBSItemRarity.EXOTIC,  # gardenFruitCropLarge_EP11GENPumpkin_set3
                271873: BBSItemRarity.EXOTIC,  # gardenFruitCropLarge_EP11GENWatermelon_set1
                283842: BBSItemRarity.EXOTIC,  # gardenFruitCropLarge_EP11GENmushroom_set1
                270295: BBSItemRarity.UNCOMMON,  # gardenFruitCropMedium_EP11GENAubergine_set1
                270297: BBSItemRarity.UNCOMMON,  # gardenFruitCropMedium_EP11GENLettuce_set1
                270299: BBSItemRarity.RARE,  # gardenFruitCropMedium_EP11GENPumpkin_set1
                286424: BBSItemRarity.RARE,  # gardenFruitCropMedium_EP11GENPumpkin_set2
                286425: BBSItemRarity.RARE,  # gardenFruitCropMedium_EP11GENPumpkin_set3
                271875: BBSItemRarity.RARE,  # gardenFruitCropMedium_EP11GENWatermelon_set1
                283840: BBSItemRarity.RARE,  # gardenFruitCropMedium_EP11GENmushroom_set1
                270289: BBSItemRarity.COMMON,  # gardenFruitCropSmall_EP11GENAubergine_set1
                270291: BBSItemRarity.COMMON,  # gardenFruitCropSmall_EP11GENLettuce_set1
                270293: BBSItemRarity.UNCOMMON,  # gardenFruitCropSmall_EP11GENPumpkin_set1
                286422: BBSItemRarity.UNCOMMON,  # gardenFruitCropSmall_EP11GENPumpkin_set2
                286423: BBSItemRarity.UNCOMMON,  # gardenFruitCropSmall_EP11GENPumpkin_set3
                271877: BBSItemRarity.UNCOMMON,  # gardenFruitCropSmall_EP11GENWatermelon_set1
                283838: BBSItemRarity.UNCOMMON,  # gardenFruitCropSmall_EP11GENmushroom_set1
                270257: BBSItemRarity.COMMON,  # gardenFruit_EP11GENBlueberry_set1
                286364: BBSItemRarity.COMMON,  # gardenFruit_EP11GENMushroomWildBasic
                272255: BBSItemRarity.COMMON,  # gardenFruit_EP11GENMushroomWildSpicy
                272253: BBSItemRarity.COMMON,  # gardenFruit_EP11GENMushroomWildVerdant
                270259: BBSItemRarity.COMMON,  # gardenFruit_EP11GENRaspberry_set1
                272254: BBSItemRarity.COMMON,  # gardenFruit_EP11GENmushroomWildCharming
                272256: BBSItemRarity.COMMON,  # gardenFruit_EP11GENmushroomWildLovely
                271725: BBSItemRarity.COMMON,  # gardenFruit_EP11GENmushroomWildMysterious
                270260: BBSItemRarity.COMMON,  # gardenFruit_EP11GENmushroomWildNightly
            }
            fruit_definition_ids.update(ep11_fruit_definition_ids)

        if Pack.GP01 in available_packs:
            gp1_fruit_definition_ids = {
                66140: BBSItemRarity.EXOTIC,  # gardenFruit_GP01GENelderberry
                67556: BBSItemRarity.RARE,  # gardenFruit_GP01GENhuckleberry
                66145: BBSItemRarity.UNCOMMON,  # gardenFruit_GP01GENmushroomMorel
            }
            fruit_definition_ids.update(gp1_fruit_definition_ids)

        if Pack.GP04 in available_packs:
            gp4_fruit_definition_ids = {
                147404: BBSItemRarity.COMMON,  # gardenFruit_GP04GENmosquito
                144964: BBSItemRarity.EXOTIC,  # gardenFruit_GP04GENplasma
            }
            fruit_definition_ids.update(gp4_fruit_definition_ids)

        if Pack.GP06 in available_packs:
            gp6_fruit_definition_ids = {
                178855: BBSItemRarity.COMMON,  # gardenFruit_GP06GENBlackBean
                187285: BBSItemRarity.COMMON,  # gardenFruit_GP06GENBlackBean_01
                178801: BBSItemRarity.EXOTIC,  # gardenFruit_GP06GENEmotionalBerry_confident
                178802: BBSItemRarity.EXOTIC,  # gardenFruit_GP06GENEmotionalBerry_energized
                178803: BBSItemRarity.EXOTIC,  # gardenFruit_GP06GENEmotionalBerry_flirty
                178804: BBSItemRarity.EXOTIC,  # gardenFruit_GP06GENEmotionalBerry_focused
                178800: BBSItemRarity.EXOTIC,  # gardenFruit_GP06GENEmotionalBerry_happy
                178805: BBSItemRarity.EXOTIC,  # gardenFruit_GP06GENEmotionalBerry_inspired
                178806: BBSItemRarity.EXOTIC,  # gardenFruit_GP06GENEmotionalBerry_playful
                178808: BBSItemRarity.COMMON,  # gardenFruit_GP06GENavocado
                187283: BBSItemRarity.COMMON,  # gardenFruit_GP06GENavocado_01
            }
            fruit_definition_ids.update(gp6_fruit_definition_ids)

        if Pack.GP08 in available_packs:
            gp6_fruit_definition_ids = {
                227207: BBSItemRarity.COMMON,  # gardenFruit_GP08GENmandrake
                227209: BBSItemRarity.COMMON,  # gardenFruit_GP08GENvalerian
            }
            fruit_definition_ids.update(gp6_fruit_definition_ids)

        return fruit_definition_ids

    @classmethod
    def get_available_animals(cls) -> Dict[int, BBSItemRarity]:
        """get_available_animals()

        Retrieve available Animals for scavenging.

        :return: A dictionary of object definition ids to the rarity of the item being obtained.
        :rtype: Dict[int, BBSItemRarity]
        """
        from sims4.common import get_available_packs
        available_packs = get_available_packs()

        animal_definition_ids = dict()

        if Pack.EP11 in available_packs:
            ep11_animal_definition_ids = {
                # Chickens
                266636: BBSItemRarity.COMMON,  # animalAvianChicken_EP11GEN_set1 (White Hen)
                263031: BBSItemRarity.COMMON,  # animalAvianRooster_EP11GEN_set1 (White Rooster)
                281877: BBSItemRarity.UNCOMMON,  # animalAvianChicken_EP11GEN_set2 (Brown Hen)
                281880: BBSItemRarity.UNCOMMON,  # animalAvianRooster_EP11GEN_set2 (Brown Rooster)
                281878: BBSItemRarity.RARE,  # animalAvianChicken_EP11GEN_set3 (Black Hen)
                281881: BBSItemRarity.RARE,  # animalAvianRooster_EP11GEN_set3 (Black Rooster)
                268719: BBSItemRarity.COMMON,  # animalAvianChick_EP11GEN (Chick Hen)
                283181: BBSItemRarity.COMMON,  # animalAvianChickRooster_EP11GEN (Chick Rooster)
                277970: BBSItemRarity.EXOTIC,  # animalAvianChicken_EP11GEN_golden (Golden Hen)
                277973: BBSItemRarity.EXOTIC,  # animalAvianRooster_EP11GEN_golden (Golden Rooster)
                277971: BBSItemRarity.EXOTIC,  # animalAvianChicken_EP11GEN_evil (Evil Hen)
                277972: BBSItemRarity.EXOTIC,  # animalAvianRooster_EP11GEN_evil (Evil Rooster)
                # Cow
                264866: BBSItemRarity.UNCOMMON,  # animalCow_EP11GEN_set1 (Spotted Cow)
                279057: BBSItemRarity.UNCOMMON,  # animalCow_EP11GEN_set3 (Cow)
                276585: BBSItemRarity.RARE,  # animalCow_EP11GEN_set2 (Brown Cow)
                # Llama
                269148: BBSItemRarity.COMMON,  # animalLlama_EP11GEN_set1 (White Llama)
                272077: BBSItemRarity.COMMON,  # animalLlama_EP11GEN_set2 (Beige Llama)
                272078: BBSItemRarity.UNCOMMON,  # animalLlama_EP11GEN_set3 (Pink Llama)
                278859: BBSItemRarity.UNCOMMON,  # animalLlama_EP11GEN_set4 (Brown Llama)
                278860: BBSItemRarity.RARE,  # animalLlama_EP11GEN_set5 (Red Llama)
                278861: BBSItemRarity.RARE,  # animalLlama_EP11GEN_set6 (Orange Llama)
                278862: BBSItemRarity.RARE,  # animalLlama_EP11GEN_set7 (Blue Llama)
                278863: BBSItemRarity.RARE,  # animalLlama_EP11GEN_set8 (Green Llama)
                278864: BBSItemRarity.EXOTIC,  # animalLlama_EP11GEN_set9 (Rainbow Llama)
                278865: BBSItemRarity.RARE,  # animalLlama_EP11GEN_set10 (Orange Llama)
                278866: BBSItemRarity.UNCOMMON,  # animalLlama_EP11GEN_set11 (Black Llama)
            }
            animal_definition_ids.update(ep11_animal_definition_ids)

        if Pack.EP14 in available_packs:
            ep14_animal_definition_ids = {
                # Sheep
                338596: BBSItemRarity.UNCOMMON,  # animalSheepMini_EP14GEN_set1 (White Sheep)
                351751: BBSItemRarity.UNCOMMON,  # animalSheepMini_EP14GEN_set2 (Cream Sheep)
                351752: BBSItemRarity.RARE,  # animalSheepMini_EP14GEN_set3 (Pink Sheep)
                351753: BBSItemRarity.UNCOMMON,  # animalSheepMini_EP14GEN_set4 (Brown Sheep)
                351754: BBSItemRarity.EXOTIC,  # animalSheepMini_EP14GEN_set5 (Red Sheep)
                351755: BBSItemRarity.EXOTIC,  # animalSheepMini_EP14GEN_set6 (Orange Sheep)
                351756: BBSItemRarity.RARE,  # animalSheepMini_EP14GEN_set7 (Blue Sheep)
                351757: BBSItemRarity.EXOTIC,  # animalSheepMini_EP14GEN_set8 (Green Sheep)
                351758: BBSItemRarity.UNCOMMON,  # animalSheepMini_EP14GEN_set9 (Black Sheep)
                351812: BBSItemRarity.EXOTIC,  # animalSheepMini_EP14GEN_set10 (Dalmatian Sheep)
                351852: BBSItemRarity.RARE,  # animalSheepMini_EP14GEN_set11 (Mocha Sheep)
                # Goat
                328494: BBSItemRarity.UNCOMMON,  # animalGoatMini_EP14GEN_set1 (White Goat)
                346691: BBSItemRarity.UNCOMMON,  # animalGoatMini_EP14GEN_set2 (Gray Goat)
                346692: BBSItemRarity.RARE,  # animalGoatMini_EP14GEN_set3 (Black Goat)
                346693: BBSItemRarity.EXOTIC,  # animalGoatMini_EP14GEN_set4 (Dalmatian Goat)
                346694: BBSItemRarity.UNCOMMON,  # animalGoatMini_EP14GEN_set5 (Brown Goat)
                346849: BBSItemRarity.UNCOMMON,  # animalGoatMini_EP14GEN_set6 (White Belt Goat)
                347200: BBSItemRarity.RARE,  # animalGoatMini_EP14GEN_set7 (Chamoisee Goat)
                347201: BBSItemRarity.UNCOMMON,  # animalGoatMini_EP14GEN_set8 (Spotted Goat)
            }
            animal_definition_ids.update(ep14_animal_definition_ids)

        return animal_definition_ids

    @classmethod
    def get_available_ingredients(cls) -> Dict[int, BBSItemRarity]:
        """get_available_ingredients()

        Retrieve available Ingredients for scavenging.

        :return: A dictionary of object definition ids to the rarity of the item being obtained.
        :rtype: Dict[int, BBSItemRarity]
        """
        from sims4.common import get_available_packs
        available_packs = get_available_packs()

        ingredient_definition_ids = {
            # Other
            278715: BBSItemRarity.COMMON,  # foodIngredient_GENsack_flour
            278719: BBSItemRarity.COMMON,  # foodIngredient_GENMeat01_whiteMeat
            278923: BBSItemRarity.COMMON,  # foodIngredient_GENMeat01_redMeat
            278924: BBSItemRarity.COMMON,  # foodIngredient_GENsack_sugar
        }

        if Pack.EP11 in available_packs:
            ep11_ingredient_definition_ids = {
                # Milk
                271852: BBSItemRarity.COMMON,  # drinkBottle_EP11GENmilk_set1_base
                277732: BBSItemRarity.UNCOMMON,  # drinkBottle_EP11GENmilk_set1_blue
                277735: BBSItemRarity.RARE,  # drinkBottle_EP11GENmilk_set1_green
                277731: BBSItemRarity.RARE,  # drinkBottle_EP11GENmilk_set2_black
                277733: BBSItemRarity.RARE,  # drinkBottle_EP11GENmilk_set3_brown
                277734: BBSItemRarity.EXOTIC,  # drinkBottle_EP11GENmilk_set4_gold
                277736: BBSItemRarity.RARE,  # drinkBottle_EP11GENmilk_set5_orange
                277737: BBSItemRarity.RARE,  # drinkBottle_EP11GENmilk_set6_pink
                277794: BBSItemRarity.EXOTIC,  # drinkBottle_EP11GENmilk_set7_rainbow
                277795: BBSItemRarity.RARE,  # drinkBottle_EP11GENmilk_set8_red
                # Eggs
                266633: BBSItemRarity.COMMON,  # egg_EP11GEN_set1_white
                272308: BBSItemRarity.EXOTIC,  # egg_EP11GEN_set2_Gold
                272309: BBSItemRarity.RARE,  # egg_EP11GEN_set3_Chocolate
                272310: BBSItemRarity.EXOTIC,  # egg_EP11GEN_set4_obsidian
                272311: BBSItemRarity.EXOTIC,  # egg_EP11GEN_set5_Blue
                272312: BBSItemRarity.RARE,  # egg_EP11GEN_set6_Green
                272313: BBSItemRarity.RARE,  # egg_EP11GEN_set7_Orange
                272314: BBSItemRarity.EXOTIC,  # egg_EP11GEN_set8_Rainbow
                284595: BBSItemRarity.UNCOMMON,  # eggHatchable_EP11GEN_set1_white
                284596: BBSItemRarity.RARE,  # eggHatchable_EP11GEN_set4_obsidian
                284597: BBSItemRarity.EXOTIC,  # eggHatchable_EP11GEN_set2_Gold
                # Other
                270258: BBSItemRarity.UNCOMMON,  # gardenFruit_EP11GENChocolateBerry_set1
            }
            ingredient_definition_ids.update(ep11_ingredient_definition_ids)

        return ingredient_definition_ids

    @classmethod
    def get_available_minerals(cls) -> Dict[int, BBSItemRarity]:
        """get_available_minerals()

        Retrieve available Minerals for scavenging.

        :return: A dictionary of object definition ids to the rarity of the item being obtained.
        :rtype: Dict[int, BBSItemRarity]
        """
        from sims4.common import get_available_packs
        available_packs = get_available_packs()

        mineral_definition_ids = {
            # Metals
            28759: BBSItemRarity.UNCOMMON,  # collectMetalMedGEN_01_crytunium
            28760: BBSItemRarity.RARE,  # collectMetalMedGEN_01_furium
            28761: BBSItemRarity.COMMON,  # collectMetalMedGEN_01_heavyMetal
            28764: BBSItemRarity.UNCOMMON,  # collectMetalMedGEN_01_ironyum
            28771: BBSItemRarity.COMMON,  # collectMetalMedGEN_01_ozinold
            28772: BBSItemRarity.COMMON,  # collectMetalMedGEN_01_plathinum
            28773: BBSItemRarity.RARE,  # collectMetalMedGEN_01_romantium
            28774: BBSItemRarity.RARE,  # collectMetalMedGEN_01_sadnum
            28775: BBSItemRarity.UNCOMMON,  # collectMetalMedGEN_01_simtanium
            28776: BBSItemRarity.COMMON,  # collectMetalMedGEN_01_utranium
            28777: BBSItemRarity.COMMON,  # collectMetalSmGEN_01_alcron
            28778: BBSItemRarity.COMMON,  # collectMetalSmGEN_01_baconite
            28779: BBSItemRarity.UNCOMMON,  # collectMetalSmGEN_01_deathMetal
            28780: BBSItemRarity.UNCOMMON,  # collectMetalSmGEN_01_flamingonium
            28781: BBSItemRarity.RARE,  # collectMetalSmGEN_01_literalite
            28782: BBSItemRarity.COMMON,  # collectMetalSmGEN_01_obtainium
            28783: BBSItemRarity.COMMON,  # collectMetalSmGEN_01_phozonite
            28784: BBSItemRarity.COMMON,  # collectMetalSmGEN_01_punium
            28785: BBSItemRarity.COMMON,  # collectMetalSmGEN_01_pyrite
            28786: BBSItemRarity.UNCOMMON,  # collectMetalSmGEN_01_socialite
            # Crystals
            28727: BBSItemRarity.UNCOMMON,  # collectCrystalSmGEN_01_amethyst
            28728: BBSItemRarity.UNCOMMON,  # collectCrystalSmGEN_01_diamond
            28729: BBSItemRarity.COMMON,  # collectCrystalSmGEN_01_emerald
            28730: BBSItemRarity.UNCOMMON,  # collectCrystalSmGEN_01_hematite
            28731: BBSItemRarity.RARE,  # collectCrystalSmGEN_01_jonquilyst
            28732: BBSItemRarity.COMMON,  # collectCrystalSmGEN_01_orangeTopaz
            28733: BBSItemRarity.COMMON,  # collectCrystalSmGEN_01_peach
            28734: BBSItemRarity.RARE,  # collectCrystalSmGEN_01_rainborz
            28735: BBSItemRarity.COMMON,  # collectCrystalSmGEN_01_sapphire
            28736: BBSItemRarity.UNCOMMON,  # collectCrystalSmGEN_01_simanite
            28738: BBSItemRarity.COMMON,  # collectCrystalMedGEN_01_alabaster
            28739: BBSItemRarity.COMMON,  # collectCrystalMedGEN_01_citrine
            28740: BBSItemRarity.UNCOMMON,  # collectCrystalMedGEN_01_fireOpal
            28741: BBSItemRarity.RARE,  # collectCrystalMedGEN_01_jet
            28743: BBSItemRarity.RARE,  # collectCrystalMedGEN_01_plumbite
            28744: BBSItemRarity.COMMON,  # collectCrystalMedGEN_01_quartz
            28747: BBSItemRarity.COMMON,  # collectCrystalMedGEN_01_rose
            28748: BBSItemRarity.COMMON,  # collectCrystalMedGEN_01_ruby
            28749: BBSItemRarity.UNCOMMON,  # collectCrystalMedGEN_01_shinalite
            28750: BBSItemRarity.COMMON,  # collectCrystalMedGEN_01_turquoise
        }

        if Pack.EP01 in available_packs:
            ep01_mineral_definition_ids = {
                # Metals
                72392: BBSItemRarity.EXOTIC,  # collectMetalMed_EP01GENblutonium
                72394: BBSItemRarity.EXOTIC,  # collectMetalMed_EP01GENsolarium
                # Crystals
                72395: BBSItemRarity.EXOTIC,  # collectCrystalMed_EP01GEN_crandestine
                72396: BBSItemRarity.EXOTIC,  # collectCrystalMed_EP01GEN_nitelite
            }
            mineral_definition_ids.update(ep01_mineral_definition_ids)

        if Pack.GP06 in available_packs:
            gp06_mineral_definition_ids = {
                # Crystals
                178735: BBSItemRarity.RARE,  # collectCrystalMed_GP06GEN_alexandrite
                178736: BBSItemRarity.UNCOMMON,  # collectCrystalMed_GP06GEN_amazonite
            }
            mineral_definition_ids.update(gp06_mineral_definition_ids)

        return mineral_definition_ids

    @classmethod
    def give_scavenge_rewards(
        cls,
        scavenger_sim_info: SimInfo,
        run_length: BBSScavengingRunLength,
        to_receive_sim_info: SimInfo = None
    ) -> None:
        """give_scavenge_rewards(scavenger_sim_info, run_length, to_receive_sim_info=None)

        Give scavenging Rewards to a Sim.

        :param scavenger_sim_info: The info of a Sim.
        :type scavenger_sim_info: SimInfo
        :param run_length: The length of the scavenging run.
        :type run_length: BBSScavengingRunLength
        :param to_receive_sim_info: The info of the Sim to receive the rewards from the scavenger. Default is the Scavenger
        :type to_receive_sim_info: SimInfo, optional
        """
        if to_receive_sim_info is None:
            to_receive_sim_info = scavenger_sim_info

        log = cls.get_log()
        try:
            log.debug('Giving scavenge rewards', sim=scavenger_sim_info, target_of_rewards=to_receive_sim_info)
            simoleons_found = cls.reward_currency(to_receive_sim_info, run_length)

            received_items: List[Tuple[GameObject, int]] = list()

            def _add_received_item(_game_object: GameObject, _item_count: int):
                received_items.append((_game_object, _item_count))

            # Spawn Seeds
            seed_definition_ids = cls.get_available_seeds()
            cls.reward_items(BBSScavengedItemType.SEED, seed_definition_ids, scavenger_sim_info, to_receive_sim_info, run_length, _add_received_item)

            fruit_definition_ids = cls.get_available_fruits()
            cls.reward_items(BBSScavengedItemType.FRUIT, fruit_definition_ids, scavenger_sim_info, to_receive_sim_info, run_length, _add_received_item)

            animal_definition_ids = cls.get_available_animals()
            cls.reward_items(BBSScavengedItemType.ANIMAL, animal_definition_ids, scavenger_sim_info, to_receive_sim_info, run_length, _add_received_item)

            ingredient_definition_ids = cls.get_available_ingredients()
            cls.reward_items(BBSScavengedItemType.INGREDIENT, ingredient_definition_ids, scavenger_sim_info, to_receive_sim_info, run_length, _add_received_item)

            mineral_definition_ids = cls.get_available_minerals()
            cls.reward_items(BBSScavengedItemType.MINERAL, mineral_definition_ids, scavenger_sim_info, to_receive_sim_info, run_length, _add_received_item)

            cls.display_rewards_notification(scavenger_sim_info, to_receive_sim_info, received_items, simoleons_found)
        except Exception as ex:
            log.error('An error occurred rewarding scavenging rewards.', exception=ex)

    @classmethod
    def display_rewards_notification(
        cls,
        scavenger_sim_info: SimInfo,
        to_receive_sim_info: SimInfo,
        received_items: List[Tuple[GameObject, int]],
        simoleons_found: int
    ):
        """display_rewards_notification(scavenger_sim_info, to_receive_sim_info, received_items, simoleons_found)

        Display a notification indicating what a Sim was rewarded with during scavenging.

        :param scavenger_sim_info: The Sim that went scavenging.
        :type scavenger_sim_info: SimInfo
        :param to_receive_sim_info: The Sim that received the scavenged items.
        :type to_receive_sim_info: SimInfo
        :param received_items: The items received while scavenging and how many was received.
        :type received_items: List[Tuple[GameObject, int]]
        :param simoleons_found: The number of simoleons found while scavenging.
        :type simoleons_found: int
        :return:
        """
        log = cls.get_log()
        # Create the notification that indicates the items received.
        try:
            received_item_strings = list()
            scavenging_sim = BBSimUtils.to_sim_instance(scavenger_sim_info)
            to_receive_sim = BBSimUtils.to_sim_instance(to_receive_sim_info)

            if simoleons_found > 0:
                received_item_strings.append(BBLocalizationUtils.to_localized_string(BBSStringId.STRING_SIMOLEONS, tokens=(str(simoleons_found),)))

            if received_items:
                for (received_item, item_count) in received_items:
                    catalog_name = received_item.custom_name if received_item.has_custom_name() else received_item.catalog_name
                    log.debug('Got item definition', received_item=received_item, catalog_name=catalog_name, definition_id=str(received_item.definition.id))
                    if log.is_enabled():
                        # noinspection PyTypeChecker
                        received_item_strings.append(
                            BBLocalizationUtils.to_localized_string(
                                BBStringId.BBL_STRING_PARENTHESIS_STRING,
                                tokens=(
                                    BBLocalizationUtils.to_localized_string(catalog_name, tokens=(item_count,), normalize_tokens=False),
                                    str(received_item.definition.id)
                                )
                            )
                        )
                    else:
                        received_item_strings.append(BBLocalizationUtils.to_localized_string(catalog_name, tokens=(item_count,), normalize_tokens=False))

            if received_item_strings:
                text = BBLocalizationUtils.combine_strings(received_item_strings, separator_text=BBStringId.BBL_STRING_NEWLINE_STRING)

                BBNotification(
                    cls.get_mod_identity(),
                    BBLocalizedStringData(BBSStringId.FOUND_WHILE_SCAVENGING),
                    BBLocalizedStringData(text)
                ).show(icon=BBSimIconInfo(scavenger_sim_info), secondary_icon=BBSimIconInfo(to_receive_sim_info) if scavenger_sim_info is not to_receive_sim_info else None)
        except Exception as ex:
            log.error('An error occurred displaying notification', exception=ex)

    @classmethod
    def reward_currency(
        cls,
        to_receive_sim_info: SimInfo,
        run_length: BBSScavengingRunLength
    ) -> int:
        log = cls.get_log()
        scavenge_random = Random()
        simoleons_found = scavenge_random.randint(
            (cls.MIN_SIMOLEONS_PER_QUICK_RUN if cls.MIN_SIMOLEONS_PER_QUICK_RUN < cls.MAX_SIMOLEONS_PER_QUICK_RUN else cls.MAX_SIMOLEONS_PER_QUICK_RUN) * int(run_length),
            cls.MAX_SIMOLEONS_PER_QUICK_RUN * int(run_length)
        )
        log.debug('Simoleons found', simoleons_found=simoleons_found)
        BBSimCurrencyUtils.add_simoleons(to_receive_sim_info, simoleons_found)
        return simoleons_found

    @classmethod
    def reward_items(
        cls,
        scavenged_item_type: BBSScavengedItemType,
        item_definition_ids: Dict[int, BBSItemRarity],
        scavenger_sim_info: SimInfo,
        to_receive_sim_info: SimInfo,
        run_length: BBSScavengingRunLength,
        on_item_added: Callable[[GameObject, int], None]
    ):
        """reward_items(\
            scavenged_item_type,\
            item_definition_ids,\
            scavenger_sim_info,\
            to_receive_sim_info,\
            run_length,\
            on_item_added\
        )

        :param scavenged_item_type:
        :param item_definition_ids:
        :param scavenger_sim_info:
        :param to_receive_sim_info:
        :param run_length:
        :param on_item_added:
        :return:
        """
        item_name = scavenged_item_type.name
        item_chance = cls.ITEM_CHANCE[scavenged_item_type]
        base_item_count = cls.ITEMS_PER_QUICK_RUN[scavenged_item_type] * int(run_length)
        log = cls.get_log()
        scavenge_random = Random()
        item_dice_roll = scavenge_random.random()
        if item_dice_roll < item_chance:
            rarity_chances = cls.RARITY_CHANCES
            log.debug(f'Giving random {item_name}.', item_chance=item_chance, item_dice_roll=item_dice_roll)
            chosen_items = scavenge_random.sample(tuple(item_definition_ids.keys()), base_item_count)
            to_add_items = list()
            for chosen_item in chosen_items:
                chosen_item_rarity = item_definition_ids[chosen_item]
                chosen_item_chance = rarity_chances[chosen_item_rarity]
                if scavenge_random.random() < chosen_item_chance:
                    to_add_items.append(chosen_item)
            log.debug(f'Chose {item_name}', chosen_items=chosen_items, to_add_items=to_add_items)

            item_count = 1

            def _on_item_added(_game_object: GameObject):
                on_item_added(_game_object, item_count)

            for to_add_mineral in to_add_items:
                BBSimInventoryUtils.create_in_inventory(to_receive_sim_info, to_add_mineral, on_added=_on_item_added)
        else:
            log.debug(f'Not giving {item_name}', item_chance=item_chance, item_dice_roll=item_dice_roll)
