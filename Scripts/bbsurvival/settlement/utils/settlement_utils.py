"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Tuple, Any

import services
from bbsurvival.bb_lib.dialog.bb_button_dialog import BBButtonDialog
from bbsurvival.bb_lib.dialog.fields.bb_button import BBButton
from bbsurvival.bb_lib.utils.bb_sim_age_utils import BBSimAgeUtils
from bbsurvival.bb_lib.utils.bb_sim_household_utils import BBSimHouseholdUtils
from bbsurvival.bb_lib.utils.bb_sim_relationship_utils import BBSimRelationshipUtils
from bbsurvival.bb_lib.utils.bb_sim_species_utils import BBSimSpeciesUtils
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.settlement.contexts.settlement_context import BBSSettlementContext
from bbsurvival.settlement.contexts.settlement_context_manager import BBSSettlementContextManager
from bbsurvival.settlement.enums.relationship_bit_ids import BBSSettlementRelationshipBitId
from bbsurvival.settlement.enums.settlement_member_job import BBSSettlementMemberJobFlags
from bbsurvival.settlement.enums.trait_ids import BBSSettlementTraitId
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.classes.bb_test_result import BBTestResult
from bluuberrylibrary.dialogs.notifications.bb_notification import BBNotification
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from sims.sim_info import SimInfo

log = BBLogRegistry().register_log(ModIdentity(), 'bbs_settlement_utils')
# log.enable()


class BBSSettlementUtils:
    """Utilities for managing the settlement."""
    @classmethod
    def is_head_of_settlement(cls, sim_info: SimInfo) -> bool:
        return BBSimTraitUtils.has_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD)

    @classmethod
    def is_settlement_member(cls, sim_info: SimInfo) -> bool:
        return BBSimTraitUtils.has_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER)

    @classmethod
    def is_member_of_active_settlement(cls, sim_info: SimInfo) -> bool:
        settlement_context = BBSSettlementContextManager().get_settlement_context_by_sim_info(sim_info)
        if settlement_context is None:
            return False
        active_sim_info = BBSimUtils.get_active_sim_info()
        active_sim_household = BBSimHouseholdUtils.get_household(active_sim_info)
        return active_sim_household.home_zone_id == settlement_context.home_zone_id

    @classmethod
    def add_head_of_settlement_relationship(cls, head_of_settlement_sim_info: SimInfo, settlement_member_sim_info: SimInfo):
        return BBSimRelationshipUtils.add_relationship_bit(
            head_of_settlement_sim_info,
            settlement_member_sim_info,
            BBSSettlementRelationshipBitId.HEAD_OF_SETTLEMENT_TO_SETTLEMENT_MEMBER
        )

    @classmethod
    def remove_head_of_settlement_relationship(cls, head_of_settlement_sim_info: SimInfo, settlement_member_sim_info: SimInfo):
        return BBSimRelationshipUtils.remove_relationship_bit(
            head_of_settlement_sim_info,
            settlement_member_sim_info,
            BBSSettlementRelationshipBitId.HEAD_OF_SETTLEMENT_TO_SETTLEMENT_MEMBER
        )

    @classmethod
    def has_head_of_settlement_relationship(cls, head_of_settlement_sim_info: SimInfo, settlement_member_sim_info: SimInfo) -> bool:
        return BBSimRelationshipUtils.has_relationship_bit(
            head_of_settlement_sim_info,
            settlement_member_sim_info,
            BBSSettlementRelationshipBitId.HEAD_OF_SETTLEMENT_TO_SETTLEMENT_MEMBER
        )

    @classmethod
    def is_in_same_settlement(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> BBTestResult:
        settlement_context_a = BBSSettlementContextManager().get_settlement_context_by_sim_info(sim_info_a)
        if settlement_context_a is None:
            return BBTestResult(False, f'{sim_info_a} is not a part of a Settlement.')
        settlement_context_b = BBSSettlementContextManager().get_settlement_context_by_sim_info(sim_info_b)
        if settlement_context_b is None:
            return BBTestResult(False, f'{sim_info_b} is not a part of a Settlement.')
        if settlement_context_a is not settlement_context_b:
            return BBTestResult(False, f'{sim_info_a} is not in the same settlement as {sim_info_b}')
        return BBTestResult.TRUE

    @classmethod
    def retire_head_of_settlement(cls, old_head_of_settlement_sim_info: SimInfo) -> BBRunResult:
        log.debug('Retiring Head of Settlement.', sim=old_head_of_settlement_sim_info)
        settlement_context = BBSSettlementContextManager().get_settlement_context_by_sim_info(old_head_of_settlement_sim_info)
        if settlement_context is not None:
            old_head_of_settlement_context = settlement_context.get_head_of_settlement_context()
            old_head_of_settlement_context.is_head_of_settlement = False
            BBSimTraitUtils.remove_trait(old_head_of_settlement_sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD)
            for member_context in settlement_context.member_contexts:
                if member_context is old_head_of_settlement_context:
                    continue
                cls.remove_head_of_settlement_relationship(old_head_of_settlement_sim_info, member_context.sim_info)

            settlement_context.remove_member_context(old_head_of_settlement_context)
            cls.elect_new_head_of_settlement(settlement_context)
        else:
            BBSimTraitUtils.remove_trait(old_head_of_settlement_sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD)
            for sim_info in BBSimUtils.get_all_sim_info_gen():
                cls.remove_head_of_settlement_relationship(old_head_of_settlement_sim_info, sim_info)
        return BBRunResult.TRUE

    @classmethod
    def retire_settlement_member(cls, settlement_member_sim_info: SimInfo) -> BBRunResult:
        log.debug('Retiring settlement member.', sim=settlement_member_sim_info)
        if BBSimTraitUtils.has_trait(settlement_member_sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD):
            return cls.retire_head_of_settlement(settlement_member_sim_info)

        settlement_context = BBSSettlementContextManager().get_settlement_context_by_sim_info(settlement_member_sim_info)
        if settlement_context is not None:
            head_of_settlement_context = settlement_context.get_head_of_settlement_context()
            settlement_member_context = settlement_context.get_member_context(settlement_member_sim_info)
            BBSimTraitUtils.remove_trait(settlement_member_sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER)
            cls.remove_head_of_settlement_relationship(head_of_settlement_context.sim_info, settlement_member_sim_info)
            settlement_context.remove_member_context(settlement_member_context)
        else:
            BBSimTraitUtils.remove_trait(settlement_member_sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER)
            for sim_info in BBSimUtils.get_all_sim_info_gen():
                cls.remove_head_of_settlement_relationship(sim_info, settlement_member_sim_info)
        return BBRunResult.TRUE

    @classmethod
    def elect_new_head_of_settlement(cls, settlement_context: BBSSettlementContext) -> BBRunResult:
        log.debug('Electing a new head of settlement.')
        head_of_settlement_context = settlement_context.get_head_of_settlement_context()
        if head_of_settlement_context is not None:
            return BBRunResult(False, f'Settlement already has a Head of settlement {head_of_settlement_context.sim_info}')
        new_head_of_settlement_context = None
        for member_context in settlement_context.member_contexts:
            if not cls.is_allowed_as_head_of_settlement(member_context.sim_info):
                continue
            new_head_of_settlement_context = member_context
            break

        return cls.change_to_head_of_settlement(new_head_of_settlement_context.sim_info)

    @classmethod
    def change_to_head_of_settlement(cls, new_head_of_settlement_sim_info: SimInfo) -> BBRunResult:
        log.debug('Changing head of settlement to Sim.', new_head_of_settlement_sim_info=new_head_of_settlement_sim_info)
        settlement_context = BBSSettlementContextManager().get_settlement_context_by_sim_info(new_head_of_settlement_sim_info)
        if settlement_context is None:
            return BBRunResult(False, f'{new_head_of_settlement_sim_info} is not a part of any Settlement and thus cannot become a head of a settlement.')

        old_head_of_settlement_context = settlement_context.get_head_of_settlement_context()
        if old_head_of_settlement_context is not None:
            old_head_of_settlement_sim_info = old_head_of_settlement_context.sim_info
            if old_head_of_settlement_sim_info is new_head_of_settlement_sim_info:
                return BBRunResult(True, f'{new_head_of_settlement_sim_info} is already the head of a Settlement.')
            BBSimTraitUtils.remove_trait(old_head_of_settlement_sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD)
            BBSimTraitUtils.add_trait(old_head_of_settlement_sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER)
            old_head_of_settlement_context.is_head_of_settlement = False
            for _member_context in settlement_context.member_contexts:
                if _member_context is old_head_of_settlement_context:
                    continue
                cls.remove_head_of_settlement_relationship(old_head_of_settlement_sim_info, _member_context.sim_info)

        new_head_of_settlement_context = settlement_context.get_member_context(new_head_of_settlement_sim_info)
        BBSimTraitUtils.remove_trait(new_head_of_settlement_sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER)
        BBSimTraitUtils.add_trait(new_head_of_settlement_sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD)
        new_head_of_settlement_context.is_head_of_settlement = True
        for member_context in settlement_context.member_contexts:
            if member_context.sim_info is new_head_of_settlement_sim_info:
                continue
            cls.add_head_of_settlement_relationship(
                new_head_of_settlement_sim_info,
                member_context.sim_info
            )
        new_head_of_settlement_context.teardown()
        new_head_of_settlement_context.setup()
        return BBRunResult.TRUE

    @classmethod
    def is_allowed_as_head_of_settlement(cls, sim_info: SimInfo) -> BBTestResult:
        if not BBSimSpeciesUtils.is_human(sim_info):
            return BBTestResult(False, f'{sim_info} is not allowed as Head of Settlement because they are not Human.')
        if BBSimAgeUtils.is_baby(sim_info)\
                or BBSimAgeUtils.is_infant(sim_info)\
                or BBSimAgeUtils.is_toddler(sim_info)\
                or BBSimAgeUtils.is_child(sim_info):
            return BBTestResult(False, f'{sim_info} is too young to be a Head of Settlement.')
        current_zone_id = services.current_zone_id()
        sim_household = BBSimHouseholdUtils.get_household(sim_info)
        home_zone_id = sim_household.home_zone_id
        if current_zone_id != home_zone_id:
            return BBTestResult(False, f'{sim_info} is not the owner of the current lot. Thus they cannot be Head of Settlement.')
        # This is to fix npcs that are not living on the home lot.
        for _sim_info in BBSimUtils.get_all_sim_info_gen():
            if BBSSettlementUtils.has_head_of_settlement_relationship(_sim_info, sim_info):
                other_sim_household = BBSimHouseholdUtils.get_household(_sim_info)
                if current_zone_id != other_sim_household.home_zone_id:
                    return BBTestResult(False, f'{sim_info} is already part of another Settlement.')
        return BBTestResult.TRUE

    @classmethod
    def get_allowed_jobs(cls, sim_info: SimInfo) -> Tuple[BBSSettlementMemberJobFlags]:
        if BBSimSpeciesUtils.is_human(sim_info):
            if BBSimAgeUtils.is_child(sim_info):
                # noinspection PyTypeChecker
                return (
                    BBSSettlementMemberJobFlags.GARDENER,
                    BBSSettlementMemberJobFlags.SANITATION,
                    BBSSettlementMemberJobFlags.MAINTENANCE,
                    BBSSettlementMemberJobFlags.RANCHER
                )
            elif BBSimAgeUtils.is_teen(sim_info)\
                    or BBSimAgeUtils.is_young_adult(sim_info)\
                    or BBSimAgeUtils.is_adult(sim_info)\
                    or BBSimAgeUtils.is_elder(sim_info):
                # noinspection PyTypeChecker
                return (
                    BBSSettlementMemberJobFlags.COOK,
                    BBSSettlementMemberJobFlags.NANNY,
                    BBSSettlementMemberJobFlags.GARDENER,
                    BBSSettlementMemberJobFlags.GUARD,
                    BBSSettlementMemberJobFlags.DOCTOR,
                    BBSSettlementMemberJobFlags.SCOUT,
                    BBSSettlementMemberJobFlags.SANITATION,
                    BBSSettlementMemberJobFlags.MAINTENANCE,
                    BBSSettlementMemberJobFlags.TEACHER,
                    BBSSettlementMemberJobFlags.GATHERER,
                    BBSSettlementMemberJobFlags.RANCHER,
                )
        elif not BBSimSpeciesUtils.is_horse(sim_info):
            # noinspection PyTypeChecker
            return (
                BBSSettlementMemberJobFlags.GUARD,
                BBSSettlementMemberJobFlags.SCOUT
            )
        return tuple()

    @classmethod
    def remove_all_settlement_related_things(cls):
        sim_info_list_one = tuple(BBSimUtils.get_all_sim_info_gen())
        for sim_info in sim_info_list_one:
            for sim_info_b in sim_info_list_one:
                if sim_info is sim_info_b:
                    continue
                cls.remove_head_of_settlement_relationship(sim_info, sim_info_b)
                cls.remove_head_of_settlement_relationship(sim_info_b, sim_info)
            BBSimTraitUtils.remove_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD)
            BBSimTraitUtils.remove_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER)
            BBSimTraitUtils.remove_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_SCOUT)
            BBSimTraitUtils.remove_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_SANITATION)
            BBSimTraitUtils.remove_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_MAINTENANCE)
            BBSimTraitUtils.remove_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_COOK)
            BBSimTraitUtils.remove_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_NANNY)
            BBSimTraitUtils.remove_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_GARDENER)
            BBSimTraitUtils.remove_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_GUARD)
            BBSimTraitUtils.remove_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_DOCTOR)
            BBSimTraitUtils.remove_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_TEACHER)
            BBSimTraitUtils.remove_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_GATHERER)
            BBSimTraitUtils.remove_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_RANCHER)

    @classmethod
    def open_survival_manual(cls, sim_info: SimInfo):

        def _on_choose_read_the_basics(_: Any):
            BBNotification(
                ModIdentity(),
                BBLocalizedStringData('The Basics'),
                BBLocalizedStringData('The basics to surviving are to ensure you have enough food, enough power, and enough water. Buy a Generator or Solar Panels for power and a Dew Collector for water. Go scavenging for Food.')
            ).show()

        buttons = (
            BBButton(
                1,
                BBLocalizedStringData('Read The Basics'),
                _on_choose_read_the_basics,
                value='Basics',
                subtext=BBLocalizedStringData('Learn the basics of surviving.'),
                tooltip_text=BBLocalizedStringData('Learn the basics of surviving.')
            ),
        )

        def _on_closed():
            pass

        BBButtonDialog(
            ModIdentity(),
            BBLocalizedStringData(f'What will {sim_info} read?'),
            BBLocalizedStringData('Choose a topic.'),
            buttons
        ).display(sim_info, on_closed=_on_closed)
