"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Tuple

from bbsurvival.enums.interaction_ids import BBSInteractionId
from bluuberrylibrary.interactions.registration.bb_interaction_registry import BBInteractionRegistry
from bluuberrylibrary.interactions.registration.handlers.bb_object_interaction_handler import BBObjectInteractionHandler
from objects.game_object import GameObject


@BBInteractionRegistry.register()
class _BBSLightOnFireObjectInteractionRegistration(BBObjectInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        return (
            BBSInteractionId.LIGHT_ON_FIRE,
        )

    def get_excluded_definition_ids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            # Chickens
            266636,  # animalAvianChicken_EP11GEN_set1 (White Hen)
            263031,  # animalAvianRooster_EP11GEN_set1 (White Rooster)
            281877,  # animalAvianChicken_EP11GEN_set2 (Brown Hen)
            281880,  # animalAvianRooster_EP11GEN_set2 (Brown Rooster)
            281878,  # animalAvianChicken_EP11GEN_set3 (Black Hen)
            281881,  # animalAvianRooster_EP11GEN_set3 (Black Rooster)
            268719,  # animalAvianChick_EP11GEN (Chick Hen)
            283181,  # animalAvianChickRooster_EP11GEN (Chick Rooster)
            277970,  # animalAvianChicken_EP11GEN_golden (Golden Hen)
            277973,  # animalAvianRooster_EP11GEN_golden (Golden Rooster)
            277971,  # animalAvianChicken_EP11GEN_evil (Evil Hen)
            277972,  # animalAvianRooster_EP11GEN_evil (Evil Rooster)
            # Cow
            264866,  # animalCow_EP11GEN_set1 (Spotted Cow)
            279057,  # animalCow_EP11GEN_set3 (Cow)
            276585,  # animalCow_EP11GEN_set2 (Brown Cow)
            # Llama
            269148,  # animalLlama_EP11GEN_set1 (White Llama)
            272077,  # animalLlama_EP11GEN_set2 (Beige Llama)
            272078,  # animalLlama_EP11GEN_set3 (Pink Llama)
            278859,  # animalLlama_EP11GEN_set4 (Brown Llama)
            278860,  # animalLlama_EP11GEN_set5 (Red Llama)
            278861,  # animalLlama_EP11GEN_set6 (Orange Llama)
            278862,  # animalLlama_EP11GEN_set7 (Blue Llama)
            278863,  # animalLlama_EP11GEN_set8 (Green Llama)
            278864,  # animalLlama_EP11GEN_set9 (Rainbow Llama)
            278865,  # animalLlama_EP11GEN_set10 (Orange Llama)
            278866,  # animalLlama_EP11GEN_set11 (Black Llama)
            # Sheep
            338596,  # animalSheepMini_EP14GEN_set1 (White Sheep)
            351751,  # animalSheepMini_EP14GEN_set2 (Cream Sheep)
            351752,  # animalSheepMini_EP14GEN_set3 (Pink Sheep)
            351753,  # animalSheepMini_EP14GEN_set4 (Brown Sheep)
            351754,  # animalSheepMini_EP14GEN_set5 (Red Sheep)
            351755,  # animalSheepMini_EP14GEN_set6 (Orange Sheep)
            351756,  # animalSheepMini_EP14GEN_set7 (Blue Sheep)
            351757,  # animalSheepMini_EP14GEN_set8 (Green Sheep)
            351758,  # animalSheepMini_EP14GEN_set9 (Black Sheep)
            351812,  # animalSheepMini_EP14GEN_set10 (Dalmatian Sheep)
            351852,  # animalSheepMini_EP14GEN_set11 (Mocha Sheep)
            # Goat
            328494,  # animalGoatMini_EP14GEN_set1 (White Goat)
            346691,  # animalGoatMini_EP14GEN_set2 (Gray Goat)
            346692,  # animalGoatMini_EP14GEN_set3 (Black Goat)
            346693,  # animalGoatMini_EP14GEN_set4 (Dalmatian Goat)
            346694,  # animalGoatMini_EP14GEN_set5 (Brown Goat)
            346849,  # animalGoatMini_EP14GEN_set6 (White Belt Goat)
            347200,  # animalGoatMini_EP14GEN_set7 (Chamoisee Goat)
            347201,  # animalGoatMini_EP14GEN_set8 (Spotted Goat)
            # Rabbit
            263506,  # animalRabbit_EP11GEN_set1
            276901,  # animalRabbit_EP11GEN_set2
            276902,  # animalRabbit_EP11GEN_set3
            276903,  # animalRabbit_EP11GEN_set4
            276904,  # animalRabbit_EP11GEN_set5
            276905,  # animalRabbit_EP11GEN_set6
            276906,  # animalRabbit_EP11GEN_set7
            276907,  # animalRabbit_EP11GEN_set8
            # Bird
            267595,  # animalBirdSmall_EP11GEN_set1_europeanRobin
            273844,  # animalBirdSmall_EP11GEN_set2_greatTit
            273845,  # animalBirdSmall_EP11GEN_set3_willowTit
            273846,  # animalBirdSmall_EP11GEN_set4_goldcrest
            273847,  # animalBirdSmall_EP11GEN_set5_blackcap
            273848,  # animalBirdSmall_EP11GEN_set6_greenfinch

            # Animal Housing
            270277,  # animalPen_EP11GEN_set1
            284098,  # animalPen_EP11GEN_set2
            284099,  # animalPen_EP11GEN_set3
            284100,  # animalPen_EP11GEN_set4
            284101,  # animalPen_EP11GEN_set5
            284102,  # animalPen_EP11GEN_set6
            286738,  # animalPen_EP11GEN_set7
            286739,  # animalPen_EP11GEN_set8
            286740,  # animalPen_EP11GEN_set9
            286741,  # animalPen_EP11GEN_set10
            286742,  # animalPen_EP11GEN_set11
            286743,  # animalPen_EP11GEN_set12
            286744,  # animalPen_EP11GEN_set13

            264211,  # chickenCoop_EP11GEN_set1
            281509,  # chickenCoop_EP11GEN_set2
            281510,  # chickenCoop_EP11GEN_set3
            281511,  # chickenCoop_EP11GEN_set4
            286771,  # chickenCoop_EP11GEN_set5
            286772,  # chickenCoop_EP11GEN_set6
            286773,  # chickenCoop_EP11GEN_set7
            286774,  # chickenCoop_EP11GEN_set8
            286775,  # chickenCoop_EP11GEN_set9
            286776,  # chickenCoop_EP11GEN_set10
            286777,  # chickenCoop_EP11GEN_set11
            286778,  # chickenCoop_EP11GEN_set12
            286779,  # chickenCoop_EP11GEN_set13
        )
    
    def should_register(self, game_object: GameObject) -> bool:
        super_result = super().should_register(game_object)
        if not super_result:
            return super_result
        definition_id = game_object.definition.id
        if definition_id in self.get_excluded_definition_ids():
            return False
        return super_result


# @BBInteractionRegistry.register()
class _BBSObjectFoodInteractionRegistration(BBObjectInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        return (
            BBSInteractionId.EAT_HARVESTABLE,
        )

    def should_register(self, game_object: GameObject) -> bool:
        super_result = super().should_register(game_object)
        if not super_result:
            return super_result
        included_object_definition_ids = (
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
            48368,  # gardenFruitGENApple_vfxTest
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
        definition_id = game_object.definition.id
        if definition_id not in included_object_definition_ids:
            return False
        return super_result
