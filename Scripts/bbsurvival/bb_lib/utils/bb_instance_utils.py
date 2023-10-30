"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Type, Any, TypeVar, ItemsView, Union

import services
from bluuberrylibrary.enums.classes.bb_int import BBInt
from bluuberrylibrary.enums.classes.bb_int_flags import BBIntFlags
from enum import Int
from sims4.resources import Types
from sims4.tuning.dynamic_enum import DynamicEnum, DynamicEnumLocked
from sims4.tuning.instance_manager import InstanceManager

BBEnumType = TypeVar('BBEnumType', int, BBInt, BBIntFlags, Int, DynamicEnum, DynamicEnumLocked)
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

    @classmethod
    def get_enum_from_name(cls, name: str, enum_type: Type[BBEnumType], default_value: BBEnumType = None) -> BBEnumType:
        """get_enum_from_name(name, enum_type, default_value=None)

        Get an enum by using its name.

        :param name: The name of the enum.
        :type name: str
        :param enum_type: The type of enum being got.
        :type enum_type: Type[BBEnumType]
        :param default_value: A value used when an enum is not found matching the name.
        :type default_value: BBEnumType
        :return: An enum with a matching name.
        :rtype: BBEnumType
        """
        if hasattr(enum_type, name):
            return getattr(enum_type, name)
        # noinspection PyBroadException
        try:
            # noinspection PyTypeChecker
            if name in enum_type:
                return enum_type[name]
        except:
            pass
        if hasattr(enum_type, 'name_to_value') and name in enum_type.name_to_value:
            return enum_type.name_to_value.get(name)
        return default_value
