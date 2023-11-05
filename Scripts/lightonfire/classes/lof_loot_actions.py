"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import services
from interactions import ParticipantType
from interactions.utils.loot import LootActions, LootActionVariant
from interactions.utils.loot_basic_op import BaseTargetedLootOperation
from sims4.tuning.tunable import TunableList, TunableEnumEntry


class LOFLightOnFireLootOp(BaseTargetedLootOperation):
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


class LOFLootActionVariant(LootActionVariant):
    def __init__(self, *args, statistic_pack_safe=False, **kwargs) -> None:
        super().__init__(
            *args,
            statistic_pack_safe=statistic_pack_safe,
            light_on_fire=LOFLightOnFireLootOp.TunableFactory(
                target_participant_type_options={
                    'description': '\n                    The participant of the interaction\n                    ',
                    'default_participant': ParticipantType.Object
                }
            ),
            **kwargs
        )


class LOFLootActions(LootActions):
    INSTANCE_TUNABLES = {
        'loot_actions': TunableList(
            description='\n           List of loots operations that will be awarded.\n           ',
            tunable=LOFLootActionVariant(statistic_pack_safe=True)
        ),
    }