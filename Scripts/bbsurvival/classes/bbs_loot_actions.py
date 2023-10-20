from bbsurvival.bb_lib.utils.bb_sim_household_utils import BBSimHouseholdUtils
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
        BBSimHouseholdUtils.move_to_household_of_sim(sim_info, target_sim_info)


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
            **kwargs
        )


class BBSLootActions(LootActions):
    INSTANCE_TUNABLES = {
        'loot_actions': TunableList(
            description='\n           List of loots operations that will be awarded.\n           ',
            tunable=BBSLootActionVariant(statistic_pack_safe=True)
        ),
    }