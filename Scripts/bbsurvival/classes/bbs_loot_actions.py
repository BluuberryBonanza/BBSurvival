"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import services
from bbsurvival.bb_lib.utils.bb_sim_household_utils import BBSimHouseholdUtils
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.settlement.enums.settlement_member_job import BBSSettlementMemberJobFlags
from bbsurvival.settlement.enums.trait_ids import BBSSettlementTraitId
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from interactions import ParticipantType
from interactions.utils.loot import LootActions, LootActionVariant
from interactions.utils.loot_basic_op import BaseTargetedLootOperation
from sims4.tuning.tunable import TunableList, TunableEnumEntry

log = BBLogRegistry().register_log(ModIdentity(), 'bbs_loot_actions')
log.enable()


class BBSAssignToJobLootOp(BaseTargetedLootOperation):
    FACTORY_TUNABLES = {
        'subject': TunableEnumEntry(
            description='\n            The Sim we want to move.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.Actor
        ),
        'target': TunableEnumEntry(
            description='\n            The Sim we want to assign the job.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.TargetSim
        ),
        'settlement_job': TunableEnumEntry(
            description='\n            The job to assign.\n            ',
            tunable_type=BBSSettlementMemberJobFlags,
            default=BBSSettlementMemberJobFlags.NONE
        ),
    }

    __slots__ = {'subject', 'target', 'settlement_job'}

    def __init__(self, *_, subject=ParticipantType.Actor, target=ParticipantType.TargetSim, settlement_job=BBSSettlementMemberJobFlags.NONE, **__) -> None:
        super().__init__(*_, **__)
        self.subject = subject
        self.target = target
        self.settlement_job = settlement_job

    def _apply_to_subject_and_target(self, subject, target, resolver) -> None:
        if self._tests:
            test_result = self._tests.run_tests(resolver)
            if not test_result:
                return test_result
        target_sim = resolver.get_participant(self.target)
        target_sim_info = BBSimUtils.to_sim_info(target_sim)
        from bbsurvival.settlement.contexts.settlement_context_manager import BBSSettlementContextManager
        settlement_context = BBSSettlementContextManager().settlement_context
        if settlement_context is None:
            return
        target_context = settlement_context.get_member_context(target_sim_info)
        if target_context is None:
            return
        target_context.add_job(self.settlement_job)


class BBSUnassignFromJobLootOp(BaseTargetedLootOperation):
    FACTORY_TUNABLES = {
        'subject': TunableEnumEntry(
            description='\n            The Sim we want to move.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.Actor
        ),
        'target': TunableEnumEntry(
            description='\n            The Sim we want to assign the job.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.TargetSim
        ),
        'settlement_job': TunableEnumEntry(
            description='\n            The job to assign.\n            ',
            tunable_type=BBSSettlementMemberJobFlags,
            default=BBSSettlementMemberJobFlags.NONE
        ),
    }

    __slots__ = {'subject', 'target', 'settlement_job'}

    def __init__(self, *_, subject=ParticipantType.Actor, target=ParticipantType.TargetSim, settlement_job=BBSSettlementMemberJobFlags.NONE, **__) -> None:
        super().__init__(*_, **__)
        self.subject = subject
        self.target = target
        self.settlement_job = settlement_job

    def _apply_to_subject_and_target(self, subject, target, resolver) -> None:
        if self._tests:
            test_result = self._tests.run_tests(resolver)
            if not test_result:
                return test_result
        target_sim = resolver.get_participant(self.target)
        target_sim_info = BBSimUtils.to_sim_info(target_sim)
        from bbsurvival.settlement.contexts.settlement_context_manager import BBSSettlementContextManager
        settlement_context = BBSSettlementContextManager().settlement_context
        if settlement_context is None:
            return
        target_context = settlement_context.get_member_context(target_sim_info)
        if target_context is None:
            return
        target_context.remove_job(self.settlement_job)


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
        log.debug('Added Sim to target household', sim=sim_info, target=target_sim_info, result=result)
        trait_result = BBSimTraitUtils.add_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER)
        log.debug('added trait?', trait_result=trait_result)
        if not BBSimTraitUtils.has_trait(target_sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD):
            BBSimTraitUtils.add_trait(target_sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD)

        from bbsurvival.settlement.contexts.settlement_context_manager import BBSSettlementContextManager
        add_result = BBSSettlementContextManager().add_settlement_member_context(sim_info, head_of_settlement_sim_info=target_sim_info)
        log.debug('Add context result', add_result=add_result)


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
            assign_to_job=BBSAssignToJobLootOp.TunableFactory(
                target_participant_type_options={
                    'description': '\n                    The participant of the interaction\n                    ',
                    'default_participant': ParticipantType.Object
                }
            ),
            unassign_from_job=BBSUnassignFromJobLootOp.TunableFactory(
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