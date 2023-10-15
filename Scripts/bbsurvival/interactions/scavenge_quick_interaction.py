"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import random
from typing import Any

from bbsurvival.bb_lib.utils.bb_sim_currency_utils import BBSimCurrencyUtils
from bbsurvival.bb_lib.utils.bb_sim_inventory_utils import BBSimInventoryUtils
from bbsurvival.bb_lib.utils.bb_sim_rabbit_hole_utils import BBSimRabbitHoleUtils
from bbsurvival.enums.rabbit_hole_ids import BBSRabbitHoleId
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.classes.bb_test_result import BBTestResult
from bluuberrylibrary.interactions.classes.bb_super_interaction import BBSuperInteraction
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from sims.sim_info import SimInfo


class BBSScavengeQuickInteraction(BBSuperInteraction):
    """Scavenge quickly for supplies."""

    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        return ModIdentity()

    @classmethod
    def get_log_name(cls) -> str:
        return 'bbs_scavenge_quick_interaction'

    def bbl_started(self, interaction_sim_info: SimInfo, interaction_target: Any) -> BBTestResult:
        def _on_leave_rabbit_hole(_sim_info: SimInfo, cancelled: bool):
            if cancelled:
                return
            self._give_scavenge_rewards(_sim_info)

        success = BBSimRabbitHoleUtils.send_into_rabbit_hole(interaction_sim_info, BBSRabbitHoleId.SCAVENGE_QUICK, on_leave_rabbit_hole=_on_leave_rabbit_hole)

        if success:
            return BBTestResult.TRUE
        return BBTestResult(False, success.reason)

    def _give_scavenge_rewards(self, sim_info: SimInfo) -> None:
        simoleons_found = random.randint(0, 200)
        BBSimCurrencyUtils.add_simoleons(sim_info, simoleons_found)
        # Spawn Seeds
        seed_definition_ids = (
            59678,  # seedPacket_Garden_Starter_Fruits
            59676,  # seedPacket_Garden_Starter_Flowers
            59679,  # seedPacket_Garden_Starter_Herbs
            59680,  # seedPacket_Garden_Starter_Vegetables
            62723,  # seedPacket_Garden_Starter_Deluxe_FlowersFruit
            62724,  # seedPacket_Garden_Starter_Deluxe_VegetablesHerbs
            176694,  # seedPacket_Garden_Starter_Catnip
            228500,  # seedPacket_Garden_Starter_Magic
            188697,  # seedPacket_Garden_EP05_summer
            188699,  # seedPacket_Garden_EP05_fall
            188700,  # seedPacket_Garden_EP05_winter
            188702,  # seedPacket_Garden_EP05_spring
            193547,  # seedPacket_Garden_rare
            193549,  # seedPacket_Garden_uncommon
        )

        seed_chance = 0.2

        chosen_seed = random.choice(seed_definition_ids)
        log = self.get_log()
        log.debug('Chose seed', seed=chosen_seed)
        result = BBSimInventoryUtils.create_in_inventory(sim_info, chosen_seed)
        created_object = result.result
        log.debug('Created seed', created_object=created_object, result=result)

        fruit_definition_ids = (
            270185,  # gardenFruitCropLarge_EP11GENAubergine_set1
            270186,  # gardenFruitCropLarge_EP11GENLettuce_set1
            270187,  # gardenFruitCropLarge_EP11GENPumpkin_set1
            286426,  # gardenFruitCropLarge_EP11GENPumpkin_set2
            286427,  # gardenFruitCropLarge_EP11GENPumpkin_set3
            271873,  # gardenFruitCropLarge_EP11GENWatermelon_set1
            283842,  # gardenFruitCropLarge_EP11GENmushroom_set1
            270295,  # gardenFruitCropMedium_EP11GENAubergine_set1
            270297,  # gardenFruitCropMedium_EP11GENLettuce_set1
            270299,  # gardenFruitCropMedium_EP11GENPumpkin_set1
            286424,  # gardenFruitCropMedium_EP11GENPumpkin_set2
            286425,  # gardenFruitCropMedium_EP11GENPumpkin_set3
            271875,  # gardenFruitCropMedium_EP11GENWatermelon_set1
            283840,  # gardenFruitCropMedium_EP11GENmushroom_set1
            270289,  # gardenFruitCropSmall_EP11GENAubergine_set1
            270291,  # gardenFruitCropSmall_EP11GENLettuce_set1
            270293,  # gardenFruitCropSmall_EP11GENPumpkin_set1
            286422,  # gardenFruitCropSmall_EP11GENPumpkin_set2
            286423,  # gardenFruitCropSmall_EP11GENPumpkin_set3
            271877,  # gardenFruitCropSmall_EP11GENWatermelon_set1
            283838,  # gardenFruitCropSmall_EP11GENmushroom_set1
            165689,  # gardenFruitEF05GENforbiddenFruit
            29009,  # gardenFruitGENAlien_01
            21939,  # gardenFruitGENApple_01
            23438,  # gardenFruitGENBlackberry_01
            45767,  # gardenFruitGENBonsai
            45299,  # gardenFruitGENCarrot_01
            22467,  # gardenFruitGENCherry_01
            37858,  # gardenFruitGENCowplant_01
            23440,  # gardenFruitGENDragon_01
            23442,  # gardenFruitGENGrapes_01
            22466,  # gardenFruitGENLemon_01
            45311,  # gardenFruitGENMushroom_01
            23445,  # gardenFruitGENPear_01
            22468,  # gardenFruitGENPlantain_01
            23439,  # gardenFruitGENPomegranate_01
            23437,  # gardenFruitGENStrawberry_01
            46336,  # gardenFruitGENTomato_01
            188687,  # gardenFruit_EP05GENgreenBeans
            188689,  # gardenFruit_EP05GENgreenPeppers
            188693,  # gardenFruit_EP05GENmoney
            188691,  # gardenFruit_EP05GENpeas
            215737,  # gardenFruit_EP07GENcoconut
            213665,  # gardenFruit_EP07GENkava
            215738,  # gardenFruit_EP07GENpineapple
            242040,  # gardenFruit_EP09GENsoybean
            270257,  # gardenFruit_EP11GENBlueberry_set1
            286364,  # gardenFruit_EP11GENMushroomWildBasic
            272255,  # gardenFruit_EP11GENMushroomWildSpicy
            272253,  # gardenFruit_EP11GENMushroomWildVerdant
            270259,  # gardenFruit_EP11GENRaspberry_set1
            272254,  # gardenFruit_EP11GENmushroomWildCharming
            272256,  # gardenFruit_EP11GENmushroomWildLovely
            271725,  # gardenFruit_EP11GENmushroomWildMysterious
            270260,  # gardenFruit_EP11GENmushroomWildNightly
            125468,  # gardenFruit_GENGrowfruit_01
            66140,  # gardenFruit_GP01GENelderberry
            67556,  # gardenFruit_GP01GENhuckleberry
            66145,  # gardenFruit_GP01GENmushroomMorel
            147404,  # gardenFruit_GP04GENmosquito
            144964,  # gardenFruit_GP04GENplasma
            178855,  # gardenFruit_GP06GENBlackBean
            187285,  # gardenFruit_GP06GENBlackBean_01
            178801,  # gardenFruit_GP06GENEmotionalBerry_confident
            178802,  # gardenFruit_GP06GENEmotionalBerry_energized
            178803,  # gardenFruit_GP06GENEmotionalBerry_flirty
            178804,  # gardenFruit_GP06GENEmotionalBerry_focused
            178800,  # gardenFruit_GP06GENEmotionalBerry_happy
            178805,  # gardenFruit_GP06GENEmotionalBerry_inspired
            178806,  # gardenFruit_GP06GENEmotionalBerry_playful
            178808,  # gardenFruit_GP06GENavocado
            187283,  # gardenFruit_GP06GENavocado_01
            227207,  # gardenFruit_GP08GENmandrake
            227209,  # gardenFruit_GP08GENvalerian
        )

        fruit_chance = 0.2

        chosen_fruit = random.choice(fruit_definition_ids)
        BBSimInventoryUtils.create_in_inventory(sim_info, chosen_fruit)

        # Add milk, flour, chocolate, eggs, and other grocery items.
