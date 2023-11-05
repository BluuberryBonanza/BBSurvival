"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any

from bbsurvival.bb_lib.utils.bb_instance_utils import BBInstanceUtils
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.settlement.enums.trait_ids import BBSSettlementTraitId
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_end_event import BBOnZoneLoadEndEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.instances.bb_interaction_utils import BBInteractionUtils
from bluuberrylibrary.utils.instances.bb_trait_utils import BBTraitUtils
from event_testing.results import TestResult
from event_testing.test_base import BaseTest
from event_testing.tests import TestList
from interactions import ParticipantType
from objects.part import ObjectPart
from sims.sim_info_tests import TraitTest
from sims4.resources import Types
from statistics.statistic import Statistic

log = BBLogRegistry().register_log(ModIdentity(), 'bbs_change_rancher_interactions')
log.enable()


class _BBSIsAnimalObjectHungryTest(BaseTest):
    def __init__(self, *_, interaction_name: str = None, **__):
        super().__init__(*_, **__)
        self._interaction_name = interaction_name

    # noinspection PyMissingOrEmptyDocstring
    def get_expected_args(self) -> Any:
        return {'subject': ParticipantType.Actor, 'target': ParticipantType.Object}

    def __call__(self, subject: Any = (), target: Any = ()) -> TestResult:
        if not target:
            # log.debug('Not checking hungry.')
            return TestResult.TRUE

        game_object = next(iter(target), None)
        stat_id = 256986  # commodity_AnimalObjects_Motive_Hunger
        statistic = BBInstanceUtils.get_instance(Types.STATISTIC, stat_id, return_type=Statistic)
        statistic_tracker = game_object.get_tracker(statistic)
        if statistic_tracker is None:
            return TestResult.TRUE
        stat_value = statistic_tracker.get_value(statistic)
        # log.debug('Got hungry value', stat_value=stat_value)
        if stat_value <= 150:
            return TestResult.TRUE
        return TestResult(False, 'Not hungry enough.')


class _BBSIsAnimalObjectDirtyTest(BaseTest):
    def __init__(self, *_, interaction_name: str = None, **__):
        super().__init__(*_, **__)
        self._interaction_name = interaction_name

    # noinspection PyMissingOrEmptyDocstring
    def get_expected_args(self) -> Any:
        return {'subject': ParticipantType.Actor, 'target': ParticipantType.Object}

    def __call__(self, subject: Any = (), target: Any = ()) -> TestResult:
        if not target:
            # log.debug('Not checking hygiene.')
            return TestResult.TRUE
        game_object = next(iter(target), None)
        stat_id = 256988  # commodity_AnimalObjects_Motive_Hygiene
        statistic = BBInstanceUtils.get_instance(Types.STATISTIC, stat_id, return_type=Statistic)
        statistic_tracker = game_object.get_tracker(statistic)
        if statistic_tracker is None:
            return TestResult.TRUE
        stat_value = statistic_tracker.get_value(statistic)

        # log.debug('Got hygiene value', stat_value=stat_value)
        if stat_value <= 150:
            return TestResult.TRUE
        return TestResult(False, 'Not dirty enough.')


class _BBSIsAnimalObjectLonelyTest(BaseTest):
    def __init__(self, *_, interaction_name: str = None, **__):
        super().__init__(*_, **__)
        self._interaction_name = interaction_name

    # noinspection PyMissingOrEmptyDocstring
    def get_expected_args(self) -> Any:
        return {'subject': ParticipantType.Actor, 'target': ParticipantType.Object}

    def __call__(self, subject: Any = (), target: Any = ()) -> TestResult:
        if not target:
            # log.debug('Not checking lonely.')
            return TestResult.TRUE

        game_object = next(iter(target), None)
        stat_id = 256987  # commodity_AnimalObjects_Motive_Activity
        statistic = BBInstanceUtils.get_instance(Types.STATISTIC, stat_id, return_type=Statistic)
        statistic_tracker = game_object.get_tracker(statistic)
        if statistic_tracker is None:
            return TestResult.TRUE
        stat_value = statistic_tracker.get_value(statistic)

        # log.debug('Got lonely value', stat_value=stat_value)
        if stat_value <= 150:
            return TestResult.TRUE
        return TestResult(False, 'Not lonely enough.')


class _InteractionDisabler:
    interactions_disabled = False
    FEED_INTERACTION_IDS = (
        260972,  # sI_AnimalObjects_FeedBasic_Chickens
        269785,  # sI_AnimalObjects_FeedBasic_LivestockPen
        300309,  # sI_AnimalObjects_FeedBasic_Goat
        325932,  # sI_AnimalObjects_FeedBasic_Goat_Milk
        312145,  # sI_AnimalObjects_FeedBasic_LivestockPen_WildGrassHay
        300310,  # sI_AnimalObjects_FeedBasic_Sheep
        325933,  # sI_AnimalObjects_FeedBasic_Sheep_Milk
    )

    CLEAN_INTERACTION_IDS = (
        262294,  # sI_AnimalObjects_Clean_Llama
        262293,  # sI_AnimalObjects_Clean_Cow
        337567,  # sI_AnimalObjects_Clean_Goat_All_Start
        300317,  # sI_AnimalObjects_Clean_Sheep
        337566,  # sI_AnimalObjects_Clean_Sheep_All_Start
        337565,  # sI_AnimalObjects_Clean_Goat_All
        336604,  # sI_AnimalObjects_Clean_Sheep_All
        300318,  # sI_AnimalObjects_Clean_Goat
    )

    SOCIAL_INTERACTION_IDS = (
        262992,  # sI_AnimalObjects_Pet_LivestockPen_Cow
        262993,  # sI_AnimalObjects_Pet_LivestockPen_Llama
        261790,  # sI_AnimalObjects_Hug_LivestockPen_Start_Cow
        261791,  # sI_AnimalObjects_Hug_LivestockPen_Start_Llama
        261272,  # sI_AnimalObjects_Pet_Chicken
        261275,  # sI_AnimalObjects_Hug_Chicken
        257950,  # sI_AnimalObjects_Socials_Friendly_Chicken_TalkTo
        260886,  # sI_AnimalObjects_Socials_Friendly_Chicken_TalkTo_Child
        260914,  # sI_AnimalObjects_Socials_Friendly_Chicken_TalkTo_Toddler
        258087,  # sI_AnimalObjects_Socials_Friendly_Chicken_Ask
        257954,  # sI_AnimalObjects_Socials_Funny_Chicken_TellJoke
        256882,  # sI_AnimalObjects_Socials_Mean_Chicken
        261275,  # sI_AnimalObjects_Hug_Chicken
        261272,  # sI_AnimalObjects_Pet_Chicken
        260688,  # sI_AnimalObjects_Socials_Friendly_Chicken_Play
        260689,  # sI_AnimalObjects_Socials_Mean_Chicken_Scare
        262005,  # sI_AnimalObjects_Socials_Friendly_LivestockPen_TalkTo_Cow
        262006,  # sI_AnimalObjects_Socials_Friendly_LivestockPen_TalkTo_Llama
        262003,  # sI_AnimalObjects_Socials_Friendly_LivestockPen_TalkTo_Child_Cow
        262001,  # sI_AnimalObjects_Socials_Friendly_LivestockPen_TalkTo_Toddler_Cow
        261971,  # sI_AnimalObjects_Socials_Funny_LivestockPen_TellJoke_Cow
    )


@BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadEndEvent)
def _bbs_disable_leave_interactions_for_community_members_on_zone_load(event: BBOnZoneLoadEndEvent):
    if _InteractionDisabler.interactions_disabled:
        return
    _InteractionDisabler.interactions_disabled = True

    for interaction_id in _InteractionDisabler.FEED_INTERACTION_IDS:
        interaction = BBInteractionUtils.load_interaction_by_guid(interaction_id)
        if interaction is None:
            continue
        tests_list = list(interaction.test_globals)
        tests_list.insert(0, _BBSIsAnimalObjectHungryTest())
        interaction.test_globals = TestList(tests_list)

    for interaction_id in _InteractionDisabler.CLEAN_INTERACTION_IDS:
        interaction = BBInteractionUtils.load_interaction_by_guid(interaction_id)
        if interaction is None:
            continue
        tests_list = list(interaction.test_globals)
        tests_list.insert(0, _BBSIsAnimalObjectDirtyTest())
        interaction.test_globals = TestList(tests_list)

    for interaction_id in _InteractionDisabler.SOCIAL_INTERACTION_IDS:
        interaction = BBInteractionUtils.load_interaction_by_guid(interaction_id)
        if interaction is None:
            continue
        tests_list = list(interaction.test_globals)
        tests_list.insert(0, _BBSIsAnimalObjectLonelyTest())
        interaction.test_globals = TestList(tests_list)

    clean_interaction = BBInteractionUtils.load_interaction_by_guid(260379)  # empty_Trash_AnimalObject_Home_Coop
    if clean_interaction is not None:
        test_autonomous = clean_interaction.test_autonomous
        # log.debug('test autonomous', test_autonomous=test_autonomous)
        for auto_test in test_autonomous:
            # log.debug('auto test', auto_test=auto_test)
            for a_test in auto_test:
                if isinstance(a_test, TraitTest):
                    rancher_trait = BBTraitUtils.load_trait_by_guid(BBSSettlementTraitId.SETTLEMENT_RANCHER)
                    if a_test.whitelist_traits:
                        a_test.whitelist_traits = (*a_test.whitelist_traits, rancher_trait)
                    # log.debug('a test', a_test=a_test)

    chicken_coop_object_part = BBInstanceUtils.get_instance(Types.OBJECT_PART, 270077, return_type=ObjectPart)  # objectPart_AnimalObject_AnimalHomes_SimNest
    if chicken_coop_object_part is not None:
        # log.debug('Chicken coop part', chicken_coop_object_part=chicken_coop_object_part, affordance_data=chicken_coop_object_part.supported_affordance_data)
        compatibility = chicken_coop_object_part.supported_affordance_data.compatibility
        # log.debug('Compability', compatibility=compatibility, compatibility_dir=dir(compatibility))
    return TestResult.TRUE
