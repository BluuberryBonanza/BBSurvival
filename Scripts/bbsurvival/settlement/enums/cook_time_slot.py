"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.settlement.enums.statistic_ids import BBSSettlementStatisticId
from bluuberrylibrary.enums.classes.bb_int import BBInt


class BBSSettlementCookTimeSlot(BBInt):
    SLOT_ONE: 'BBSSettlementCookTimeSlot' = ...
    SLOT_TWO: 'BBSSettlementCookTimeSlot' = ...
    SLOT_THREE: 'BBSSettlementCookTimeSlot' = ...

    @classmethod
    def get_hour_statistic(cls, time_slot: 'BBSSettlementCookTimeSlot') -> int:
        if time_slot == BBSSettlementCookTimeSlot.SLOT_ONE:
            return BBSSettlementStatisticId.SETTLEMENT_COOK_COOK_HOUR_ONE
        if time_slot == BBSSettlementCookTimeSlot.SLOT_TWO:
            return BBSSettlementStatisticId.SETTLEMENT_COOK_COOK_HOUR_TWO
        return BBSSettlementStatisticId.SETTLEMENT_COOK_COOK_HOUR_THREE

    @classmethod
    def get_default_cook_hour(cls, time_slot: 'BBSSettlementCookTimeSlot') -> int:
        if time_slot == BBSSettlementCookTimeSlot.SLOT_ONE:
            return 6
        if time_slot == BBSSettlementCookTimeSlot.SLOT_TWO:
            return 12
        return 18

    @classmethod
    def get_minute_statistic(cls, time_slot: 'BBSSettlementCookTimeSlot') -> int:
        if time_slot == BBSSettlementCookTimeSlot.SLOT_ONE:
            return BBSSettlementStatisticId.SETTLEMENT_COOK_COOK_MINUTE_ONE
        if time_slot == BBSSettlementCookTimeSlot.SLOT_TWO:
            return BBSSettlementStatisticId.SETTLEMENT_COOK_COOK_MINUTE_TWO
        return BBSSettlementStatisticId.SETTLEMENT_COOK_COOK_MINUTE_THREE

    @classmethod
    def get_default_cook_minute(cls, time_slot: 'BBSSettlementCookTimeSlot') -> int:
        return 0
