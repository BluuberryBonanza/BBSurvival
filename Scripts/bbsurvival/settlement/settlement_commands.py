"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import services
from bbsurvival.bb_lib.utils.bb_instance_utils import BBInstanceUtils
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from drama_scheduler.stayover_drama_node import StayoverDramaNode
from event_testing.resolver import SingleSimResolver
from sims4.commands import CommandType, Command
from sims4.resources import Types

log = BBLogRegistry().register_log(ModIdentity(), 'bbs_settlement_commands')


@Command(
    'bbs.trigger_settler',
    command_type=CommandType.Live
)
def _bbs_command_trigger_settler(_connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    try:
        # all_sims = tuple(BBSimUtils.get_sim_info_manager().get_all())
        # chosen_sim_info = random.choice(all_sims)
        chosen_sim_info = BBSimUtils.get_active_sim_info()
        resolver = SingleSimResolver(chosen_sim_info)
        drama_node = BBInstanceUtils.get_instance(Types.DRAMA_NODE, 15988136587536259929, return_type=StayoverDramaNode)
        services.drama_scheduler_service().schedule_node(drama_node, resolver)
        output('Done')
    except Exception as ex:
        output('An error occurred.')
        log.error('Failed to trigger settler. Error occurred', exception=ex)
