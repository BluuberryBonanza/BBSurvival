"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.bb_lib.utils.bb_zone_modifier_utils import BBZoneModifierUtils
from sims4.commands import CommandType, Command


@Command(
    'bbl.add_zone_modifier',
    command_type=CommandType.Live
)
def _bbl_command_add_zone_modifier(zone_modifier: int, zone_id: int = None, _connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    output(f'Adding Zone Modifier {zone_modifier} to Zone Id {zone_id}')
    BBZoneModifierUtils.add_zone_modifier(zone_id, zone_modifier)
