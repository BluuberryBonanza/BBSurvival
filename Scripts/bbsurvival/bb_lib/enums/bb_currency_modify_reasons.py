"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.enums.classes.bb_int import BBInt
from protocolbuffers import Consts_pb2


class BBCurrencyModifyReason(BBInt):
    """Reasons for modifying currency."""
    CHEAT: 'BBCurrencyModifyReason' = Consts_pb2.TELEMETRY_MONEY_CHEAT
