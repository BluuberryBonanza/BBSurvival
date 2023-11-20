"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Callable, Tuple

from bbsurvival.bb_lib.dialog.picker_rows.bb_sim_picker_row import BBSimPickerRow
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4.commands import Command, CommandType
from ui.ui_dialog_picker import UiSimPicker


class BBSimDialog:
    """BBSimDialog(\
        mod_identity,\
        title,\
        description,\
        rows,\
        min_required_choices=1,\
        max_allowed_choices=1\
    )

    A dialog for displaying Sims to choose from.

    :param mod_identity: The identity of the mod that owns this dialog.
    :type mod_identity: BBModIdentity
    :param title: The title to show in the dialog.
    :type title: BBLocalizedStringData
    :param description: The description to show in the dialog.
    :type description: BBLocalizedStringData
    :param rows: The rows to display in the dialog.
    :type rows: Tuple[BBSimPickerRow]
    :param min_required_choices: The number of Sims required to be chosen to submit the dialog. Default is 1. If a value above "max_allowed_choices" is specified, then this value will be "max_allowed_choices".
    :type min_required_choices: int, optional
    :param max_allowed_choices: The maximum number of Sims allowed to be chosen within the dialog. Default is 1.
    :type max_allowed_choices: int, optional
    """
    def __init__(
        self,
        mod_identity: BBModIdentity,
        title: BBLocalizedStringData,
        description: BBLocalizedStringData,
        rows: Tuple[BBSimPickerRow],
        min_required_choices: int = 1,
        max_allowed_choices: int = 1
    ):
        self._mod_identity = mod_identity
        self._title = title.localize()
        self._description = description.localize()
        self._rows = rows
        self._min_required_choices = min_required_choices if min_required_choices <= max_allowed_choices else max_allowed_choices
        self._max_allowed_choices = max_allowed_choices

    @property
    def mod_identity(self) -> BBModIdentity:
        return self._mod_identity

    @property
    def title(self) -> LocalizedString:
        return self._title

    @property
    def description(self) -> LocalizedString:
        return self._description

    def display(
        self,
        owning_sim_info: SimInfo,
        on_submit: Callable[[Tuple[SimInfo]], None],
        on_closed: Callable[[], None] = None
    ):
        _log = BBLogRegistry().register_log(self.mod_identity, 'bb_sim_dialog')
        try:
            if len(self._rows) == 0:
                raise AssertionError('No Rows specified for the Sim dialog to display!')

            # noinspection PyBroadException
            def _on_submit(_dialog: UiSimPicker) -> None:
                if not _dialog.accepted:
                    if on_closed is not None:
                        on_closed()
                    return
                # noinspection PyTypeChecker
                chosen: Tuple[SimInfo] = tuple([BBSimUtils.to_sim_info(_sim_id) for _sim_id in _dialog.get_result_tags()])
                on_submit(chosen)

            dialog = UiSimPicker.TunableFactory().default(
                owning_sim_info,
                title=lambda *_, **__: self.title,
                text=lambda *_, **__: self.description,
                min_selectable=self._min_required_choices,
                max_selectable=self._max_allowed_choices,
                should_show_names=True,
                hide_row_description=False,
                column_count=3
            )

            for row in self._rows:
                dialog.add_row(row.to_picker_row())

            dialog.add_listener(_on_submit)
            dialog.show_dialog()
        except Exception as ex:
            _log.error('An error occurred while displaying Sim dialog.', exception=ex)


@Command(
    'bbl.show_sim_dialog',
    command_type=CommandType.Live
)
def _bbl_show_sim_dialog(_connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    output('Showing Sim dialog.')

    try:
        sim_rows = list()
        for sim_info in BBSimUtils.get_all_sim_info_gen():
            sim_rows.append(
                BBSimPickerRow(
                    sim_info,
                )
            )

        active_sim_info = BBSimUtils.get_active_sim_info()

        def _on_submit(values: Tuple[SimInfo]):
            output('Got the values!')
            for _sim_info in values:
                output(f'Got {_sim_info}')

        def _on_closed():
            output('Dialog was closed!')

        BBSimDialog(
            ModIdentity(),
            BBLocalizedStringData('I am the title of the dialog.'),
            BBLocalizedStringData('I am the description of the dialog.'),
            tuple(sim_rows),
            min_required_choices=2,
            max_allowed_choices=3
        ).display(active_sim_info, _on_submit, on_closed=_on_closed)
    except Exception as ex:
        output('An error occurred!')
        log = BBLogRegistry().register_log(ModIdentity(), 'bbl_sim_dialog')
        log.error('Something broke', exception=ex)

    output('Done showing dialog.')
