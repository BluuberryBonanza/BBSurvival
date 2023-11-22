"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Callable, TypeVar, Any

from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from ui.ui_dialog import UiDialogResponse, ButtonType

ButtonValueType = TypeVar('ButtonValueType', covariant=Any)


class BBButton:
    """BBButton(\
        identifier,\
        text,\
        on_chosen,\
        subtext=None,\
        disabled_text=None,\
        tooltip_text=None,\
    )

    A button used in dialogs.

    :param identifier: This identifies the button.
    :type identifier: int
    :param text: The localization data for the text.
    :type text: BBLocalizedStringData
    :param on_chosen: What to do when the button is chosen.
    :type on_chosen: Callable[[], None]
    :param subtext: The localization data for the sub text (Text that appears below the normal text). Default is no text.
    :type subtext: BBLocalizedStringData, optional
    :param disabled_text: The text to show when the button is disabled. If supplied, the button will be disabled. Default is no text.
    :type disabled_text: BBLocalizedStringData, optional
    :param tooltip_text: The text to show when the Player hovers over the button. Default is no text.
    :type tooltip_text: BBLocalizedStringData, optional
    """
    def __init__(
        self,
        identifier: int,
        text: BBLocalizedStringData,
        on_chosen: Callable[[ButtonValueType], None],
        value: ButtonValueType = None,
        subtext: BBLocalizedStringData = None,
        disabled_text: BBLocalizedStringData = None,
        tooltip_text: BBLocalizedStringData = None
    ):
        self._identifier = identifier
        self.text = text
        self._on_chosen = on_chosen
        self.dialog_response_id = ButtonType.DIALOG_RESPONSE_NO_RESPONSE
        self.subtext = subtext
        self.disabled_text = disabled_text
        self.tooltip_text = tooltip_text
        self.value = value

    # noinspection PyMissingOrEmptyDocstring
    @property
    def identifier(self) -> int:
        return self._identifier

    def on_chosen(self):
        self._on_chosen(self.value)

    def to_dialog_response(self) -> UiDialogResponse:
        return UiDialogResponse(
            dialog_response_id=self.identifier,
            text=lambda *_, **__: self.text.localize(additional_tokens=_),
            subtext=self.subtext.localize() if self.subtext is not None else None,
            disabled_text=self.disabled_text.localize() if self.disabled_text is not None else None,
            tooltip_text=(lambda *_, **__: self.tooltip_text.localize(additional_tokens=_)) if self.tooltip_text is not None else None
        )
