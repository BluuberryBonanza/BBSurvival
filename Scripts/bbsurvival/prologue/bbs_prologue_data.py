"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Callable

import clock
from bbsurvival.bb_lib.utils.bb_alarm_utils import BBAlarmUtils
from bbsurvival.bb_lib.utils.bb_sim_statistic_utils import BBSimStatisticUtils
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.prologue.enums.statistic_ids import BBSPrologueStatisticId
from bbsurvival.prologue.enums.trait_ids import BBSPrologueTraitId
from bluuberrylibrary.classes.bb_singleton import BBSingleton
from bluuberrylibrary.dialogs.icons.bb_sim_icon_info import BBSimIconInfo
from bluuberrylibrary.dialogs.notifications.bb_notification import BBNotification
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.sims.bb_sim_trait_utils import BBSimTraitUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from sims.sim_info import SimInfo
from sims4.commands import Command, CommandType

log = BBLogRegistry().register_log(ModIdentity(), 'bbs_prologue_log')
log.enable()


class BBSPrologueData(metaclass=BBSingleton):
    """Data related to the prologue."""
    def __init__(self):
        super().__init__()
        self._on_activate_callbacks = list()
        self._setup_prologue_alarm = None

    def is_mod_fully_active(self):
        for sim_info in BBSimUtils.get_all_sim_info_gen():
            if BBSimTraitUtils.has_trait(sim_info, BBSPrologueTraitId.PROLOGUE_COMPLETED):
                return True
        return False

    def register_on_activate(self, func: Callable[[], None]):
        if func in self._on_activate_callbacks:
            return
        self._on_activate_callbacks.append(func)

    def set_mod_fully_active(self):
        if self.is_mod_fully_active():
            return

        for sim_info in BBSimUtils.get_all_sim_info_gen():
            BBSimTraitUtils.add_trait(sim_info, BBSPrologueTraitId.PROLOGUE_COMPLETED)
            BBSimTraitUtils.remove_trait(sim_info, BBSPrologueTraitId.RUNNING_PROLOGUE)

        for on_activate_func in self._on_activate_callbacks:
            on_activate_func()

    def start_prologue(self, sim_info: SimInfo):
        if self.is_mod_fully_active():
            log.debug('Not starting prologue, the mod is already fully active.')
            return
        if sim_info.is_npc:
            log.debug('Not starting prologue for Sim, they are an NPC.', sim=sim_info)
            return
        existing_sim_running_prologue = self.get_sim_running_prologue()
        if existing_sim_running_prologue is not None:
            log.debug('Not starting prologue for Sim, there is already another Sim running the prologue.', sim=sim_info, existing_sim_running_prologue=existing_sim_running_prologue)
            return
        if BBSimTraitUtils.add_trait(sim_info, BBSPrologueTraitId.RUNNING_PROLOGUE):
            log.debug('Added running prologue trait to Sim', sim=sim_info)
            BBSimStatisticUtils.set_statistic_value(sim_info, BBSPrologueStatisticId.PROLOGUE_STAGE, 0)
            BBNotification(
                ModIdentity(),
                BBLocalizedStringData('I Have a Bad Feeling'),
                BBLocalizedStringData('I have a really bad feeling, I should watch the news on a Television immediately!')
            ).show(icon=BBSimIconInfo(sim_info))
        elif self._setup_prologue_alarm is None:
            log.debug('Failed to add running prologue to Sim, setting an alarm to set it up.', sim=sim_info)

            def _setup_prologue(_sim_info: SimInfo, _):
                log.debug('Setting up the prologue after an alarm.', sim=sim_info)
                self._setup_prologue_alarm = None
                self.start_prologue(_sim_info)

            time_until_first_drop_off_supplies = clock.interval_in_sim_minutes(2)
            self._setup_prologue_alarm = BBAlarmUtils.schedule_alarm(
                ModIdentity(),
                sim_info,
                time_until_first_drop_off_supplies,
                _setup_prologue
            )

    def get_prologue_stage(self, sim_info: SimInfo) -> int:
        if not BBSimStatisticUtils.has_statistic(sim_info, BBSPrologueStatisticId.PROLOGUE_STAGE):
            return -1
        return int(BBSimStatisticUtils.get_statistic_value(sim_info, BBSPrologueStatisticId.PROLOGUE_STAGE))

    def get_sim_running_prologue(self) -> SimInfo:
        for sim_info in BBSimUtils.get_all_sim_info_gen():
            if BBSimTraitUtils.has_trait(sim_info, BBSPrologueTraitId.RUNNING_PROLOGUE):
                return sim_info

    def advance_prologue_stage(self, sim_info: SimInfo):
        current_prologue_stage = self.get_prologue_stage(sim_info)
        if current_prologue_stage == -1:
            current_prologue_stage = 0

        if current_prologue_stage == 0:
            BBNotification(
                ModIdentity(),
                BBLocalizedStringData('Bad News'),
                BBLocalizedStringData('Bad news on the television, sounds like trouble. I should wait for the next broadcast and watch again.')
            ).show()
        elif current_prologue_stage == 1:
            BBNotification(
                ModIdentity(),
                BBLocalizedStringData('Really Bad News'),
                BBLocalizedStringData('The trouble got a whole lot worse! I should wait for the next broadcast and watch again.')
            ).show()
        elif current_prologue_stage == 2:
            BBNotification(
                ModIdentity(),
                BBLocalizedStringData('Really Really Bad News'),
                BBLocalizedStringData('The television is telling me to prepare for the apocolypse. I should wait for the next broadcast and watch again.')
            ).show()
        elif current_prologue_stage == 3:
            BBNotification(
                ModIdentity(),
                BBLocalizedStringData('Worse News'),
                BBLocalizedStringData('The news caster is freaking out. Telling Sims to stay indoors. I should wait for the next broadcast and watch again.')
            ).show()
        elif current_prologue_stage == 4:
            BBNotification(
                ModIdentity(),
                BBLocalizedStringData('Worst News'),
                BBLocalizedStringData('The television cuts out in the middle of the broadcast. The power and water also went out! I dont think there will be anymore broadcasts. (BB Survival has begun)')
            ).show()

        next_prologue_stage = current_prologue_stage + 1
        if next_prologue_stage >= 5:
            self.complete_prologue(sim_info)
            return
        BBSimStatisticUtils.set_statistic_value(sim_info, BBSPrologueStatisticId.PROLOGUE_STAGE, next_prologue_stage)

    def complete_prologue(self, sim_info: SimInfo):
        self.set_mod_fully_active()


@Command(
    'bbs.activate',
    command_type=CommandType.Live
)
def _bbs_command_activate(_connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    try:
        output('Activating BB Survival')
        BBSPrologueData().set_mod_fully_active()
        output('Done')
    except Exception as ex:
        output(f'An error occurred {ex}')
        log = BBLogRegistry().register_log(ModIdentity(), 'bbs_prologue')
        log.error('An error occurred while activating BBS', exception=ex)
