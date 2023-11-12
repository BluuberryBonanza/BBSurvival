"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Callable, Dict

from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4.commands import Command, CommandType
from ui.ui_dialog import ButtonType, UiDialogOkCancel


class BBOkCancelDialog:
    """BBOkCancelDialog(\
        mod_identity,\
        title,\
        description,\
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
        subtitle: BBLocalizedStringData = BBLocalizedStringData(0),
        ok_text: BBLocalizedStringData = BBLocalizedStringData(3648501874),
        cancel_text: BBLocalizedStringData = BBLocalizedStringData(3497542682),
    ):
        self._mod_identity = mod_identity
        self._title = title.localize()
        self._description = description.localize()
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
        on_ok: Callable[[], None],
        on_cancel: Callable[[], None],
        on_closed: Callable[[], None] = None
    ):
        """display(owning_sim_info, on_ok, on_cancel, on_closed=None)

        Display the dialog to the Player.

        :param owning_sim_info: The Sim that owns the dialog.
        :type owning_sim_info: SimInfo
        :param on_ok: What to do when the Ok button is chosen.
        :type on_ok: Callable[[Dict[str, Any]], None]
        :param on_cancel: What to do when the cancel button is chosen.
        :type on_cancel: Callable[[], None]
        :param on_closed: What to do when the dialog is closed. Default is no behavior.
        :type on_closed: Callable[[], None], optional
        """
        _log = BBLogRegistry().register_log(self.mod_identity, 'bb_input_integer_dialog')
        try:
            dialog = UiDialogOkCancel.TunableFactory().default(
                owning_sim_info,
                text=lambda *_, **__: self.description,
                title=lambda *_, **__: self.title,
                subtitle=lambda *_, **__: self._subtitle,
                text_ok=lambda *_, **__: self._ok_text,
                text_cancel=lambda *_, **__: self._cancel_text,
            )

            # noinspection PyBroadException
            def _on_submit(_dialog: UiDialogOkCancel) -> None:
                try:
                    if _dialog.response == ButtonType.DIALOG_RESPONSE_CLOSED:
                        if on_closed is not None:
                            on_closed()
                        return
                    if not _dialog.accepted:
                        on_cancel()
                        return
                    on_ok()
                except Exception as _ex:
                    _log.error('Error happened on submit.', exception=_ex)

            dialog.add_listener(_on_submit)
            dialog.show_dialog()
        except Exception as ex:
            _log.error('An error occurred while displaying ok/cancel dialog.', exception=ex)


@Command(
    'bbl.show_ok_cancel_dialog',
    command_type=CommandType.Live
)
def _bbl_show_ok_cancel_dialog(_connection: int = None):
    from sims4.commands import CheatOutput
    output = CheatOutput(_connection)
    output('Showing ok/cancel dialog.')

    try:
        active_sim_info = BBSimUtils.get_active_sim_info()

        def _on_ok():
            output('Dialog was Ok!')

        def _on_cancel():
            output('Dialog was cancelled!')

        def _on_closed():
            output('Dialog was closed!')

        BBOkCancelDialog(
            ModIdentity(),
            BBLocalizedStringData('I am the title of the dialog.'),
            BBLocalizedStringData('I am the description of the dialog.'),
            subtitle=BBLocalizedStringData('I am a subtitle'),
            ok_text=BBLocalizedStringData('I am the ok'),
            cancel_text=BBLocalizedStringData('I am the cancel')
        ).display(active_sim_info, _on_ok, _on_cancel, on_closed=_on_closed)
    except Exception as ex:
        output('An error occurred!')
        log = BBLogRegistry().register_log(ModIdentity(), 'bbl_ok_cancel_dialog')
        log.error('Something broke', exception=ex)

    output('Done showing dialog.')
