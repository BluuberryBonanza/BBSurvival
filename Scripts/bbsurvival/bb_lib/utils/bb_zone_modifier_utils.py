"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import TYPE_CHECKING, Union

import services
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from event_testing.results import TestResult
from sims4.resources import Types

if TYPE_CHECKING:
    from zone_modifier.zone_modifier import ZoneModifier


class BBZoneModifierUtils:
    """Utilities for manipulating zone modifiers."""

    @classmethod
    def add_zone_modifier_to_current_lot(cls, zone_modifier: int) -> BBRunResult:
        """add_zone_modifier_to_current_lot(zone_modifier)

        Add a Zone Modifier to the current lot.

        :param zone_modifier: The Zone Modifier to add.
        :type zone_modifier: int
        :return: The result of running the function. True, if successful. False, if not.
        :rtype: BBRunResult
        """
        current_zone_id = services.current_zone_id()
        return cls.add_zone_modifier(current_zone_id, zone_modifier)

    @classmethod
    def add_zone_modifier(cls, zone_id: int, zone_modifier: int) -> BBRunResult:
        """add_zone_modifier(zone_id, zone_modifier)

        Add a Zone Modifier to a lot.

        :param zone_id: The Zone to modify.
        :type zone_id: int
        :param zone_modifier: The Zone Modifier to add.
        :type zone_modifier: int
        :return: The result of running the function. True, if successful. False, if not.
        :rtype: BBRunResult
        """
        persistence_service = services.get_persistence_service()
        zone_data = persistence_service.get_zone_proto_buff(services.current_zone_id())
        if zone_data is None:
            return BBRunResult(False, f'The Zone specified {zone_id} does not exist.')
        zone_modifier_instance = cls.load_zone_modifier_by_guid(zone_modifier)
        if zone_modifier_instance is None:
            return BBRunResult(False, f'The Zone Modifier specified {zone_modifier} does not exist.')
        zone_modifier_id = getattr(zone_modifier_instance, 'guid64')
        if zone_modifier_id in zone_data.lot_traits:
            return BBRunResult(False, f'The Zone {zone_data} already had Modifier {zone_modifier_instance}.')
        zone_data.lot_traits.append(zone_modifier_id)
        services.get_zone_modifier_service().check_for_and_apply_new_zone_modifiers(zone_id)
        return BBRunResult.TRUE

    @classmethod
    def remove_zone_modifier(cls, zone_id: int, zone_modifier: int) -> BBRunResult:
        """remove_zone_modifier(zone_id, zone_modifier)

        Remove a Zone Modifier from a lot.

        :param zone_id: The Zone to modify.
        :type zone_id: int
        :param zone_modifier: The Zone Modifier to remove.
        :type zone_modifier: int
        :return: The result of running the function. True, if successful. False, if not.
        :rtype: BBRunResult
        """
        persistence_service = services.get_persistence_service()
        zone_data = persistence_service.get_zone_proto_buff(services.current_zone_id())
        if zone_data is None:
            return BBRunResult(False, f'The Zone specified {zone_id} does not exist.')
        zone_modifier_instance = cls.load_zone_modifier_by_guid(zone_modifier)
        if zone_modifier_instance is None:
            return BBRunResult(False, f'The Zone Modifier specified {zone_modifier} does not exist.')
        zone_modifier_id = getattr(zone_modifier_instance, 'guid64')
        if zone_modifier_id not in zone_data.lot_traits:
            return BBRunResult(True, f'The Zone {zone_data} did not have Modifier {zone_modifier_instance}.')
        zone_data.lot_traits.remove(zone_modifier_id)
        services.get_zone_modifier_service().check_for_and_apply_new_zone_modifiers(zone_id)
        return BBRunResult.TRUE

    @classmethod
    def load_zone_modifier_by_guid(cls, zone_modifier: int) -> Union['ZoneModifier', None]:
        """load_zone_modifier_by_guid(zone_modifier)

        Load a Zone Modifier by its GUID

        :param zone_modifier: The GUID of the Zone Modifier to load.
        :type zone_modifier: int
        :return: The loaded Zone Modifier or None if not found.
        :rtype: ZoneModifier or None
        """
        from zone_modifier.zone_modifier import ZoneModifier
        if isinstance(zone_modifier, ZoneModifier):
            return zone_modifier
        instance_manager = services.get_instance_manager(Types.ZONE_MODIFIER)
        return instance_manager.get(zone_modifier)
