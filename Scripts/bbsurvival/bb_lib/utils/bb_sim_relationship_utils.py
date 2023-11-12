"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.utils.instances.bb_instance_utils import BBInstanceUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from sims.sim_info import SimInfo
from sims4.resources import Types


class BBSimRelationshipUtils:
    """Utilities for manipulating statistics on Sims."""

    @classmethod
    def add_relationship_bit(cls, sim_info_a: SimInfo, sim_info_b: SimInfo, relationship_bit: int):
        relationship_bit_instance = BBInstanceUtils.get_instance(Types.RELATIONSHIP_BIT, relationship_bit)
        if relationship_bit_instance is None:
            return
        target_sim_id = BBSimUtils.to_sim_id(sim_info_b)
        relationship_tracker = sim_info_a.relationship_tracker
        if relationship_tracker is None:
            return
        relationship_tracker.add_relationship_bit(target_sim_id, relationship_bit_instance)

    @classmethod
    def remove_relationship_bit(cls, sim_info_a: SimInfo, sim_info_b: SimInfo, relationship_bit: int):
        relationship_bit_instance = BBInstanceUtils.get_instance(Types.RELATIONSHIP_BIT, relationship_bit)
        if relationship_bit_instance is None:
            return
        target_sim_id = BBSimUtils.to_sim_id(sim_info_b)
        relationship_tracker = sim_info_a.relationship_tracker
        if relationship_tracker is None:
            return
        relationship_tracker.remove_relationship_bit(target_sim_id, relationship_bit_instance)

    @classmethod
    def has_relationship_bit(cls, sim_info_a: SimInfo, sim_info_b: SimInfo, relationship_bit: int) -> bool:
        relationship_bit_instance = BBInstanceUtils.get_instance(Types.RELATIONSHIP_BIT, relationship_bit)
        if relationship_bit_instance is None:
            return False
        target_sim_id = BBSimUtils.to_sim_id(sim_info_b)
        relationship_tracker = sim_info_a.relationship_tracker
        if relationship_tracker is None:
            return False
        return relationship_tracker.has_bit(target_sim_id, relationship_bit_instance)
