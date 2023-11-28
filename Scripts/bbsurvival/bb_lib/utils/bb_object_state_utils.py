"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Tuple, Dict, Union

from bbsurvival.bb_lib.enums.bb_component_type import BBComponentType
from bbsurvival.bb_lib.utils.bb_component_utils import BBComponentUtils
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.utils.instances.bb_instance_utils import BBInstanceUtils
from objects.components.state import ObjectStateValue, StateComponent, ObjectState
from objects.game_object import GameObject
from sims4.resources import Types


class BBObjectStateUtils:
    """Utilities for manipulating the state of Objects."""
    @classmethod
    def get_object_state_value(cls, game_object: GameObject, object_state: int) -> Union[ObjectStateValue, None]:
        """get_object_state_value(game_object, object_state)

        Get the applied Object State Value for an Object State of an Object.

        :param game_object: A Game Object.
        :type game_object: GameObject
        :param object_state: The Object State to retrieve the value of.
        :type object_state: int
        :return: The Object State Value for the specified Object State or None, if the state is not found.
        :rtype: ObjectStateValue or None
        """
        state_component = BBComponentUtils.get_component(game_object, BBComponentType.STATE, return_type=StateComponent)
        if state_component is None:
            return None
        object_state_instance = cls.load_object_state_by_guid(object_state)
        if object_state_instance is None:
            return None
        if not state_component.has_state(object_state_instance):
            return None
        return state_component.get_state(object_state_instance)

    @classmethod
    def apply_object_state_value(cls, game_object: GameObject, object_state_value: int) -> BBRunResult:
        """apply_object_state_value(game_object, object_state_value)

        Apply an Object State Value to an Object.

        :param game_object: A Game Object.
        :type game_object: GameObject
        :param object_state_value: The Object State value being applied.
        :type object_state_value: int
        :return: The result of running. True, if successful. False, if not.
        :rtype: BBRunResult
        """
        state_component = BBComponentUtils.get_component(game_object, BBComponentType.STATE, return_type=StateComponent)
        if state_component is None:
            return BBRunResult(False, f'Object {game_object} had not state component.')
        object_state_value_instance = cls.load_object_state_value_by_guid(object_state_value)
        if object_state_value_instance is None:
            return BBRunResult(False, f'No Object State Value existed with id {object_state_value}.')
        state_component.set_state(object_state_value_instance.state, object_state_value_instance)
        return BBRunResult.TRUE

    @classmethod
    def set_object_state_value(cls, game_object: GameObject, object_state: int, object_state_value: int) -> BBRunResult:
        """set_object_state_value(game_object, object_state, object_state_value)

        Set the Object State Value of an Object State of an Object.

        :param game_object: A Game Object.
        :type game_object: GameObject
        :param object_state: The Object State to modify.
        :type object_state: int
        :param object_state_value: The value to set the Object State to.
        :type object_state_value: int
        :return: The result of running. True, if successful. False, if not.
        :rtype: BBRunResult
        """
        state_component = BBComponentUtils.get_component(game_object, BBComponentType.STATE, return_type=StateComponent)
        if state_component is None:
            return BBRunResult(False, f'Object {game_object} had not state component.')
        object_state_instance = cls.load_object_state_by_guid(object_state)
        if object_state_instance is None:
            return BBRunResult(False, f'No Object State existed with id {object_state_value}.')
        object_state_value_instance = cls.load_object_state_value_by_guid(object_state_value)
        if object_state_value_instance is None:
            return BBRunResult(False, f'No Object State Value existed with id {object_state_value}.')
        state_component.set_state(object_state_instance, object_state_value_instance)
        return BBRunResult.TRUE

    @classmethod
    def get_object_states(cls, game_object: GameObject) -> Tuple[ObjectState]:
        """get_object_states(game_object)

        Get the Object States of an Object.

        :param game_object: A Game Object.
        :type game_object: GameObject
        :return: A collection of Object States available on an Object.
        :rtype: Tuple[ObjectState]
        """
        if game_object is None:
            return tuple()
        state_component = cls.get_object_state_component(game_object)
        if state_component is None:
            return tuple()
        return tuple(state_component.keys())

    @classmethod
    def get_object_state_values(cls, game_object: GameObject) -> Tuple[ObjectStateValue]:
        """get_object_state_values(game_object)

        Get the Object State Values of an Object.

        .. note:: These are only the current values each state is set to, not all possible values.

        :param game_object: A Game Object.
        :type game_object: GameObject
        :return: A collection of Object State Values currently applied to the Object.
        :rtype: Tuple[ObjectStateValue]
        """
        if game_object is None:
            return tuple()
        state_component = cls.get_object_state_component(game_object)
        if state_component is None:
            return tuple()
        return tuple(state_component.values())

    @classmethod
    def get_object_states_and_values(cls, game_object: GameObject) -> Dict[ObjectState, ObjectStateValue]:
        """get_object_states_and_values(game_object)

        Get the Object States and Object State Values of an Object.

        .. note:: The values of each state is the currently applied state.

        :param game_object: A Game Object.
        :type game_object: GameObject
        :return: A dictionary of Object States to Object State Values on the Object.
        :rtype: Dict[ObjectState, ObjectStateValue]
        """
        if game_object is None:
            return dict()
        state_component = cls.get_object_state_component(game_object)
        if state_component is None:
            return dict()
        # noinspection PyProtectedMember
        return dict(state_component._states)

    @classmethod
    def get_object_state_component(cls, game_object: GameObject) -> Union[StateComponent, None]:
        """get_object_state_component(game_object)

        Get the state component of an object.

        :param game_object: A Game Object.
        :type game_object: GameObject
        :return: The state component of the object or None if the object does not have a state component.
        :rtype: StateComponent or None
        """
        return BBComponentUtils.get_component(game_object, BBComponentType.STATE, return_type=StateComponent)

    @classmethod
    def load_object_state_by_guid(cls, object_state: int) -> Union[ObjectState, None]:
        """load_object_state_by_guid(object_state)

        Load an Object State by its GUID

        :param object_state: The GUID of the Object State to load.
        :type object_state: int
        :return: The loaded Object State or None if not found.
        :rtype: ObjectState or None
        """
        if isinstance(object_state, ObjectState) or object_state is ObjectState:
            return object_state

        return BBInstanceUtils.get_instance(Types.OBJECT_STATE, object_state, return_type=ObjectState)

    @classmethod
    def load_object_state_value_by_guid(cls, object_state_value: int) -> Union[ObjectStateValue, None]:
        """load_object_state_value_by_guid(object_state_value)

        Load an Object State Value by its GUID

        :param object_state_value: The GUID of the Object State Value to load.
        :type object_state_value: int
        :return: The loaded Object State Value or None if not found.
        :rtype: ObjectStateValue or None
        """
        if isinstance(object_state_value, ObjectStateValue) or object_state_value is ObjectStateValue:
            return object_state_value

        return BBInstanceUtils.get_instance(Types.OBJECT_STATE, object_state_value, return_type=ObjectStateValue)
