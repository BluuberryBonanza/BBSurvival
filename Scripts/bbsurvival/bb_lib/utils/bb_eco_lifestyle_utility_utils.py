import services
from bbsurvival.bb_lib.utils.bb_component_utils import BBComponentUtils
from objects.components.statistic_component import StatisticComponent
from sims4.resources import Types


class BBEcoLifestyleUtilityUtils:
    """Utilities for manipulating Eco Lifestyle Utilities."""
    @classmethod
    def get_eco_footprint_level(cls, zone_id: int) -> float:
        """get_eco_footprint_level(zone_id)

        Get the eco footprint level of a Zone.

        :param zone_id: The ID of a Zone.
        :type zone_id: int
        :return: The amount of eco footprint level of the Zone.
        :rtype: float
        """
        zone = services.get_zone(zone_id)
        lot = zone.lot
        import objects.components.types
        statistic_component: StatisticComponent = None if lot is None else BBComponentUtils.get_component(lot, objects.components.types.STATISTIC_COMPONENT, return_type=StatisticComponent)
        instance_manager = services.get_instance_manager(Types.STATISTIC)
        statistic_eco_footprint = instance_manager.get(233233)  # commodity_EcoFootprint_Lot
        return statistic_component.get_stat_value(statistic_eco_footprint)

    @classmethod
    def set_eco_footprint_level(cls, zone_id: int, level: float):
        """set_eco_footprint_level(zone_id, level)

        Set the eco footprint level of a Zone.

        :param zone_id: The ID of a Zone.
        :type zone_id: int
        :param level: The eco footprint level to set the Zone to.
        :type level: float
        """
        zone = services.get_zone(zone_id)
        lot = zone.lot
        import objects.components.types
        statistic_component: StatisticComponent = None if lot is None else BBComponentUtils.get_component(lot, objects.components.types.STATISTIC_COMPONENT, return_type=StatisticComponent)
        instance_manager = services.get_instance_manager(Types.STATISTIC)
        statistic_eco_footprint = instance_manager.get(233233)  # commodity_EcoFootprint_Lot
        statistic_component.set_stat_value(statistic_eco_footprint, level)

    @classmethod
    def get_power_level(cls, zone_id: int) -> float:
        """get_power_level(zone_id)

        Get the power level of a Zone.

        :param zone_id: The ID of a Zone.
        :type zone_id: int
        :return: The amount of power the Zone has available.
        :rtype: float
        """
        zone = services.get_zone(zone_id)
        lot = zone.lot
        import objects.components.types
        statistic_component: StatisticComponent = None if lot is None else BBComponentUtils.get_component(lot, objects.components.types.STATISTIC_COMPONENT, return_type=StatisticComponent)
        instance_manager = services.get_instance_manager(Types.STATISTIC)
        statistic_power = instance_manager.get(233027)  # commodity_Utilities_Power
        return statistic_component.get_stat_value(statistic_power)

    @classmethod
    def set_power_level(cls, zone_id: int, level: float):
        """set_power_level(zone_id, level)

        Set the power level available for a Zone.

        :param zone_id: The ID of a Zone.
        :type zone_id: int
        :param level: The amount of power wanted to be available.
        :type level: float
        """
        zone = services.get_zone(zone_id)
        lot = zone.lot
        import objects.components.types
        statistic_component: StatisticComponent = None if lot is None else BBComponentUtils.get_component(lot, objects.components.types.STATISTIC_COMPONENT, return_type=StatisticComponent)
        instance_manager = services.get_instance_manager(Types.STATISTIC)
        statistic_power = instance_manager.get(233027)  # commodity_Utilities_Power
        statistic_component.set_stat_value(statistic_power, level)

    @classmethod
    def get_water_level(cls, zone_id: int) -> float:
        """get_water_level(zone_id)

        Get the water level of a Zone.

        :param zone_id: The ID of a Zone.
        :type zone_id: int
        :return: The amount of water the Zone has available.
        :rtype: float
        """
        zone = services.get_zone(zone_id)
        lot = zone.lot
        import objects.components.types
        statistic_component: StatisticComponent = None if lot is None else BBComponentUtils.get_component(lot, objects.components.types.STATISTIC_COMPONENT, return_type=StatisticComponent)
        instance_manager = services.get_instance_manager(Types.STATISTIC)
        statistic_water = instance_manager.get(233028)  # commodity_Utilities_Water
        return statistic_component.get_stat_value(statistic_water)

    @classmethod
    def set_water_level(cls, zone_id: int, level: float):
        """set_water_level(zone_id, level)

        Set the water level available for a Zone.

        :param zone_id: The ID of a Zone.
        :type zone_id: int
        :param level: The amount of water wanted to be available.
        :type level: float
        """
        zone = services.get_zone(zone_id)
        lot = zone.lot
        import objects.components.types
        statistic_component: StatisticComponent = None if lot is None else BBComponentUtils.get_component(lot, objects.components.types.STATISTIC_COMPONENT, return_type=StatisticComponent)
        instance_manager = services.get_instance_manager(Types.STATISTIC)
        statistic_water = instance_manager.get(233028)  # commodity_Utilities_Water
        statistic_component.set_stat_value(statistic_water, level)
