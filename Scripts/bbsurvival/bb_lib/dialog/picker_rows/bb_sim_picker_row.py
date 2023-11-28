"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from sims.sim_info import SimInfo
from ui.ui_dialog_picker import SimPickerRow


class BBSimPickerRow:
    """BBSimPickerRow(\
        sim_info,\
        is_selected=False,\
        select_as_default=False,\
    )

    A row used in dialogs to display a Sim.

    :param sim_info: The info of a Sim.
    :type sim_info: SimInfo
    :param is_selected: If this Sim is selected initially. Default is False.
    :type is_selected: bool, optional
    :param select_as_default: If no Sims are chosen, this Sim will be chosen. Default is False.
    :type select_as_default: bool, optional
    """
    def __init__(
        self,
        sim_info: SimInfo,
        is_selected: bool = False,
        select_as_default: bool = False
    ):
        self.sim_info = sim_info
        self.is_selected = is_selected
        self.select_as_default = select_as_default

    def to_picker_row(self) -> SimPickerRow:
        return SimPickerRow(
            sim_id=BBSimUtils.to_sim_id(self.sim_info),
            tag=self.sim_info,
            select_default=self.select_as_default,
            is_selected=self.is_selected
        )
