"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Dict, Any, Type

import services
from bbsurvival.bb_lib.classes.bb_serializable import BBJSONSerializable
from bbsurvival.bb_lib.utils.bb_bitwise_utils import BBBitwiseUtils
from bbsurvival.bb_lib.utils.bb_instance_utils import BBInstanceUtils
from bbsurvival.settlement.enums.settlement_member_job import BBSSettlementMemberJobFlags
from bbsurvival.settlement.enums.situation_ids import BBSSituationId
from bbsurvival.settlement.enums.situation_job_ids import BBSSituationJobId
from bbsurvival.settlement.situations.settlement_member_situation import BBSSettlementMemberSituation
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.utils.instances.bb_situation_utils import BBSituationUtils
from bluuberrylibrary.utils.sims.bb_sim_situation_utils import BBSimSituationUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4.resources import Types
from situations.situation_guest_list import SituationGuestList, SituationGuestInfo, SituationInvitationPurpose


class BBSSettlementMemberContext(BBJSONSerializable):
    def __init__(
        self,
        sim_info: SimInfo,
        job_flags: BBSSettlementMemberJobFlags,
        is_head_of_settlement: bool
    ):
        self._sim_info = sim_info
        self._job_flags = job_flags
        self._is_head_of_settlement = is_head_of_settlement
        self._situation_id = None

    @property
    def sim_info(self) -> SimInfo:
        return self._sim_info

    @property
    def sim(self) -> Sim:
        return BBSimUtils.to_sim_instance(self.sim_info)

    @property
    def sim_id(self) -> int:
        return BBSimUtils.to_sim_id(self.sim_info)

    @property
    def job_flags(self) -> BBSSettlementMemberJobFlags:
        return self._job_flags

    @property
    def is_head_of_settlement(self) -> bool:
        return self._is_head_of_settlement

    @is_head_of_settlement.setter
    def is_head_of_settlement(self, value: bool):
        self._is_head_of_settlement = value

    def has_all_jobs(self, job_flags: BBSSettlementMemberJobFlags) -> bool:
        return BBBitwiseUtils.has_all_bits(self._job_flags, job_flags)

    def has_any_jobs(self, job_flags: BBSSettlementMemberJobFlags) -> bool:
        return BBBitwiseUtils.has_any_bits(self._job_flags, job_flags)

    def add_job(self, job_flags: BBSSettlementMemberJobFlags):
        self._job_flags = BBBitwiseUtils.add_bits(self._job_flags, job_flags)

    def remove_job(self, job_flags: BBSSettlementMemberJobFlags):
        self._job_flags = BBBitwiseUtils.remove_bits(self._job_flags, job_flags)

    def setup(self):
        self._start_situation()

    def is_running_situation(self, sim_info: SimInfo) -> bool:
        sim_id = BBSimUtils.to_sim_id(sim_info)
        if sim_id is None:
            return False
        for situation in BBSimSituationUtils.get_situations(self.sim_info):
            if isinstance(situation, BBSSettlementMemberSituation):
                return True
        return False

    # Override
    def _start_situation(self) -> BBRunResult:
        sim_info = self.sim_info
        situation_manager = services.get_zone_situation_manager()
        if situation_manager is None:
            return BBRunResult(False, reason='No Zone situation manager found.')
        if self.is_running_situation(sim_info):
            return BBRunResult(False, reason=f'Settlement Member {sim_info} is already running situation.')
        is_npc = sim_info.is_npc
        sim_id = self.sim_id

        situation_job = BBInstanceUtils.get_instance(Types.SITUATION_JOB, BBSSituationJobId.SETTLEMENT_MEMBER_NPC)
        guest_list = SituationGuestList(invite_only=is_npc)
        guest_info = SituationGuestInfo.construct_from_purpose(sim_id, situation_job, SituationInvitationPurpose.CAREER)
        guest_info.expectation_preference = True
        guest_list.add_guest_info(guest_info)
        creation_source = str(self)
        situation_type = BBSituationUtils.load_situation_by_guid(BBSSituationId.SETTLEMENT_MEMBER_NPC)
        if situation_type is None:
            return BBRunResult(False, reason='Found a None Situation.')
        situation_id = situation_manager.create_situation(situation_type, guest_list=guest_list, spawn_sims_during_zone_spin_up=True, user_facing=False, creation_source=creation_source)
        self._situation_id = situation_id
        return BBRunResult.TRUE

    def __eq__(self, other: 'BBSSettlementMemberContext'):
        return self.sim_info is other.sim_info

    def serialize(self: 'BBSSettlementMemberContext') -> Dict[str, Any]:
        data = dict()
        data['sim_id'] = self.sim_id
        data['job_flags'] = [job_flag.name for job_flag in BBSSettlementMemberJobFlags.list_values_from_flags(self.job_flags)]
        data['is_head_of_settlement'] = self._is_head_of_settlement
        return data

    @classmethod
    def deserialize(cls: Type['BBSSettlementMemberContext'], serialized_data: Dict[str, Any]) -> 'BBSSettlementMemberContext':
        sim_id = serialized_data['sim_id']
        sim_info = BBSimUtils.to_sim_info(sim_id)
        job_flag_strs = serialized_data['job_flags']
        job_flags = None
        for job_flag_str in job_flag_strs:
            job_flag = BBInstanceUtils.get_enum_from_name(job_flag_str, BBSSettlementMemberJobFlags, default_value=None)
            if job_flag is None:
                continue
            if job_flag == BBSSettlementMemberJobFlags.NONE:
                job_flags = job_flag
                break
            if job_flags is None:
                job_flags = job_flag
            else:
                job_flags = BBBitwiseUtils.add_bits(job_flags, job_flag)

        is_head_of_community = serialized_data['is_head_of_settlement']

        return BBSSettlementMemberContext(
            sim_info,
            job_flags,
            is_head_of_community
        )
