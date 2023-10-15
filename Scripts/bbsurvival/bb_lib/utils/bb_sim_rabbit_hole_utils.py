"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Callable

from bbsurvival.bb_lib.utils.bb_rabbit_hole_utils import BBRabbitHoleUtils
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from sims.sim_info import SimInfo


class BBSimRabbitHoleUtils:
    """Utilities for manipulating Sims inside rabbit holes."""

    @classmethod
    def send_into_rabbit_hole(cls, sim_info: SimInfo, rabbit_hole: int, on_leave_rabbit_hole: Callable[[SimInfo, bool], None] = None) -> BBRunResult:
        """send_into_rabbit_hole(sim_info, rabbit_hole, on_leave_rabbit_hole=None)

        Send a Sim into a Rabbit Hole to do whatever.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param rabbit_hole: The rabbit hole to send the Sim into.
        :type rabbit_hole: int
        :param on_leave_rabbit_hole: Called when the Sim leaves the rabbit hole. Default is None.
        :type on_leave_rabbit_hole: Callable[[SimInfo, bool], None], optional
        :return: The result of sending the Sim.
        :rtype: BBRunResult
        """
        if sim_info is None:
            raise AssertionError('sim_info was None')
        rabbit_hole_instance = BBRabbitHoleUtils.load_rabbit_hole_by_guid(rabbit_hole)
        if rabbit_hole_instance is None:
            return BBRunResult(False, reason=f'No rabbit hole existed with id {rabbit_hole}.')

        sim_id = BBSimUtils.to_sim_id(sim_info)
        rabbit_hole_service = BBRabbitHoleUtils.get_rabbit_hole_service()
        rabbit_hole_id = rabbit_hole_service.put_sim_in_managed_rabbithole(sim_info, rabbit_hole_type=rabbit_hole_instance)
        if rabbit_hole_id is not None:
            if on_leave_rabbit_hole is not None:
                def _on_leave_rabbit_hole(canceled: bool = False):
                    on_leave_rabbit_hole(sim_info, canceled)
                    rabbit_hole_service.remove_rabbit_hole_expiration_callback(sim_id, rabbit_hole_id, _on_leave_rabbit_hole)

                rabbit_hole_service.set_rabbit_hole_expiration_callback(sim_id, rabbit_hole_id, _on_leave_rabbit_hole)
            return BBRunResult.TRUE
        return BBRunResult(False, f'Failed to send the Sim into rabbit hole {rabbit_hole_instance}.')