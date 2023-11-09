"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Callable, Iterable, Dict, Any

from bbsurvival.bb_lib.dialog._bb_text_input_ok_cancel_ui_dialog import _BBTextInputOkCancelUiDialog
from bbsurvival.bb_lib.dialog.fields.bb_integer_field import BBIntegerField
from bbsurvival.bb_lib.dialog.fields.bb_text_field import BBTextField
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


class BBInputDialog:
    """BBInputDialog(\
        mod_identity,\
        title,\
        description,\
        input_fields,\
        subtitle=BBLocalizedStringData(0),\
        cancel_text=BBLocalizedStringData(3497542682),\
        ok_text=BBLocalizedStringData(3648501874)\
    )

    A dialog for displaying input fields for the Player to enter data into.

    :param mod_identity: The identity of the mod that owns this dialog.
    :type mod_identity: BBModIdentity
    :param title: The title to show in the dialog.
    :type title: BBLocalizedStringData
    :param description: The description to show in the dialog.
    :type description: BBLocalizedStringData
    :param input_fields: The inputs to display in the dialog.
    :type input_fields: Iterable[BBTextField]
    :param subtitle: A subtitle to display below the normal title. Default is no subtitle.
    :type subtitle: BBLocalizedStringData, optional
    :param ok_text: The text to show on the Ok button. Default is "Ok".
    :type ok_text: BBLocalizedStringData, optional
    :param cancel_text: The text to show on the Cancel button. Default is "Cancel".
    :type cancel_text: BBLocalizedStringData, optional
    """
    def __init__(
        self,
        mod_identity: BBModIdentity,
        title: BBLocalizedStringData,
        description: BBLocalizedStringData,
        input_fields: Iterable[BBTextField],
        subtitle: BBLocalizedStringData = BBLocalizedStringData(0),
        ok_text: BBLocalizedStringData = BBLocalizedStringData(3648501874),
        cancel_text: BBLocalizedStringData = BBLocalizedStringData(3497542682),
    ):
        self._mod_identity = mod_identity
        self._title = title.localize()
        self._description = description.localize()
        self.input_fields = tuple(input_fields)
        self._subtitle = subtitle.localize()
        self._ok_text = ok_text.localize()
        self._cancel_text = cancel_text.localize()

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
        on_submit: Callable[[Dict[str, Any]], None],
        on_cancel: Callable[[], None],
        on_closed: Callable[[], None] = None
    ):
        """display(owning_sim_info, on_submit, on_cancel, on_closed=None)

        Display the dialog to the Player.

        :param owning_sim_info: The Sim that owns the dialog.
        :type owning_sim_info: SimInfo
        :param on_submit: What to do when the dialog is submitted.
        :type on_submit: Callable[[Dict[str, Any]], None]
        :param on_cancel: What to do when the dialog is cancelled or closed.
        :type on_cancel: Callable[[], None]
        :param on_closed: What to do when the dialog is closed. Default is the on_cancel behavior.
        :type on_closed: Callable[[], None], optional
        """
        if on_closed is None:
            on_closed = on_cancel
        _log = BBLogRegistry().register_log(self.mod_identity, 'bb_input_integer_dialog')
        try:
            dialog = _BBTextInputOkCancelUiDialog.TunableFactory().default(
                owning_sim_info,
                self.input_fields,
                text=lambda *_, **__: self.description,
                title=lambda *_, **__: self.title,
                subtitle=lambda *_, **__: self._subtitle,
                text_ok=lambda *_, **__: self._ok_text,
                text_cancel=lambda *_, **__: self._cancel_text,
            )

            # noinspection PyBroadException
            def _on_submit(_dialog: _BBTextInputOkCancelUiDialog) -> None:
                try:
                    input_values = dict(_dialog.text_input_responses)
                    if _dialog.response == ButtonType.DIALOG_RESPONSE_CLOSED:
                        on_closed()
                        return
                    if not input_values or not _dialog.accepted:
                        on_cancel()
                        return
                    on_submit(input_values)
                except Exception as _ex:
                    _log.error('Error happened on submit.', exception=_ex)

            dialog.add_listener(_on_submit)
            if self.input_fields is not None:
                dialog.show_dialog(additional_tokens=tuple([input_field.initial_value for input_field in self.input_fields]))
            else:
                dialog.show_dialog()
        except Exception as ex:
            _log.error('An error occurred while displaying input dialog.', exception=ex)


@Command(
    'bbl.show_input_dialog',
    command_type=CommandType.Live
)
def _bbl_show_input_dialog(_connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    output('Showing input dialog.')

    try:
        input_fields = (
            BBIntegerField(
                'field_one',
                BBLocalizedStringData('I am field one'),
                24,
                min_value=-2,
                max_value=200,
                default_text=BBLocalizedStringData('I am the default text'),
                input_too_short_tooltip=BBLocalizedTooltipData('The input is too short "I am field one"!'),
                input_too_small_tooltip=BBLocalizedTooltipData('The input is too small "I am field one"!'),
                input_too_big_tooltip=BBLocalizedTooltipData('The input is too big "I am field one"!')
            ),
            BBIntegerField(
                'field_two',
                BBLocalizedStringData('I am field two'),
                50,
                min_value=5,
                max_value=100,
                default_text=BBLocalizedStringData('I am the default text for second field'),
                input_too_short_tooltip=BBLocalizedTooltipData('The input is too short "I am field two"!'),
                input_too_small_tooltip=BBLocalizedTooltipData('The input is too small "I am field two"!'),
                input_too_big_tooltip=BBLocalizedTooltipData('The input is too big "I am field two"!')
            ),
        )

        active_sim_info = BBSimUtils.get_active_sim_info()

        def _on_submit(values: Dict[str, int]):
            output('Got the values!')
            for (field_name, value) in values.items():
                output(f'Got {value} for {field_name}')

        def _on_cancel():
            output('Dialog was cancelled!')

        def _on_closed():
            output('Dialog was closed!')

        BBInputDialog(
            ModIdentity(),
            BBLocalizedStringData('I am the title of the dialog.'),
            BBLocalizedStringData('I am the description of the dialog.'),
            input_fields,
            subtitle=BBLocalizedStringData('I am a subtitle'),
            ok_text=BBLocalizedStringData('I am the ok'),
            cancel_text=BBLocalizedStringData('I am the cancel')
        ).display(active_sim_info, _on_submit, _on_cancel, on_closed=_on_closed)
    except Exception as ex:
        output('An error occurred!')
        log = BBLogRegistry().register_log(ModIdentity(), 'bbl_input_integer_dialog')
        log.error('Something broke', exception=ex)

    output('Done showing dialog.')
