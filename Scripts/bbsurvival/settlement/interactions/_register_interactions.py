"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Tuple

from bbsurvival.settlement.enums.interaction_ids import BBSSettlementInteractionId
from bluuberrylibrary.interactions.registration.bb_interaction_registry import BBInteractionRegistry
from bluuberrylibrary.interactions.registration.handlers.bb_object_interaction_handler import BBObjectInteractionHandler
from objects.game_object import GameObject


@BBInteractionRegistry.register()
class _BBSFrogLogObjectInteractionRegistration(BBObjectInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        return (
            BBSSettlementInteractionId.SETTLEMENT_GATHERER_COLLECT_FROGS,
        )

    def get_included_tuning_ids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            76115,  # collectibles_Spawners_Frogs_Log
        )
    
    def should_register(self, game_object: GameObject) -> bool:
        super_result = super().should_register(game_object)
        if not super_result:
            return super_result
        object_guid = getattr(game_object, 'guid64', -1)
        if object_guid == -1:
            return False
        return object_guid in self.get_included_tuning_ids()


@BBInteractionRegistry.register()
class _BBSDigSpotObjectInteractionRegistration(BBObjectInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        return (
            BBSSettlementInteractionId.SETTLEMENT_GATHERER_DIG,
        )

    def get_included_tuning_ids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            28690,  # collectibles_Spawners_Rock_DigSite
            116600,  # collectibles_Spawners_Rock_DigSite_ScientistLot
            216795,  # collectibles_Spawners_Rock_DigSite_Magic
        )

    def should_register(self, game_object: GameObject) -> bool:
        super_result = super().should_register(game_object)
        if not super_result:
            return super_result
        object_guid = getattr(game_object, 'guid64', -1)
        if object_guid == -1:
            return False
        return object_guid in self.get_included_tuning_ids()


@BBInteractionRegistry.register()
class _BBSDigSpotDigTreasureObjectInteractionRegistration(BBObjectInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        return (
            BBSSettlementInteractionId.SETTLEMENT_GATHERER_DIG_TREASURE,
        )

    def get_included_tuning_ids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            28690,  # collectibles_Spawners_Rock_DigSite
            116600,  # collectibles_Spawners_Rock_DigSite_ScientistLot
        )

    def should_register(self, game_object: GameObject) -> bool:
        super_result = super().should_register(game_object)
        if not super_result:
            return super_result
        object_guid = getattr(game_object, 'guid64', -1)
        if object_guid == -1:
            return False
        return object_guid in self.get_included_tuning_ids()


@BBInteractionRegistry.register()
class _BBSDigSpotDigGP06CommonObjectInteractionRegistration(BBObjectInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        return (
            BBSSettlementInteractionId.SETTLEMENT_GATHERER_DIG_GP06_COMMON,
        )

    def get_included_tuning_ids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            175607,  # collectibles_Spawners_Rock_DigSite_GP06_Common
        )

    def should_register(self, game_object: GameObject) -> bool:
        super_result = super().should_register(game_object)
        if not super_result:
            return super_result
        object_guid = getattr(game_object, 'guid64', -1)
        if object_guid == -1:
            return False
        return object_guid in self.get_included_tuning_ids()


@BBInteractionRegistry.register()
class _BBSDigSpotDigGP06RareObjectInteractionRegistration(BBObjectInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        return (
            BBSSettlementInteractionId.SETTLEMENT_GATHERER_DIG_GP06_RARE,
        )

    def get_included_tuning_ids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            175608,  # collectibles_Spawners_Rock_DigSite_GP06_Rare
        )

    def should_register(self, game_object: GameObject) -> bool:
        super_result = super().should_register(game_object)
        if not super_result:
            return super_result
        object_guid = getattr(game_object, 'guid64', -1)
        if object_guid == -1:
            return False
        return object_guid in self.get_included_tuning_ids()


@BBInteractionRegistry.register()
class _BBSDigSpotDigMagicObjectInteractionRegistration(BBObjectInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        return (
            BBSSettlementInteractionId.SETTLEMENT_GATHERER_DIG_MAGIC,
        )

    def get_included_tuning_ids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            216795,  # collectibles_Spawners_Rock_DigSite_Magic
        )

    def should_register(self, game_object: GameObject) -> bool:
        super_result = super().should_register(game_object)
        if not super_result:
            return super_result
        object_guid = getattr(game_object, 'guid64', -1)
        if object_guid == -1:
            return False
        return object_guid in self.get_included_tuning_ids()


@BBInteractionRegistry.register()
class _BBSAnimalFeederObjectInteractionRegistration(BBObjectInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        return (
            BBSSettlementInteractionId.SETTLEMENT_RANCHER_ANIMAL_FEEDER_REFILL_WITH_WILD_GRASS,
        )

    def get_included_tuning_ids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            311825,  # object_AnimalObjects_AnimalFeeder_GoatSheep_Horse
        )

    def should_register(self, game_object: GameObject) -> bool:
        super_result = super().should_register(game_object)
        if not super_result:
            return super_result
        object_guid = getattr(game_object, 'guid64', -1)
        if object_guid == -1:
            return False
        return object_guid in self.get_included_tuning_ids()


@BBInteractionRegistry.register()
class _BBSLivestockPenObjectInteractionRegistration(BBObjectInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        return (
            BBSSettlementInteractionId.SETTLEMENT_RANCHER_LIVESTOCK_PEN_INSIDE_REFILL_WITH_WILD_GRASS,
        )

    def get_included_tuning_ids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            258035,  # object_animalObjects_home_livestock_livestockPen
        )

    def should_register(self, game_object: GameObject) -> bool:
        super_result = super().should_register(game_object)
        if not super_result:
            return super_result
        object_guid = getattr(game_object, 'guid64', -1)
        if object_guid == -1:
            return False
        return object_guid in self.get_included_tuning_ids()


@BBInteractionRegistry.register()
class _BBSCoopObjectInteractionRegistration(BBObjectInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        return (
            BBSSettlementInteractionId.SETTLEMENT_RANCHER_COOP_COLLECT_EGGS,
        )

    def get_included_tuning_ids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            256701,  # object_animalObjects_home_livestock_chickenCoop
        )

    def should_register(self, game_object: GameObject) -> bool:
        super_result = super().should_register(game_object)
        if not super_result:
            return super_result
        object_guid = getattr(game_object, 'guid64', -1)
        if object_guid == -1:
            return False
        return object_guid in self.get_included_tuning_ids()


@BBInteractionRegistry.register()
class _BBSDirtMoundObjectInteractionRegistration(BBObjectInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        return (
            BBSSettlementInteractionId.SETTLEMENT_GATHERER_DIRT_MOUND_DIG_HUMAN,
        )

    def get_included_tuning_ids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            173085,  # object_DirtMound
        )

    def should_register(self, game_object: GameObject) -> bool:
        super_result = super().should_register(game_object)
        if not super_result:
            return super_result
        object_guid = getattr(game_object, 'guid64', -1)
        if object_guid == -1:
            return False
        return object_guid in self.get_included_tuning_ids()


@BBInteractionRegistry.register()
class _BBSDirtMoundMountainObjectInteractionRegistration(BBObjectInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        return (
            BBSSettlementInteractionId.SETTLEMENT_GATHERER_DIRT_MOUND_MOUNTAIN_DIG_HUMAN,
        )

    def get_included_tuning_ids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            251001,  # snowDrift_Mountain
        )

    def should_register(self, game_object: GameObject) -> bool:
        super_result = super().should_register(game_object)
        if not super_result:
            return super_result
        object_guid = getattr(game_object, 'guid64', -1)
        if object_guid == -1:
            return False
        return object_guid in self.get_included_tuning_ids()


@BBInteractionRegistry.register()
class _BBSFridgeStoveObjectInteractionRegistration(BBObjectInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            BBSSettlementInteractionId.SETTLEMENT_COOK_COOK_GROUP_MEAL_AUTONOMOUSLY,
            BBSSettlementInteractionId.SETTLEMENT_COOK_COOK_GROUP_MEAL_AUTONOMOUSLY_VEGETARIAN,
            BBSSettlementInteractionId.SETTLEMENT_COOK_COOK_GROUP_MEAL_AUTONOMOUSLY_REQUIRED_INGREDIENTS,
            BBSSettlementInteractionId.SETTLEMENT_COOK_COOK_GROUP_MEAL_AUTONOMOUSLY_VEGETARIAN_REQUIRED_INGREDIENTS,
        )

    def get_included_tuning_ids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            10191,  # object_fridgeLOW_01
            10192,  # object_fridgeHIGH_01
            14919,  # object_fridgeMED_01
            36439,  # object_fridgeModRWCulinary_01
            36440,  # object_fridgeMED_02
            36441,  # object_fridgeDS_02
            217114,  # object_fridgeGFVintage_01
            223824,  # object_fridgeLOW_Mini
            223916,  # object_fridgeMED_Mini
            115853,  # object_fridge1x1_EP01GENlab_01
            122001,  # object_fridge1x1_GP02ZEN
            270943,  # object_FridgeMED_Mini_Skincare
            121943,  # object_Fridge_SP03BRUSHED
            217118,  # object_Fridge1x1_GP05WOOD
            182432,  # fridge1x1_GP06APP
            223320,  # object_Fridge_GP08IRONold
            155531,  # object_Fridge_LowQuality_Used
            253958,  # object_fridge1x1_EP10KIT
            269450,  # object_fridge1x1_EP11IRON
            323200,  # object_Fridge_EP13CLASSIC
            134399,  # object_HomeChefStation
            135402,  # object_homeChefStation_InWall
            14972,  # object_stove_electric
            36821,  # object_stoveMinorDS_01
            36822,  # object_stoveMinorLOW_01
            36823,  # object_stoveMinorMED_01
            36824,  # object_stoveMinorHIGH_01
            77313,  # object_stoveMinorGFVintage_01
            97201,  # object_stoveRWCulGriddle_01
            239082,  # object_stove_GP08IRONold
            121948,  # object_stoveSP03BRUSHED
            258242,  # object_stove_counter_OvenCounterTop
            258243,  # object_stove_counter_OvenCounter
            258244,  # object_stove_counter_StoveCounter
            267684,  # object_stove_counter_StoveCounter_Gas
            155529,  # object_stove_LowQuality_Used
            323469,  # object_stoveMinor_EP13CLASSIC
            269477,  # object_stoveMinor_EP11IRON
            181021,  # object_stoveMinor_GP06APP
            168694,  # object_stoveMinor_GP05GENretro
        )

    def should_register(self, game_object: GameObject) -> bool:
        super_result = super().should_register(game_object)
        if not super_result:
            return super_result
        object_guid = getattr(game_object, 'guid64', -1)
        if object_guid == -1:
            return False
        return object_guid in self.get_included_tuning_ids()
