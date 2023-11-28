"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any

from bbsurvival.enums.object_definition_ids import BBSObjectDefinitionId
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_end_event import BBOnZoneLoadEndEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.instances.bb_interaction_utils import BBInteractionUtils
from event_testing.results import TestResult
from event_testing.test_base import BaseTest
from event_testing.tests import TestList
from interactions import ParticipantType
from interactions.context import InteractionContext

log = BBLogRegistry().register_log(ModIdentity(), 'bbs_disable_read')


class _BBSIsNotReadingAutonomouslyTest(BaseTest):
    def __init__(self, *_, interaction_name: str = None, **__):
        super().__init__(*_, **__)
        self._interaction_name = interaction_name

    # noinspection PyMissingOrEmptyDocstring
    def get_expected_args(self) -> Any:
        return {'interaction_context': ParticipantType.InteractionContext, 'target': ParticipantType.Object}

    def __call__(self, interaction_context: Any = None, target: Any = ()) -> TestResult:
        if not interaction_context and not target:
            return TestResult.TRUE

        target_obj = next(iter(target), None)

        definition_id = target_obj.definition.id
        if definition_id != BBSObjectDefinitionId.SURVIVAL_MANUAL:
            return TestResult.TRUE

        if interaction_context.source == InteractionContext.SOURCE_AUTONOMY:
            return TestResult.NONE
        return TestResult.TRUE


class _InteractionDisabler:
    interactions_disabled = False
    INTERACTION_IDS = (
        13117,  # book_read
    )


@BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadEndEvent)
def _bbs_disable_autonomous_read_survival_manual_on_zone_load(event: BBOnZoneLoadEndEvent) -> BBRunResult:
    if _InteractionDisabler.interactions_disabled:
        return BBRunResult.TRUE
    _InteractionDisabler.interactions_disabled = True

    for interaction_id in _InteractionDisabler.INTERACTION_IDS:
        interaction = BBInteractionUtils.load_interaction_by_guid(interaction_id)
        if interaction is None:
            continue
        tests_list = list(interaction.test_globals)
        tests_list.insert(0, _BBSIsNotReadingAutonomouslyTest())
        interaction.test_globals = TestList(tests_list)
    return BBRunResult.TRUE
