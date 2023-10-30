"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from sims.bills import Bills, ALL_BILLS_SOURCE


@BBInjectionUtils.inject(ModIdentity(), Bills, 'can_deliver_bill')
def _bbs_can_deliver_bills(original, *_, **__):
    return False


@BBInjectionUtils.inject(ModIdentity(), Bills, 'current_payment_owed')
def _bbs_current_payment_owed(original, *_, **__):
    return None


@BBInjectionUtils.inject(ModIdentity(), Bills, Bills._get_bill_multiplier.__name__)
def _bbs_get_bill_multiplier(original, *_, **__):
    (multipliers, bill_multiplier_descriptions) = original(*_, **__)
    multipliers[ALL_BILLS_SOURCE] = 0
    return (multipliers, bill_multiplier_descriptions)


@BBInjectionUtils.inject(ModIdentity(), Bills, Bills._get_property_taxes.__name__)
def _bbs_get_property_taxes(original, *_, **__):
    return 0
