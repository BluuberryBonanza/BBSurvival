"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Callable, Iterable, Any

from bbsurvival.bb_lib.dialog._bb_button_ui_dialog import _BBButtonUiDialog
from bbsurvival.bb_lib.dialog.fields.bb_button import BBButton
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from bluuberrylibrary.utils.text.bb_localized_tooltip_data import BBLocalizedTooltipData
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4.commands import Command, CommandType
from ui.ui_dialog import ButtonType


class BBButtonDialog:
    """BBButtonDialog(\
        mod_identity,\
        title,\
        description,\
        buttons,\
    )

    A dialog for displaying buttons for the Player to click.

    :param mod_identity: The identity of the mod that owns this dialog.
    :type mod_identity: BBModIdentity
    :param title: The title to show in the dialog.
    :type title: BBLocalizedStringData
    :param description: The description to show in the dialog.
    :type description: BBLocalizedStringData
    :param buttons: The buttons to display in the dialog.
    :type buttons: Iterable[BBButton]
    """
    def __init__(
        self,
        mod_identity: BBModIdentity,
        title: BBLocalizedStringData,
        description: BBLocalizedStringData,
        buttons: Iterable[BBButton],
    ):
        self._mod_identity = mod_identity
        self._title = title.localize()
        self._description = description.localize()
        self.buttons = tuple(buttons)

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
        on_closed: Callable[[], None] = None
    ):
        """display(owning_sim_info, on_closed=None)

        Display the dialog to the Player.

        :param owning_sim_info: The Sim that owns the dialog.
        :type owning_sim_info: SimInfo
        :param on_closed: What to do when the dialog is closed. Default is no behavior.
        :type on_closed: Callable[[], None], optional
        """
        _log = BBLogRegistry().register_log(self.mod_identity, 'bb_button_dialog')
        try:
            dialog = _BBButtonUiDialog.TunableFactory().default(
                self.mod_identity,
                owning_sim_info,
                self.buttons,
                text=lambda *_, **__: self.description,
                title=lambda *_, **__: self.title,
            )

            # noinspection PyBroadException
            def _on_submit(_dialog: _BBButtonUiDialog) -> None:
                try:
                    if _dialog.response == ButtonType.DIALOG_RESPONSE_CLOSED:
                        on_closed()
                        return
                    chosen_button_id = _dialog.get_chosen_button()
                    if chosen_button_id is None:
                        if on_closed is not None:
                            on_closed()
                        return
                except Exception as _ex:
                    _log.error('Error happened on submit.', exception=_ex)

            dialog.add_listener(_on_submit)
            dialog.show_dialog()
        except Exception as ex:
            _log.error('An error occurred while displaying button dialog.', exception=ex)


@Command(
    'bbl.show_button_dialog',
    command_type=CommandType.Live
)
def _bbl_show_button_dialog(_connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    output('Showing button dialog.')

    def _on_button_chosen(_: Any):
        output(f'Submitted button {_}')

    try:
        buttons = (
            BBButton(
                1,
                BBLocalizedStringData('I am button one'),
                _on_button_chosen,
                value='one',
                subtext=BBLocalizedStringData('I am some subtext one'),
                tooltip_text=BBLocalizedStringData('I am button one tooltip')
            ),
            BBButton(
                2,
                BBLocalizedStringData('I am button two'),
                _on_button_chosen,
                value='two',
                subtext=BBLocalizedStringData('I am some subtext two'),
                tooltip_text=BBLocalizedStringData('I am button two tooltip')
            ),
            BBButton(
                3,
                BBLocalizedStringData('I am button three'),
                _on_button_chosen,
                value='three',
                subtext=BBLocalizedStringData('I am some subtext three'),
                tooltip_text=BBLocalizedStringData('I am button three tooltip'),
                disabled_text=BBLocalizedStringData('I am button three disabled text')
            )
        )

        active_sim_info = BBSimUtils.get_active_sim_info()

        def _on_closed():
            output('Dialog was closed!')

        BBButtonDialog(
            ModIdentity(),
            BBLocalizedStringData('I am the title of the dialog.'),
            BBLocalizedStringData('I am the description of the dialog.'),
            buttons
        ).display(active_sim_info, on_closed=_on_closed)
    except Exception as ex:
        output('An error occurred!')
        log = BBLogRegistry().register_log(ModIdentity(), 'bbl_button_dialog')
        log.error('Something broke', exception=ex)

    output('Done showing dialog.')
