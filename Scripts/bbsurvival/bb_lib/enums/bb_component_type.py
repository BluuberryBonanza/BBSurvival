"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any
from bluuberrylibrary.enums.classes.bb_int import BBInt


class BBComponentType:
    """Types of components."""
    def _get_component_type(*args) -> Any:
        try:
            import objects.components.types as component_types
            return getattr(component_types, args[0])
        except KeyError:
            return args[0]

    INVENTORY: 'BBComponentType' = _get_component_type('INVENTORY_COMPONENT')