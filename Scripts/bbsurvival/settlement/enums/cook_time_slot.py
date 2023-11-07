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
