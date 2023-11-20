"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Iterable, Union, Tuple

import clock
import services
from bbsurvival.bb_lib.dialog.picker_rows.bb_sim_picker_row import BBSimPickerRow
from bbsurvival.bb_lib.utils.bb_alarm_utils import BBAlarmUtils
from bbsurvival.bb_lib.utils.bb_sim_household_utils import BBSimHouseholdUtils
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.prologue.bbs_prologue_data import BBSPrologueData
from bbsurvival.settlement.enums.settlement_member_job import BBSSettlementMemberJobFlags
from bbsurvival.settlement.enums.trait_ids import BBSSettlementTraitId
from bbsurvival.settlement.contexts.settlement_context import BBSSettlementContext
from bbsurvival.settlement.contexts.settlement_member_context import BBSSettlementMemberContext
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.classes.bb_singleton import BBSingleton
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from sims.household import Household
from sims.sim_info import SimInfo

log = BBLogRegistry().register_log(ModIdentity(), 'bbs_settlement_context_manager')
log.enable()


class BBSSettlementContextManager(metaclass=BBSingleton):
    def __init__(self):
        super().__init__()
        self._settlement_context_by_zone_id = dict()
        self._set_head_of_settlement_alarm = None

    def setup_settlement_context_for_current_zone(self) -> Union[BBSSettlementContext, None]:
        current_zone_context = self.get_settlement_context_for_current_zone()
        if current_zone_context is not None:
            return current_zone_context

        current_zone_id = services.current_zone_id()
        member_contexts = list()
        head_of_settlement_sim_info = self._find_or_create_settlement_head_sim_info()
        if head_of_settlement_sim_info is None:
            log.debug('No head of settlement was found for the current zone. (That probably means noone lives here)')
            self._setup_alarm_for_set_head_of_settlement()
            return None
        log.debug('Setting up settlement context with Head of Settlement Sim', sim=head_of_settlement_sim_info)
        BBSimTraitUtils.add_trait(head_of_settlement_sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD)
        member_contexts.append(BBSSettlementMemberContext(
            head_of_settlement_sim_info,
            BBSSettlementMemberJobFlags.NONE,
            True
        ))
        settlement_context = BBSSettlementContext(
            member_contexts
        )
        settlement_context.setup()
        self._settlement_context_by_zone_id[current_zone_id] = settlement_context
        return settlement_context

    def add_settlement_member_context(self, sim_info: SimInfo, head_of_settlement_sim_info_override: SimInfo = None) -> BBRunResult:
        if head_of_settlement_sim_info_override is not None:
            settlement_context = self.get_settlement_context_by_sim_info(head_of_settlement_sim_info_override)
        else:
            settlement_context = self.get_settlement_context_for_current_zone()

        if settlement_context is None:
            log.debug('Failed to locate settlement context.')
            return BBRunResult(False, 'No Settlement exists on the current lot.')

        head_of_settlement_sim_info = settlement_context.get_head_of_settlement_context().sim_info

        from bbsurvival.settlement.utils.settlement_utils import BBSSettlementUtils
        BBSSettlementUtils.add_head_of_settlement_relationship(head_of_settlement_sim_info, sim_info)
        result = BBSimTraitUtils.add_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER)
        log.debug('Trait add result as result of adding settlement member context', result=result, sim_info=sim_info)

        log.debug('Attempting to add sim as member', sim=sim_info)
        if settlement_context.has_member_context(sim_info):
            log.debug('Sim was already in the settlement.', sim=sim_info)
            settlement_context.get_member_context(sim_info).setup()
            return BBRunResult(True, f'{sim_info} was already in the settlement context.')

        log.debug('Adding Sim as member.', sim=sim_info)
        member_context = BBSSettlementMemberContext(
            sim_info,
            BBSSettlementMemberJobFlags.NONE,
            False
        )
        settlement_context.add_member_context(
            member_context
        )
        return BBRunResult.TRUE

    def add_missing_settlement_member_contexts(self) -> BBRunResult:
        settlement_context = self.get_settlement_context_for_current_zone()
        log.debug('Adding missing Settlement members.')

        if settlement_context is None:
            log.debug('No settlement exists on the lot.')
            return BBRunResult(False, 'No Settlement exists on the current lot.')

        head_of_settlement_sim_info = settlement_context.get_head_of_settlement_context().sim_info
        for sim_info in self._find_settlement_member_sim_infos_gen(head_of_settlement_sim_info):
            if settlement_context.has_member_context(sim_info):
                log.debug('Sim already is in the settlement, they are not missing.', sim=sim_info)
                continue

            log.debug('Adding missing settlement member', sim=sim_info)

            member_context = BBSSettlementMemberContext(
                sim_info,
                BBSSettlementMemberJobFlags.NONE,
                False
            )
            settlement_context.add_member_context(
                member_context
            )
        return BBRunResult.TRUE

    def _setup_alarm_for_set_head_of_settlement(self):
        current_zone_id = services.current_zone_id()
        active_household: Household = services.active_household()
        if current_zone_id != active_household.home_zone_id:
            return None

        if self._set_head_of_settlement_alarm is not None:
            return

        def _set_head_of_settlement_callback(manager, __):
            self._set_head_of_settlement_alarm = None
            if not self._has_sims_living_at_current_zone():
                self._setup_alarm_for_set_head_of_settlement()
            manager.create_head_of_settlement()

        time_until_run = clock.interval_in_sim_minutes(2)
        self._set_head_of_settlement_alarm = BBAlarmUtils.schedule_alarm(
            ModIdentity(),
            self,
            time_until_run,
            _set_head_of_settlement_callback
        )

    def create_head_of_settlement(self):
        from bbsurvival.settlement.utils.settlement_utils import BBSSettlementUtils
        current_zone_id = services.current_zone_id()
        sim_rows = list()
        for sim_info in BBSimUtils.get_all_sim_info_gen():
            if BBSSettlementUtils.is_allowed_as_head_of_settlement(sim_info):
                sim_household = BBSimHouseholdUtils.get_household(sim_info)
                home_zone_id = sim_household.home_zone_id
                if current_zone_id == home_zone_id:
                    sim_rows.append(
                        BBSimPickerRow(
                            sim_info,
                        )
                    )

        def _on_submit(_sim_info_list: Tuple[SimInfo]):
            first_sim_info = _sim_info_list[0]
            BBSimTraitUtils.add_trait(first_sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD)
            BBSPrologueData().start_prologue(first_sim_info)
            self.setup_settlement_context_for_current_zone()

        def _on_close():
            self._set_head_of_settlement_alarm = None
            self._setup_alarm_for_set_head_of_settlement()

        if not sim_rows:
            log.debug('No Sims were found to be valid as the Head of Settlement on the current lot!')
            self._set_head_of_settlement_alarm = None
            self._setup_alarm_for_set_head_of_settlement()
            return

        from bbsurvival.bb_lib.dialog.bb_sim_dialog import BBSimDialog
        BBSimDialog(
            ModIdentity(),
            BBLocalizedStringData('Choose a Sim to become Head of Settlement'),
            BBLocalizedStringData('The chosen Sim will become the Head of Settlement.'),
            tuple(sim_rows)
        ).display(BBSimUtils.get_active_sim_info(), _on_submit, on_closed=_on_close)

    def _has_sims_living_at_current_zone(self) -> bool:
        current_zone_id = services.current_zone_id()
        for sim_info in BBSimUtils.get_all_sim_info_gen():
            sim_household = BBSimHouseholdUtils.get_household(sim_info)
            home_zone_id = sim_household.home_zone_id
            if current_zone_id == home_zone_id:
                return True
        return False

    def _find_or_create_settlement_head_sim_info(self) -> Union[SimInfo, None]:
        from bbsurvival.settlement.utils.settlement_utils import BBSSettlementUtils
        current_zone_id = services.current_zone_id()
        for sim_info in BBSimUtils.get_all_sim_info_gen():
            if BBSimTraitUtils.has_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD):
                sim_household = BBSimHouseholdUtils.get_household(sim_info)
                home_zone_id = sim_household.home_zone_id
                if current_zone_id == home_zone_id:
                    return sim_info

        active_household: Household = services.active_household()
        if current_zone_id == active_household.home_zone_id:
            # The active lot is the home zone id of the active Household, we need the player to choose a Head of Settlement for their lot.
            return None
        # If we can't find a Sim with Settlement head trait for the current lot, we'll make one.
        for sim_info in BBSimUtils.get_all_sim_info_gen():
            if BBSSettlementUtils.is_allowed_as_head_of_settlement(sim_info):
                sim_household = BBSimHouseholdUtils.get_household(sim_info)
                home_zone_id = sim_household.home_zone_id
                if current_zone_id == home_zone_id:
                    return sim_info

    def get_settlement_context_for_current_zone(self) -> Union[BBSSettlementContext, None]:
        current_zone_id = services.current_zone_id()
        if current_zone_id in self._settlement_context_by_zone_id:
            return self._settlement_context_by_zone_id[current_zone_id]
        return None

    def get_settlement_context_by_sim_info(self, sim_info: SimInfo) -> Union[BBSSettlementContext, None]:
        for (zone_id, settlement_context) in self._settlement_context_by_zone_id.items():
            settlement_context: BBSSettlementContext = settlement_context
            if settlement_context.has_member_context(sim_info):
                return settlement_context

    def teardown_settlement_context(self) -> BBRunResult:
        settlement_contexts = dict(self._settlement_context_by_zone_id)
        for (sim_id, settlement_context) in settlement_contexts.items():
            if settlement_context is None:
                continue
            settlement_context.teardown()
            del self._settlement_context_by_zone_id[sim_id]
        return BBRunResult(True, 'Successfully tore down settlement context.')

    def _find_settlement_member_sim_infos_gen(self, head_of_settlement_sim_info: SimInfo) -> Iterable[SimInfo]:
        from bbsurvival.settlement.utils.settlement_utils import BBSSettlementUtils
        for sim_info in BBSimUtils.get_all_sim_info_gen():
            if BBSSettlementUtils.has_head_of_settlement_relationship(head_of_settlement_sim_info, sim_info):
                yield sim_info

    def _find_household_members_not_in_settlement_already_gen(self, head_of_settlement_sim_info: SimInfo) -> Iterable[SimInfo]:
        from bbsurvival.settlement.utils.settlement_utils import BBSSettlementUtils
        for sim_info in BBSimUtils.get_all_sim_info_gen():
            if (BBSimHouseholdUtils.is_in_same_household_of_sim(sim_info, head_of_settlement_sim_info)
                    and not BBSimTraitUtils.has_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_MEMBER)
                    and not BBSimTraitUtils.has_trait(sim_info, BBSSettlementTraitId.SETTLEMENT_HEAD)):
                if BBSSettlementUtils.has_head_of_settlement_relationship(head_of_settlement_sim_info, sim_info):
                    yield sim_info

