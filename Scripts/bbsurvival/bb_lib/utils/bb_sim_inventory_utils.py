from typing import Callable, Union, Iterable

import services
from bbsurvival.bb_lib.enums.bb_component_type import BBComponentType
from bbsurvival.bb_lib.utils.bb_component_utils import BBComponentUtils
from bbsurvival.bb_lib.utils.bb_sim_location_utils import BBSimLocationUtils
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.utils.objects.bb_object_spawn_utils import BBObjectSpawnUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from objects.components.sim_inventory_component import SimInventoryComponent
from objects.game_object import GameObject
from sims.sim_info import SimInfo
from sims4.math import Location


class BBSimInventoryUtils:
    """Utilities for manipulating the inventory of Sims."""
    @classmethod
    def has_inventory(cls, sim_info: SimInfo) -> bool:
        """has_inventory(sim_info)

        Check if a Sim has an inventory.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has an inventory. False, if not.
        :rtype: bool
        """
        return cls.get_inventory(sim_info) is not None

    @classmethod
    def has_any_inventory_items(cls, sim_info: SimInfo) -> bool:
        """has_any_inventory_items(sim_info)

        Check if a Sim has any items in their inventory.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has any items in their inventory. False, if not.
        :rtype: bool
        """
        for _ in cls.get_inventory_items_gen(sim_info):
            return True
        return False

    @classmethod
    def transfer_inventory_to_sim(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> BBRunResult:
        """transfer_inventory_to_sim(sim_info_a, sim_info_b)

        Transfer all inventory items of Sim A to the inventory of Sim B.

        :param sim_info_a: The info of a Sim. The items of this Sim will be transferred.
        :type sim_info_a: SimInfo
        :param sim_info_b: The info of a Sim. This Sim will receive all items from Sim A.
        """
        sim_b_inventory = cls.get_inventory(sim_info_b)
        if sim_b_inventory is None:
            return BBRunResult(False, f'{sim_info_b} does not have an inventory to transfer to.')
        sim_a_inventory = cls.get_inventory(sim_info_a)
        if sim_a_inventory is None:
            return BBRunResult(False, f'{sim_info_a} does not have an inventory to transfer from.')
        sim_a_visible_storage = sim_a_inventory.visible_storage
        if sim_a_visible_storage is not None:
            for visible_inventory_item in tuple(sim_a_visible_storage):
                sim_a_inventory.visible_storage.remove(visible_inventory_item, count=visible_inventory_item.stack_count())
                sim_b_inventory.visible_storage.insert(visible_inventory_item, sim_b_inventory.owner)

        sim_a_hidden_storage = sim_a_inventory.hidden_storage
        if sim_a_hidden_storage is not None:
            for hidden_inventory_item in tuple(sim_a_hidden_storage):
                sim_a_inventory.hidden_storage.remove(hidden_inventory_item, count=hidden_inventory_item.stack_count())
                sim_b_inventory.visible_storage.insert(hidden_inventory_item, sim_b_inventory.owner)
        # sim_a_inventory.purge_inventory()
        return BBRunResult.TRUE

    @classmethod
    def get_inventory(cls, sim_info: SimInfo) -> Union[SimInventoryComponent, None]:
        """get_inventory(sim_info)

        Get the inventory of a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: The inventory of the Sim or None, if not found.
        :rtype: SimInventoryComponent or None
        """
        sim = BBSimUtils.to_sim_instance(sim_info)
        if sim is None:
            return None
        return BBComponentUtils.get_component(sim, BBComponentType.INVENTORY)

    @classmethod
    def has_inventory_item_by_definition(cls, sim_info: SimInfo, object_definition: int) -> bool:
        """has_inventory_item_by_definition(sim_info, object_definition)

        Check if an item exists in the inventory of a Sim by definition.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param object_definition: The Object Definition ID to look for.
        :type object_definition: int
        :return: True, if the Sim has the item in their inventory. False, if not.
        :rtype: bool
        """
        for inventory_item in cls.get_inventory_items_gen(sim_info):
            if inventory_item.definition.id == object_definition:
                return True
        return False

    @classmethod
    def get_inventory_items_gen(cls, sim_info: SimInfo) -> Iterable[GameObject]:
        """get_inventory_items_gen(sim_info)

        Get the items in the inventory of a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: An iterable of Game Objects in the inventory of a Sim.
        :rtype: Iterable[GameObject]
        """
        inventory = cls.get_inventory(sim_info)
        if inventory is None:
            return tuple()
        for item in inventory:
            yield item

    @classmethod
    def create_in_inventory(
        cls,
        sim_info: SimInfo,
        object_definition: int,
        count: int = 1,
        on_init: Callable[[GameObject], None] = None,
        on_added: Callable[[GameObject], None] = None
    ) -> BBRunResult:
        """create_in_inventory(\
            sim_info,\
            object_definition_id,\
            count=1,\
            on_init=None,\
            on_added=None\
        )

        Create and move Game Objects to the inventory of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param object_definition: The definition of the game object.
        :type object_definition: int
        :param count: The number of Game Objects to add. Default is 1.
        :type count: int, optional
        :param on_init: Occurs when the object is initialized. Default is None.
        :type on_init: Callable[[GameObject], None], optional
        :param on_added: Occurs when the object is added to the Object Manager. Default is nothing.
        :type on_added: Callable[[GameObject], None], optional
        :return: The result of creating the objects. True, if successful. False, if not.
        :rtype: BBRunResult
        """
        if not cls.has_inventory(sim_info):
            return BBRunResult(False, f'{sim_info} does not have an inventory.')

        def _on_added(_game_object: GameObject) -> None:
            cls.move_object_to_inventory(sim_info, _game_object)
            if on_added is not None:
                on_added(_game_object)

        success = True
        sim_location = BBSimLocationUtils.get_location(sim_info)
        for _ in range(count):
            game_object = BBObjectSpawnUtils.spawn_object_at_location(object_definition, sim_location, on_init=on_init, on_added=_on_added)
            if game_object.result is None:
                success = False
        if success:
            return BBRunResult(success, 'Successfully added objects.')
        return BBRunResult(success, 'Failed to add some or all objects.')

    @classmethod
    def _create_empty_location(cls) -> Location:
        # noinspection PyUnresolvedReferences
        from sims4.math import Transform, Quaternion, Vector3
        from routing import SurfaceIdentifier, SurfaceType
        transform = Transform(Vector3(0.0, 0.0, 0.0), Quaternion(0.0, 0.0, 0.0, 0.0))
        current_zone_id = services.current_zone_id()
        routing_surface = SurfaceIdentifier(current_zone_id, 0, SurfaceType.SURFACETYPE_WORLD)
        return Location(transform, routing_surface, None, None, 0)

    @classmethod
    def move_object_to_inventory(cls, sim_info: SimInfo, game_object: GameObject, change_ownership: bool = True) -> BBRunResult:
        """move_object_to_inventory(sim_info, game_object, change_ownership=True)

        Move an Object to the inventory of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param change_ownership: If True, the owner of the moved object will be the Sim. If False, the owner of the object will not change. Default is True.
        :type change_ownership: bool, optional
        :return: True, if the object was successfully moved to the inventory of the specified Sim. False, if not.
        :rtype: BBRunResult
        """
        inventory_component: SimInventoryComponent = cls.get_inventory(sim_info)
        if inventory_component is None:
            return BBRunResult(False, f'Failed, {sim_info} did not have an inventory to add to.')
        sim = BBSimUtils.to_sim_instance(sim_info)
        if sim is None:
            return BBRunResult(False, f'Failed, {sim_info} was not available to add to their inventory.')
        if change_ownership:
            game_object.update_ownership(sim, make_sim_owner=True)
        result = inventory_component.player_try_add_object(game_object)
        if not result:
            return BBRunResult(False, f'Failed to move the object {game_object} to the inventory of {sim_info}.')
        return BBRunResult(True, f'Successfully moved object {game_object} to the inventory of {sim_info}.')
