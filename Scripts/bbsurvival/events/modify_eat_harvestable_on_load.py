"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.bb_lib.utils.bb_instance_utils import BBInstanceUtils
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_end_event import BBOnZoneLoadEndEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from bluuberrylibrary.utils.instances.bb_interaction_utils import BBInteractionUtils
from event_testing.results import TestResult
from event_testing.tests import TestList
from interactions import ParticipantType
from interactions.base.interaction import Interaction
from sims.sim_info_tests import SimInfoTest, MatchType
from sims4.resources import Types
from statistics.statistic_ops import StatisticChangeOp, StatisticSetMaxOp

interactions_modified = False

log = BBLogRegistry().register_log(ModIdentity(), 'bbs_modify_harvestable')
log.enable()


# @BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadEndEvent)
def _bbs_modify_eat_harvestable_on_zone_load(event: BBOnZoneLoadEndEvent) -> BBRunResult:
    global interactions_modified
    if interactions_modified:
        return BBRunResult.TRUE
    interactions_modified = True

    interaction_ids = [
        103820,  # Gardening_EatHarvestable
    ]

    hunger_motive = BBInstanceUtils.get_instance(Types.STATISTIC, 16656)  # motive_Hunger
    toddler_hunger_motive = BBInstanceUtils.get_instance(Types.STATISTIC, 306571)  # commodity_Trait_Toddler_Autonomy_ToddlerPersonalityUpdate_GoodAppetite
    _new_false_advertisements = (
        StatisticChangeOp(amount=1.5, stat=hunger_motive, subject=ParticipantType.Actor),
        StatisticSetMaxOp(stat=toddler_hunger_motive)
    )

    from sims4.collections import make_immutable_slots_class
    immutable_class = make_immutable_slots_class({'desire', 'static_commodity'})

    def _create_static_commodity(desire: float, static_commodity_id: int):
        static_commodity = BBInstanceUtils.get_instance(Types.STATIC_COMMODITY, static_commodity_id)
        if static_commodity is None:
            return None
        immutable_slot_values = dict()
        immutable_slot_values['desire'] = desire
        immutable_slot_values['static_commodity'] = static_commodity
        return immutable_class(immutable_slot_values)

    new_static_commodity_ids = (
        (1.0, 16403),  # Crafting
        (1.0, 24930),  # StaticCommodity_PoliteHunger
        (1.0, 101017),  # StaticCommodity_GrabServing
        (1.0, 106184),  # staticCommodity_SimRay_MindControl_Eat
        (1.0, 136416),  # staticCommodity_Festivals_Overeat
        (8.0, 132359),  # StaticCommodity_Trait_MeltMaster_EatGrilledCheese
        (8.0, 133130),  # StaticCommodity_Trait_Vegetarian_EatVegetarianFood
    )

    new_static_commodities = list()

    for (_desire, new_static_commodity_id) in new_static_commodity_ids:
        new_static_commodity = _create_static_commodity(_desire, new_static_commodity_id)
        if new_static_commodity is None:
            continue
        new_static_commodities.append(new_static_commodity)

    for interaction_id in interaction_ids:
        interaction = BBInteractionUtils.load_interaction_by_guid(interaction_id)
        if interaction is None:
            continue
        interaction._false_advertisements = _new_false_advertisements
        for op in interaction._false_advertisements_gen():
            if interaction._add_autonomy_ad(op, overwrite=True):
                log.debug('Added atonomy ad')
        if new_static_commodities:
            interaction._static_commodities = tuple(new_static_commodities)
        interaction._update_commodity_flags()
        log.debug('Got things', static_commodities=interaction._static_commodities, false_advertisements=interaction._false_advertisements)
    return BBRunResult.TRUE


# @BBInjectionUtils.inject(ModIdentity(), Interaction, Interaction._tuning_loading_callback.__name__)
def _bbs_modify_eat_harvestable(original, cls, *_, **__):
    log.debug('Got the thing', interaction=cls, interaction_dir=dir(cls))
    blah = True
    if blah:
        return original(*_, **__)
    cls_id = getattr(cls, 'guid64')
    interaction_ids = [
        103820,  # Gardening_EatHarvestable
    ]
    if cls_id not in interaction_ids:
        return original(*_, **__)

    hunger_motive = BBInstanceUtils.get_instance(Types.STATISTIC, 16656)  # motive_Hunger
    toddler_hunger_motive = BBInstanceUtils.get_instance(Types.STATISTIC, 306571)  # commodity_Trait_Toddler_Autonomy_ToddlerPersonalityUpdate_GoodAppetite
    _new_false_advertisements = (
        StatisticChangeOp(amount=1.5, stat=hunger_motive, subject=ParticipantType.Actor),
        StatisticSetMaxOp(stat=toddler_hunger_motive)
    )

    from sims4.collections import make_immutable_slots_class
    immutable_class = make_immutable_slots_class({'desire', 'static_commodity'})

    def _create_static_commodity(desire: float, static_commodity_id: int):
        static_commodity = BBInstanceUtils.get_instance(Types.STATIC_COMMODITY, static_commodity_id)
        if static_commodity is None:
            return None
        immutable_slot_values = dict()
        immutable_slot_values['desire'] = desire
        immutable_slot_values['static_commodity'] = static_commodity
        return immutable_class(immutable_slot_values)

    new_static_commodity_ids = (
        (1.0, 16403),  # Crafting
        (1.0, 24930),  # StaticCommodity_PoliteHunger
        (1.0, 101017),  # StaticCommodity_GrabServing
        (1.0, 106184),  # staticCommodity_SimRay_MindControl_Eat
        (1.0, 136416),  # staticCommodity_Festivals_Overeat
        (8.0, 132359),  # StaticCommodity_Trait_MeltMaster_EatGrilledCheese
        (8.0, 133130),  # StaticCommodity_Trait_Vegetarian_EatVegetarianFood
    )

    new_static_commodities = list()

    for (_desire, new_static_commodity_id) in new_static_commodity_ids:
        new_static_commodity = _create_static_commodity(_desire, new_static_commodity_id)
        if new_static_commodity is None:
            continue
        new_static_commodities.append(new_static_commodity)

    cls._false_advertisements = _new_false_advertisements
    if new_static_commodities:
        cls._static_commodities = tuple(new_static_commodities)
    log.debug('Got things', static_commodities=cls._static_commodities, false_advertisements=cls._false_advertisements)
    return original(*_, **__)
