"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.settlement.enums.trait_ids import BBSSettlementTraitId
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from interactions import ParticipantType
from objects.components.utils.inventory_helpers import get_object_or_lot_inventory, \
    transfer_object_to_lot_or_object_inventory
from objects.game_object import GameObject
from objects.object_creation import ObjectCreationMixin, StateInitializationPreference


# @BBInjectionUtils.inject(ModIdentity(), ObjectCreationMixin, ObjectCreationMixin._place_object.__name__)
def _bbs_override_place_object_for_settlement_members(original, self, created_object: GameObject):
    sim = self.resolver.get_participant(ParticipantType.Actor)
    actor_sim_info = BBSimUtils.to_sim_info(sim)
    if not BBSimTraitUtils.has_trait(actor_sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER):
        return original(self, created_object)
    self._setup_created_object(created_object, creation_stage=StateInitializationPreference.POST_ADD)
    active_household_sim_info = BBSimUtils.get_active_sim_info()
    active_household_sim = BBSimUtils.to_sim_instance(active_household_sim_info)
    active_inventory = get_object_or_lot_inventory(active_household_sim_info)
    recipient_object = None
    if active_inventory is not None:
        recipient_object = active_inventory.owner
    transfer_object_to_lot_or_object_inventory(created_object, active_inventory, recipient_object=recipient_object)
    created_object.set_household_owner_id(active_household_sim.household.id)
    if self.spawn_vfx is not None:
        effect = self.spawn_vfx(created_object)
        effect.start_one_shot()
    return True
