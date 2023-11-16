"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Type, TypeVar, Any, Union

from bbsurvival.bb_lib.enums.bb_component_type import BBComponentType
from objects.components import ComponentContainer, Component
from objects.game_object import GameObject
from sims.sim import Sim

BBExpectedReturnType = TypeVar('BBExpectedReturnType', bound=Any)


class BBComponentUtils:
    """Utilities for manipulating components."""

    # noinspection PyUnusedLocal
    @classmethod
    def add_component(cls, component_container: Union[Sim, GameObject, ComponentContainer], component_type: BBComponentType, return_type: Type[BBExpectedReturnType] = Component) -> Union[BBExpectedReturnType, None]:
        """add_component(component_container, component_type, return_type=Component)

        Add a component to something.

        :param component_container: The thing to add a component to.
        :type component_container: ComponentContainer
        :param component_type: The type of component being added.
        :type component_type: BBComponentType
        :param return_type: The type of the return value.
        :type return_type: Type[BBExpectedReturnType], optional
        :return: The added component from the object.
        :rtype: BBExpectedReturnType or None
        """
        if component_type is None or not isinstance(component_container, ComponentContainer) or not hasattr(component_container, 'get_component'):
            return None
        if component_container.has_component(component_type):
            return cls.get_component(component_container, component_type, return_type=return_type)
        if component_container.add_component(component_type):
            return cls.get_component(component_container, component_type, return_type=return_type)
        return None

    # noinspection PyUnusedLocal
    @classmethod
    def get_component(cls, component_container: Union[Sim, GameObject, ComponentContainer], component_type: BBComponentType, return_type: Type[BBExpectedReturnType] = Component) -> Union[BBExpectedReturnType, None]:
        """get_component(component_container, component_type, return_type=Component)

        Get a component from something.

        :param component_container: The thing to retrieve a component from.
        :type component_container: ComponentContainer
        :param component_type: The type of component being retrieved.
        :type component_type: BBComponentType
        :param return_type: The type of the return value.
        :type return_type: Type[BBExpectedReturnType], optional
        :return: The component from the object.
        :rtype: BBExpectedReturnType or None
        """
        if component_type is None or not isinstance(component_container, ComponentContainer) or not hasattr(component_container, 'get_component'):
            return None
        return component_container.get_component(component_type)
