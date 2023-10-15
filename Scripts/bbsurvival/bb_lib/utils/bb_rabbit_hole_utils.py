"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union

import services
from rabbit_hole.rabbit_hole import RabbitHole
from services.rabbit_hole_service import RabbitHoleService
from sims4.resources import Types


class BBRabbitHoleUtils:
    """Utilities for Managing rabbit holes."""

    @classmethod
    def load_rabbit_hole_by_guid(cls, rabbit_hole: int) -> Union[RabbitHole, None]:
        """load_rabbit_hole_by_guid(rabbit_hole)

        Load a Rabbit Hole by its GUID

        :param rabbit_hole: The GUID of the Rabbit Hole to load.
        :type rabbit_hole: int
        :return: The loaded Rabbit Hole or None if not found.
        :rtype: RabbitHole or None
        """
        if isinstance(rabbit_hole, RabbitHole):
            return rabbit_hole
        instance_manager = services.get_instance_manager(Types.RABBIT_HOLE)
        return instance_manager.get(rabbit_hole)

    @classmethod
    def get_rabbit_hole_service(cls) -> RabbitHoleService:
        """get_rabbit_hole_service()

        Get the service for Rabbit Holes.

        :return: The service for rabbit holes.
        :rtype: RabbitHoleService
        """
        return services.get_rabbit_hole_service()
