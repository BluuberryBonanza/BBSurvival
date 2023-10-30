import services
from bbsurvival.bb_lib.utils.bb_sim_household_utils import BBSimHouseholdUtils
from bbsurvival.settlement.enums.trait_ids import BBSSettlementTraitId
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from interactions import ParticipantType
from interactions.utils.loot import LootActions, LootActionVariant
from interactions.utils.loot_basic_op import BaseTargetedLootOperation
from sims4.tuning.tunable import TunableList, TunableEnumEntry


class BBSAddToSettlementLootOp(BaseTargetedLootOperation):
    FACTORY_TUNABLES = {
        'subject': TunableEnumEntry(
            description='\n            The Sim we want to move.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.TargetSim
        ),
        'target': TunableEnumEntry(
            description='\n            The Sim we want to have a new household member.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.Actor
        ),
    }

    __slots__ = {'subject', 'target'}

    def __init__(self, *_, subject=ParticipantType.TargetSim, target=ParticipantType.Actor, **__) -> None:
        super().__init__(*_, **__)
        self.subject = subject
        self.target = target

    def _apply_to_subject_and_target(self, subject, target, resolver) -> None:
        if self._tests:
            test_result = self._tests.run_tests(resolver)
            if not test_result:
                return test_result
        sim_info = BBSimUtils.to_sim_info(subject)
        target_sim = resolver.get_participant(self.target)
        target_sim_info = BBSimUtils.to_sim_info(target_sim)
        result = BBSimHouseholdUtils.move_to_household_of_sim(sim_info, target_sim_info)
        BBSimTraitUtils.add_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER)
        if not BBSimTraitUtils.has_trait(target_sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD):
            BBSimTraitUtils.add_trait(target_sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD)
            from bbsurvival.settlement.settlement_context_manager import BBSSettlementContextManager
            BBSSettlementContextManager().setup_settlement_context(target_sim_info)


class BBSLightOnFireLootOp(BaseTargetedLootOperation):
    FACTORY_TUNABLES = {
        'subject': TunableEnumEntry(
            description='\n            The thing we want to set on fire.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.Object
        ),
    }

    __slots__ = {'subject'}

    def __init__(self, *_, subject=ParticipantType.Object, **__) -> None:
        super().__init__(*_, **__)
        self.subject = subject

    def _apply_to_subject_and_target(self, subject, target, resolver) -> None:
        if self._tests:
            test_result = self._tests.run_tests(resolver)
            if not test_result:
                return test_result

        fire_service = services.get_fire_service()
        if fire_service is None:
            return
        fire_service.spawn_fire_at_object(subject)


class BBSLootActionVariant(LootActionVariant):
    def __init__(self, *args, statistic_pack_safe=False, **kwargs) -> None:
        super().__init__(
            *args,
            statistic_pack_safe=statistic_pack_safe,
            add_to_settlement=BBSAddToSettlementLootOp.TunableFactory(
                target_participant_type_options={
                    'description': '\n                    The participant of the interaction\n                    ',
                    'default_participant': ParticipantType.Object
                }
            ),
            light_on_fire=BBSLightOnFireLootOp.TunableFactory(
                target_participant_type_options={
                    'description': '\n                    The participant of the interaction\n                    ',
                    'default_participant': ParticipantType.Object
                }
            ),
            **kwargs
        )


class BBSLootActions(LootActions):
    INSTANCE_TUNABLES = {
        'loot_actions': TunableList(
            description='\n           List of loots operations that will be awarded.\n           ',
            tunable=BBSLootActionVariant(statistic_pack_safe=True)
        ),
    }