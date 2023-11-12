"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any

from bbsurvival.mod_identity import ModIdentity
from bbsurvival.settlement.enums.trait_ids import BBSSettlementTraitId
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_end_event import BBOnZoneLoadEndEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from bluuberrylibrary.utils.instances.bb_interaction_utils import BBInteractionUtils
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from event_testing.results import TestResult
from event_testing.test_base import BaseTest
from event_testing.tests import TestList
from interactions import ParticipantType
from situations.situation_manager import SituationManager


class _BBSIsNotCommunityMemberTest(BaseTest):
    def __init__(self, *_, interaction_name: str = None, **__):
        super().__init__(*_, **__)
        self._interaction_name = interaction_name

    # noinspection PyMissingOrEmptyDocstring
    def get_expected_args(self) -> Any:
        return {'subject': ParticipantType.Actor, 'target': ParticipantType.Object}

    def __call__(self, subject: Any = (), target: Any = ()) -> TestResult:
        if not subject and not target:
            return TestResult.TRUE
        sim_info = BBSimUtils.to_sim_info(next(iter(subject), None))
        if sim_info is not None:
            if BBSimTraitUtils.has_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER):
                return TestResult(False, f'BBS Blocked. {sim_info} is a Community Member.')

        if target:
            target_sim_info = BBSimUtils.to_sim_info(next(iter(target), None))
            if target_sim_info is not None:
                if BBSimTraitUtils.has_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER):
                    return TestResult(False, f'BBS Blocked. {sim_info} is a Community Member.')
        return TestResult.TRUE


class _InteractionDisabler:
    interactions_disabled = False
    LEAVE_INTERACTION_IDS = (
        # Leave
        166360,  # NPCLeaveLotInteraction: npcLeaveLot_Pet
        13002,  # SocialSuperInteraction: ask_toLeaveLot
        150258,  # SocialSuperInteraction: ask_toLeaveLot_RejectHangout
        155559,  # SocialSuperInteraction: ask_toLeaveLot_IntriguedNoise
        155560,  # SocialSuperInteraction: ask_toLeaveLot_IntriguedSmell
        130313,  # SocialSuperInteraction: ask_toLeaveLot_HiredNPC
        156214,  # SocialSuperInteraction: ask_toLeaveLot_HiredNPC_Organist
        150350,  # SocialSuperInteraction: ask_toLeaveLot_Event_NPC
        24236,  # NPCLeaveLotInteraction: npc_leave_lot_now
        24309,  # NPCLeaveLotInteraction: npc_leave_lot_now_must_run
        99554,  # NPCLeaveLotInteraction: npc_leave_lot_now_must_run_ss3_request
        124972,  # NPCLeaveLotInteraction: npc_Leave_Lot_Now_Must_Run_Klobber_Everything
        112420,  # SuperInteraction: NPCLeaveLot_Player_WaveGoodBye
        200918,  # SuperInteraction: NPCLeaveLotNow_VIPRope_Denied
        112429,  # SuperInteraction: NPCLeaveLotNow_NPC_WaveGoodBye
        112433,  # SuperInteraction: NPCLeaveLotNow_NPC_MustRun_WaveGoodBye
        176461,  # SuperInteraction: Push_Leave_Lot
        169886,  # ImmediateSuperInteraction: Push_Leave_Lot_Immediate
        169887,  # ImmediateSuperInteraction: Push_Leave_Lot_Must_Run_Immediate
        24458,  # SuperInteraction: npc_choose_to_leave_for_motive_or_homesickness
        197607,  # RabbitHoleLeaveEarlyInteraction: RabbitHoleLeaveEarlyInteraction
        # 13455,  # grimReaper_LeaveLot
        # 24400,  # grimReaper_LeaveLot_must_run
        13002,  # ask_toLeaveLot
        24458,  # npc_choose_to_leave_for_motive_or_homesickness
        # 130313,  # ask_toLeaveLot_HiredNPC
        # 140841,  # NPC_WalkBys_LeaveArea
        # 143673,  # NPCLeaveLot_NPC_Nanny_EndSituation
        # 150350,  # ask_toLeaveLot_Event_NPC
        130347,  # NPC_LeaveCafe
        129157,  # clubSuperInteraction_LeaveClubGathering
        151025,  # ask_toLeaveLot_Butler
        153134,  # vampires_MindPowers_Pusher_Command_Leave
        150153,  # vampires_MindPowers_Command_Leave
        156873,  # NightTimeVisit_Garlic_StartledLeave
        150258,  # ask_toLeaveLot_RejectHangout
        155559,  # ask_toLeaveLot_IntriguedNoise
        155560,  # ask_toLeaveLot_IntriguedSmell
        # 187070,  # scarecrow_Leave
        229882,  # UniversityMaid_LeaveLotNow
        234578,  # ask_toLeaveLot_CommunityCloseness_Complaint
        270627,  # npc_leave_lot_now_fox
        274250,  # ask_toLeaveLot_WeddingParties

        # Go Home
        210510,  # SuperInteraction: aggregateSI_goHome_clothingOptional
        13982,  # sim-gohome
        210508,  # sim-gohome-clothingOptional
        246407,  # sim-gohome_Batuu_ResistanceCamp
        245021,  # sim-gohome_Mind_Erased
        230029,  # universityWorld_GoHome
        116241,  # sI_Object_AlienPortal_GoHome
        210513,  # sI_Object_AlienPortal_GoHome_ClothingOptional
        230029,  # universityWorld_GoHome
        229423,  # universityWorld_GoHome_ClothingOptional
        140847,  # sim_GoHome_ApartmentDoor
        116234,  # aggregateSI_goHome
        223197,  # roommateNPC_GoHome
    )


@BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadEndEvent)
def _bbs_disable_leave_interactions_for_community_members_on_zone_load(event: BBOnZoneLoadEndEvent):
    if _InteractionDisabler.interactions_disabled:
        return
    _InteractionDisabler.interactions_disabled = True

    for interaction_id in _InteractionDisabler.LEAVE_INTERACTION_IDS:
        interaction = BBInteractionUtils.load_interaction_by_guid(interaction_id)
        if interaction is None:
            continue
        tests_list = list(interaction.test_globals)
        tests_list.insert(0, _BBSIsNotCommunityMemberTest())
        interaction.test_globals = TestList(tests_list)
    return TestResult.TRUE


@BBInjectionUtils.inject(ModIdentity(), SituationManager, SituationManager.can_sim_be_sent_home_in_ss3.__name__)
def _bbs_disable_leave_now_must_run(original, self, sim):
    sim_info = BBSimUtils.to_sim_info(sim)
    from bbsurvival.settlement.contexts.settlement_context_manager import BBSSettlementContextManager
    if BBSSettlementContextManager().get_settlement_context_by_sim_info(sim_info) is not None:
        return False
    return original(self, sim)


@BBInjectionUtils.inject(ModIdentity(), SituationManager, SituationManager.user_ask_sim_to_leave_now_must_run.__name__)
def _bbs_disable_leave_now_must_run(original, self, sim):
    sim_info = BBSimUtils.to_sim_info(sim)
    from bbsurvival.settlement.contexts.settlement_context_manager import BBSSettlementContextManager
    if BBSSettlementContextManager().get_settlement_context_by_sim_info(sim_info) is not None:
        return
    return original(self, sim)


@BBInjectionUtils.inject(ModIdentity(), SituationManager, SituationManager.make_sim_leave_now_must_run.__name__)
def _bbs_disable_leave_now_must_run(original, self, sim):
    sim_info = BBSimUtils.to_sim_info(sim)
    from bbsurvival.settlement.contexts.settlement_context_manager import BBSSettlementContextManager
    if BBSSettlementContextManager().get_settlement_context_by_sim_info(sim_info) is not None:
        return
    return original(self, sim)


@BBInjectionUtils.inject(ModIdentity(), SituationManager, SituationManager.make_sim_leave.__name__)
def _bbs_disable_leave_now_must_run(original, self, sim):
    sim_info = BBSimUtils.to_sim_info(sim)
    from bbsurvival.settlement.contexts.settlement_context_manager import BBSSettlementContextManager
    if BBSSettlementContextManager().get_settlement_context_by_sim_info(sim_info) is not None:
        return
    return original(self, sim)
