"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Tuple

from bbsurvival.enums.interaction_ids import BBSInteractionId
from bluuberrylibrary.interactions.registration.bb_interaction_registry import BBInteractionRegistry
from bluuberrylibrary.interactions.registration.handlers.bb_sim_interaction_handler import BBSimInteractionHandler


@BBInteractionRegistry.register()
class _BBSSimInteractionRegistration(BBSimInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        return (
            BBSInteractionId.SCAVENGE_QUICK,
        )
