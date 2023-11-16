"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Dict

import services
from bbsurvival.bb_lib.dialog.bb_input_dialog import BBInputDialog
from bbsurvival.bb_lib.dialog.bb_ok_cancel_dialog import BBOkCancelDialog
from bbsurvival.bb_lib.dialog.fields.bb_integer_field import BBIntegerField
from bbsurvival.bb_lib.utils.bb_sim_household_utils import BBSimHouseholdUtils
from bbsurvival.bb_lib.utils.bb_sim_inventory_utils import BBSimInventoryUtils
from bbsurvival.bb_lib.utils.bb_sim_statistic_utils import BBSimStatisticUtils
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.settlement.enums.cook_time_slot import BBSSettlementCookTimeSlot
from bbsurvival.settlement.enums.settlement_member_job import BBSSettlementMemberJobFlags
from bbsurvival.settlement.enums.string_ids import BBSSettlementStringIds
from bbsurvival.settlement.enums.trait_ids import BBSSettlementTraitId
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from bluuberrylibrary.utils.text.bb_localized_tooltip_data import BBLocalizedTooltipData
from interactions import ParticipantType
from interactions.utils.loot import LootActions, LootActionVariant
from interactions.utils.loot_basic_op import BaseTargetedLootOperation
from sims4.tuning.tunable import TunableList, TunableEnumEntry

log = BBLogRegistry().register_log(ModIdentity(), 'bbs_loot_actions')
log.enable()


class BBSTransferInventoryLootOp(BaseTargetedLootOperation):
    FACTORY_TUNABLES = {
        'subject': TunableEnumEntry(
            description='\n            The Sim we want to transfer the inventory of.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.Actor
        ),
        'target': TunableEnumEntry(
            description='\n            The Sim we want to receive the inventory items.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.TargetSim
        ),
    }

    __slots__ = {'subject', 'target'}

    def __init__(self, *_, subject=ParticipantType.Actor, target=ParticipantType.TargetSim, **__) -> None:
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
        result = BBSimInventoryUtils.transfer_inventory_to_sim(sim_info, target_sim_info)
        if not result:
            log.debug('Failed to transfer inventory.', sim=sim_info, target_sim=target_sim_info, result=result)


class BBSAssignCookTimeLootOp(BaseTargetedLootOperation):
    FACTORY_TUNABLES = {
        'subject': TunableEnumEntry(
            description='\n            The Sim we want to move.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.Actor
        ),
        'target': TunableEnumEntry(
            description='\n            The Sim we want to assign the cook time.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.TargetSim
        ),
        'cook_time_slot': TunableEnumEntry(
            description='\n            The cook time slot to assign.\n            ',
            tunable_type=BBSSettlementCookTimeSlot,
            default=BBSSettlementCookTimeSlot.SLOT_ONE
        ),
    }

    __slots__ = {'subject', 'target', 'cook_time_slot'}

    def __init__(self, *_, subject=ParticipantType.Actor, target=ParticipantType.TargetSim, cook_time_slot=BBSSettlementCookTimeSlot.SLOT_ONE, **__) -> None:
        super().__init__(*_, **__)
        self.subject = subject
        self.target = target
        self.cook_time_slot = cook_time_slot

    def _apply_to_subject_and_target(self, subject, target, resolver) -> None:
        if self._tests:
            test_result = self._tests.run_tests(resolver)
            if not test_result:
                return test_result
        target_sim = resolver.get_participant(self.target)
        target_sim_info = BBSimUtils.to_sim_info(target_sim)

        hour_statistic = BBSSettlementCookTimeSlot.get_hour_statistic(self.cook_time_slot)
        if BBSimStatisticUtils.has_statistic(target_sim_info, hour_statistic):
            log.debug('Getting cook time from Sim stat, because they have it.', target_sim=target_sim_info)
            initial_hour_value = int(BBSimStatisticUtils.get_statistic_value(target_sim_info, hour_statistic))
            if initial_hour_value == -1:
                log.debug('Getting default cook hour because the stat value they had was -1', target_sim=target_sim_info)
                initial_hour_value = BBSSettlementCookTimeSlot.get_default_cook_hour(self.cook_time_slot)
        else:
            log.debug('Using default cook hour because Sim did not have statistic.', target_sim=target_sim_info)
            initial_hour_value = BBSSettlementCookTimeSlot.get_default_cook_hour(self.cook_time_slot)

        minute_statistic = BBSSettlementCookTimeSlot.get_minute_statistic(self.cook_time_slot)
        if BBSimStatisticUtils.has_statistic(target_sim_info, minute_statistic):
            log.debug('Getting cook time from Sim stat, because they have it.', target_sim=target_sim_info)
            initial_minute_value = int(BBSimStatisticUtils.get_statistic_value(target_sim_info, minute_statistic))
            if initial_minute_value == -1:
                log.debug('Getting default cook minute because the stat value they had was -1', target_sim=target_sim_info)
                initial_minute_value = BBSSettlementCookTimeSlot.get_default_cook_minute(self.cook_time_slot)
        else:
            log.debug('Using default cook minute because Sim did not have statistic.', target_sim=target_sim_info)
            initial_minute_value = BBSSettlementCookTimeSlot.get_default_cook_minute(self.cook_time_slot)

        active_sim_info = BBSimUtils.get_active_sim_info()

        def _on_submit(values: Dict[str, int]):
            new_hour_value = values['hour_field']
            new_minute_value = values['minute_field']
            from bbsurvival.settlement.contexts.settlement_context_manager import BBSSettlementContextManager
            settlement_context = BBSSettlementContextManager().get_settlement_context_by_sim_info(target_sim_info)
            if settlement_context is None:
                log.debug('No settlement context found!')
                return
            target_context = settlement_context.get_member_context(target_sim_info)
            if target_context is None:
                log.debug('No target context found!')
                return
            log.debug('Setting cook time slot.', sim=target_sim_info, new_hour_value=new_hour_value, new_minute_value=new_minute_value)
            target_context.cook_component.set_cook_time_slot(self.cook_time_slot, new_hour_value, new_minute_value)

        def _on_cancel():
            log.debug('Cancel setting cook time.')
            pass

        input_fields = (
            BBIntegerField(
                'hour_field',
                BBLocalizedStringData(BBSSettlementStringIds.HOUR),
                initial_hour_value,
                min_value=0,
                max_value=23,
                input_too_small_tooltip=BBLocalizedTooltipData(BBSSettlementStringIds.HOUR_FIELD_TOO_SMALL),
                input_too_big_tooltip=BBLocalizedTooltipData(BBSSettlementStringIds.HOUR_FIELD_TOO_BIG)
            ),
            BBIntegerField(
                'minute_field',
                BBLocalizedStringData(BBSSettlementStringIds.MINUTE),
                initial_minute_value,
                min_value=0,
                max_value=59,
                input_too_small_tooltip=BBLocalizedTooltipData(BBSSettlementStringIds.MINUTE_FIELD_TOO_SMALL),
                input_too_big_tooltip=BBLocalizedTooltipData(BBSSettlementStringIds.MINUTE_FIELD_TOO_BIG)
            ),
        )

        BBInputDialog(
            ModIdentity(),
            BBLocalizedStringData(BBSSettlementStringIds.SET_COOK_TIME),
            BBLocalizedStringData(BBSSettlementStringIds.SET_COOK_TIME_DESCRIPTION, tokens=(target_sim_info,)),
            input_fields
        ).display(active_sim_info, _on_submit, _on_cancel)


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
        settlement_context = BBSSettlementContextManager().get_settlement_context_by_sim_info(target_sim_info)
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
        settlement_context = BBSSettlementContextManager().get_settlement_context_by_sim_info(target_sim_info)
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

        def _setup_sim():
            BBSimTraitUtils.add_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER)
            if not BBSimTraitUtils.has_trait(target_sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD):
                BBSimTraitUtils.add_trait(target_sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD)

            from bbsurvival.settlement.contexts.settlement_context_manager import BBSSettlementContextManager
            add_result = BBSSettlementContextManager().add_settlement_member_context(sim_info, head_of_settlement_sim_info_override=target_sim_info)
            log.debug('Add context result', add_result=add_result)

        def _on_ok():
            result = BBSimHouseholdUtils.move_to_household_of_sim(sim_info, target_sim_info)
            log.debug('Adding Sim to settlement as Household Member', sim=sim_info, target=target_sim_info, result=result)
            _setup_sim()

        def _on_cancel():
            log.debug('Adding Sim to settlement as NPC', sim=sim_info, target=target_sim_info)
            _setup_sim()

        def _on_closed():
            pass

        BBOkCancelDialog(
            ModIdentity(),
            BBLocalizedStringData(BBSSettlementStringIds.HOW_SHALL_SIM_JOIN_GROUP, tokens=(sim_info,)),
            BBLocalizedStringData(BBSSettlementStringIds.SHOULD_SIM_JOIN_AS_CONTROLLED_OR_NON_CONTROLLED, tokens=(sim_info,)),
            ok_text=BBLocalizedStringData(BBSSettlementStringIds.JOIN_AS_CONTROLLED),
            cancel_text=BBLocalizedStringData(BBSSettlementStringIds.JOIN_AS_NON_CONTROLLED)
        ).display(sim_info, _on_ok, _on_cancel, on_closed=_on_closed)


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
            assign_cook_time=BBSAssignCookTimeLootOp.TunableFactory(
                target_participant_type_options={
                    'description': '\n                    The participant of the interaction\n                    ',
                    'default_participant': ParticipantType.Object
                }
            ),
            transfer_inventory=BBSTransferInventoryLootOp.TunableFactory(
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