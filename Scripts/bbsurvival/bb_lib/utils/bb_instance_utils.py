"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Type, Any, TypeVar, ItemsView, Union

import services
from sims4.resources import Types
from sims4.tuning.instance_manager import InstanceManager

BBExpectedReturnType = TypeVar('BBExpectedReturnType', bound=Any)


class BBInstanceUtils:
    """Utilities for getting tuning resources."""

    @classmethod
    def get_instance(cls, instance_type: Types, instance_guid: int, return_type: Type[BBExpectedReturnType] = Any) -> Union[BBExpectedReturnType, None]:
        """get_instance(instance_type, instance_guid, return_type=Any)

        Get an instance of a Resource.

        :param instance_type: The type of instance.
        :type instance_type: Types
        :param instance_guid: The GUID of the instance to get.
        :type instance_guid: int
        :param return_type: The type of the returned value.
        :type return_type: Type[BBExpectedReturnType], optional
        :return: The instance or None if not found.
        :rtype: BBExpectedReturnType or None
        """
        return cls.get_instance_manager(instance_type).get(instance_guid)

    # noinspection PyUnusedLocal
    @classmethod
    def get_all_instances(cls, instance_type: Types, return_type: Type[BBExpectedReturnType] = Any) -> ItemsView[str, BBExpectedReturnType]:
        """get_all_instances(instance_type, return_type=Any)

        Get all instances of Resources.

        :param instance_type: The type of instances being loaded.
        :type instance_type: Types
        :param return_type: The type of the returned values.
        :type return_type: Type[BBExpectedReturnType], optional
        :return: All instances in format [Resource Key, Instance]
        :rtype: ItemsView[str, BBExpectedReturnType]
        """
        return cls.get_instance_manager(instance_type).types.items()

    @classmethod
    def get_instance_manager(cls, instance_type: Types) -> Union[InstanceManager, None]:
        """get_instance_manager(instance_type)

        Load the instance manager for an Instance Type.

        :param instance_type: The type of instance manager to retrieve.
        :type instance_type: Types
        :return: The instance manager for a type, if exists. If not found, None will be returned.
        :rtype: InstanceManager or None
        """
        return services.get_instance_manager(instance_type)