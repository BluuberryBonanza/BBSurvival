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
