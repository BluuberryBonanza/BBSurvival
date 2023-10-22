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
from bluuberrylibrary.interactions.registration.handlers.bb_sim_interaction_handler import BBSimInteractionHandler
from objects.game_object import GameObject


@BBInteractionRegistry.register()
class _BBSSimInteractionRegistration(BBSimInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        return (
            BBSInteractionId.SCAVENGE_QUICK,
        )


@BBInteractionRegistry.register()
class _BBSObjectInteractionRegistration(BBObjectInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        return (
            BBSInteractionId.LIGHT_ON_FIRE,
        )
    
    def should_register(self, game_object: GameObject) -> bool:
        super_result = super().should_register(game_object)
        if not super_result:
            return super_result
        excluded_animal_definition_ids = (
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
        )
        definition_id = game_object.definition.id
        if definition_id in excluded_animal_definition_ids:
            return False
        return super_result
