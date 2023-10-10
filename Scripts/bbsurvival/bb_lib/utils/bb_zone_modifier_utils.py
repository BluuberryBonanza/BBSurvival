"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import TYPE_CHECKING, Union

import services
from sims4.resources import Types

if TYPE_CHECKING:
    from zone_modifier.zone_modifier import ZoneModifier


class BBZoneModifierUtils:
    @classmethod
    def add_zone_modifier_to_current_lot(cls, zone_modifier: int):
        current_zone_id = services.current_zone_id()
        cls.add_zone_modifier(current_zone_id, zone_modifier)

    @classmethod
    def add_zone_modifier(cls, zone_id: int, zone_modifier: int):
        persistence_service = services.get_persistence_service()
        zone_data = persistence_service.get_zone_proto_buff(services.current_zone_id())
        if zone_data is None:
            return
        zone_modifier_instance = cls.load_zone_modifier_by_guid(zone_modifier)
        if zone_modifier_instance is None:
            return
        zone_modifier_id = zone_modifier_instance.guid64
        if zone_modifier_id in zone_data.lot_traits:
            return
        zone_data.lot_traits.append(zone_modifier_id)
        services.get_zone_modifier_service().check_for_and_apply_new_zone_modifiers(zone_id)

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