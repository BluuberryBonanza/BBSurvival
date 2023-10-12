"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_end_event import BBOnZoneLoadEndEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from bluuberrylibrary.utils.instances.bb_interaction_utils import BBInteractionUtils
from event_testing.results import TestResult
from event_testing.tests import TestList
from interactions import ParticipantType
from nomorequickmeals.mod_identity import ModIdentity
from sims.sim_info_tests import SimInfoTest, MatchType
interactions_disabled = False


@BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadEndEvent)
def _nms_disable_interactions_on_zone_load(event: BBOnZoneLoadEndEvent):
    global interactions_disabled
    if interactions_disabled:
        return
    interactions_disabled = True

    interaction_ids = (
        # Grab a Quick Meal
        13396,  # fridge_GrabSnack
        13397,  # fridge_GrabSnackAutonomously
        266693,  # fridge_GrabSnackAutonomously_LactoseIntolerant
        181585,  # fridge_GrabCookiesAutonomously
        145873,  # fridge_Butler_CookGourmetPartyMeal
        145872,  # fridge_Butler_CookPartyMeal
        145871,  # fridge_Butler_CookGourmetFamilyMeal
        145851,  # fridge_Butler_MakeSnack
        126096,  # fridge_Cook_SpookyPartyFood_Autonomously
        350833,  # lunchbox_GrabSnackAutonomously
        350013,  # lunchbox_Craft_HaveQuickMeal
        103037,  # cooler_GrabSnackAutonomously
        102276,  # cooler_Craft_HaveQuickMeal
        77672,  # fridge_GrabSnack_PieMenu
        13601,  # microwave_StartCrafting
        217063,  # fridge_GrabSnack_Microwave_PieMenu
        164448,  # fridge_GrabSackLunch
        270682,  # fridge_GrabSackLunch_RequiredIngredients
    )

    for interaction_id in interaction_ids:
        impossible_sim_info_test = SimInfoTest()
        impossible_sim_info_test.who = ParticipantType.Actor
        impossible_sim_info_test.gender = None
        impossible_sim_info_test.ages = (0,)
        impossible_sim_info_test.species = None
        impossible_sim_info_test.can_age_up = None
        impossible_sim_info_test.npc = False
        impossible_sim_info_test.has_been_played = False
        impossible_sim_info_test.is_active_sim = True
        impossible_sim_info_test.match_type = MatchType.MATCH_ALL
        interaction = BBInteractionUtils.load_interaction_by_guid(interaction_id)
        interaction.test_globals = TestList((impossible_sim_info_test,))
    return TestResult.TRUE
