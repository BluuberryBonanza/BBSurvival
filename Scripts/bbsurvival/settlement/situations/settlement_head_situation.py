"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any, List

import clock
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from date_and_time import TimeSpan
from role.role_state import RoleState
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4.tuning.tunable import AutoFactoryInit, HasTunableFactory
from sims4.utils import classproperty
from situations.situation import Situation
from situations.situation_complex import SituationComplexCommon, SituationState, SituationStateData
from situations.situation_job import SituationJob
from situations.situation_types import SituationSerializationOption


class _BBSSettlementHeadSituationBaseState(HasTunableFactory, AutoFactoryInit, SituationState):
    FACTORY_TUNABLES = {
        'role_state': RoleState.TunableReference(
            description='\n                The role state that is active on the Sim for the duration\n                of this state.\n                '
        ),
    }

    __slots__ = {
        'role_state',
    }

    def __init__(self, *_, **__) -> None:
        super().__init__(*_, **__)
        self.owner: BBSSettlementHeadSituation = self.owner

    def on_activate(self, reader=None) -> None:
        owner = self.owner
        if owner is None:
            return
        super().on_activate(reader=reader)
        owner._set_job_role_state(owner.situation_job, self.role_state)

    def _on_interaction_of_interest_complete(self, **kwargs) -> Any:
        pass

    def save_state(self, writer):
        pass


class _BBSSettlementHeadSituationState(_BBSSettlementHeadSituationBaseState):
    pass


class BBSSettlementHeadSituation(SituationComplexCommon):
    INSTANCE_TUNABLES = {
        'situation_job': SituationJob.TunableReference(description='\n            The situation job for the Sim.\n            '),
        'working_state': _BBSSettlementHeadSituationState.TunableFactory(
            description='\n            The state during which the Sim hangs out on the lot.\n            ',
        ),
    }
    REMOVE_INSTANCE_TUNABLES = Situation.NON_USER_FACING_REMOVE_INSTANCE_TUNABLES

    __slots__ = {'situation_job', 'working_state'}

    def __init__(self, *_, **__):
        super().__init__(*_, **__)
        SituationComplexCommon.__init__(self, *_, **__)
        self._sim_info = None

    @property
    def sim_info(self) -> SimInfo:
        if self._sim_info is None:
            self._sim_info = next(self._guest_list.invited_sim_infos_gen(), None)
        return self._sim_info

    @classmethod
    def _state_to_uid(cls, state_to_find: SituationState) -> int:
        return 1

    @classmethod
    def _uid_to_state_data(cls, uid_to_find):
        return cls._states()[0]

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def _states(cls) -> List[SituationStateData]:
        return [
            # *super_states,
            SituationStateData(1, _BBSSettlementHeadSituationState, factory=cls.working_state),
        ]

    @classmethod
    def default_job(cls) -> SituationJob:
        return cls.situation_job

    @classmethod
    def _get_tuned_job_and_default_role_state_tuples(cls) -> Any:
        return [(cls.situation_job, cls.working_state.role_state)]

    @classmethod
    def get_sims_expected_to_be_in_situation(cls) -> int:
        return 1

    # noinspection PyMissingOrEmptyDocstring,PyMethodParameters
    @classproperty
    def situation_serialization_option(cls) -> SituationSerializationOption:
        return SituationSerializationOption.DONT

    def _save_custom_state(self, writer):
        pass

    def _load_custom_state(self, reader):
        self._change_state(self.working_state())

    def _on_set_sim_job(self, sim: Sim, job_type: SituationJob) -> None:
        super()._on_set_sim_job(sim, job_type)
        sim_info = BBSimUtils.to_sim_info(sim)
        self._sim_info = sim_info
        self._change_state(self.working_state())

    def _situation_timed_out(self, _) -> Any:
        pass

    # noinspection PyMethodMayBeStatic
    def _get_remaining_time(self) -> TimeSpan:
        return clock.interval_in_sim_hours(999)

    def on_ask_sim_to_leave(self, sim):
        return False
