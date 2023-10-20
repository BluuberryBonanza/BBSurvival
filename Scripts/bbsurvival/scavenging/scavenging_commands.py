"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.scavenging.bbs_scavenging_run_length import BBSScavengingRunLength
from bbsurvival.scavenging.scavenging_utils import BBSScavengingUtils
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from sims4.commands import CommandType, Command


@Command(
    'bbs.give_scavenge_rewards',
    command_type=CommandType.Live
)
def _bbs_command_give_scavenging_rewards(_connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    active_sim_info = BBSimUtils.get_active_sim_info()
    output('Giving Scavenge Rewards')
    BBSScavengingUtils.give_scavenge_rewards(active_sim_info, BBSScavengingRunLength.QUICK)
    output('Done')
