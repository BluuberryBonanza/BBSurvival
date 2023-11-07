"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Tuple, List, Dict, Any, Type

from bbsurvival.bb_lib.classes.bb_serializable import BBJSONSerializable
from bbsurvival.bb_lib.utils.bb_sim_household_utils import BBSimHouseholdUtils
from bbsurvival.settlement.contexts.settlement_member_context import BBSSettlementMemberContext
from sims.sim_info import SimInfo


class BBSSettlementContext(BBJSONSerializable):

    def __init__(
        self,
        member_contexts: List[BBSSettlementMemberContext]
    ):
        self._member_contexts = list(member_contexts)
        self._is_running = False
        head_sims_of_community = list()
        for member_context in self._member_contexts:
            if member_context.is_head_of_settlement:
                head_sims_of_community.append(member_context)

        if len(head_sims_of_community) > 0:
            new_head_of_household = None
            for head_sim_community in head_sims_of_community:
                if new_head_of_household is None:
                    new_head_of_household = head_sim_community
                else:
                    head_sim_community.is_head_of_settlement = False
        elif len(head_sims_of_community) == 0:
            self._member_contexts[0].is_head_of_settlement = True

        for member_context in self._member_contexts:
            if member_context.is_head_of_settlement:
                self._head_member_context = member_context
                break

        head_sim_community = BBSimHouseholdUtils.get_household(self.head_member_context.sim_info)
        if head_sim_community is not None:
            self._home_zone_id = head_sim_community.home_zone_id
        else:
            self._home_zone_id = -1

    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def head_member_context(self) -> BBSSettlementMemberContext:
        return self._head_member_context

    @property
    def home_zone_id(self) -> int:
        return self._home_zone_id

    @property
    def member_contexts(self) -> Tuple[BBSSettlementMemberContext]:
        return tuple(self._member_contexts)

    def has_member_context(self, sim_info: SimInfo) -> bool:
        return self.get_member_context(sim_info) is not None

    def add_member_context(self, member_context: BBSSettlementMemberContext):
        if self.has_member_context(member_context.sim_info):
            return
        self._member_contexts.append(member_context)

    def remove_member_context(self, member_context: BBSSettlementMemberContext):
        if not self.has_member_context(member_context.sim_info):
            return
        if member_context in self._member_contexts:
            self._member_contexts.remove(member_context)

    def get_member_context(self, sim_info: SimInfo) -> BBSSettlementMemberContext:
        for member_context in self.member_contexts:
            if member_context.sim_info is sim_info:
                return member_context

    def setup(self) -> None:
        for member_context in self.member_contexts:
            member_context.setup()
        self._is_running = True

    def teardown(self) -> None:
        for member_context in self.member_contexts:
            member_context.teardown()
        self._is_running = False

    def serialize(self: 'BBSSettlementContext') -> Dict[str, Any]:
        data = dict()
        data['member_contexts'] = [member_context.serialize() for member_context in self.member_contexts]
        return data

    @classmethod
    def deserialize(cls: Type['BBSSettlementContext'], serialized_data: Dict[str, Any]) -> 'BBSSettlementContext':
        member_contexts = list()

        for member_context_data in serialized_data['member_contexts']:
            member_context = BBSSettlementMemberContext.deserialize(member_context_data)
            if not member_context:
                continue
            member_contexts.append(member_context)

        return BBSSettlementContext(
            member_contexts,
        )
