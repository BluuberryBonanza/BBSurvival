"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any, Callable, TypeVar

from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from ui.ui_dialog_picker import ObjectPickerRow

ValueType = TypeVar('ValueType', covariant=Any)


class BBValuePickerRow:
    """BBValuePickerRow(\
        identifier,\
        header,\
        description,\
        tooltip_text=None,\
        is_enabled=True,\
        is_selected=False\
    )

    A row used in dialogs to display a Value.

    :param identifier: This identifies the row.
    :type identifier: int
    :param value: A value to provide upon the row being chosen.
    :type value: ValueType
    :param header: The localization data for the heading.
    :type header: BBLocalizedStringData
    :param description: The localization data for the description.
    :type description: BBLocalizedStringData
    :param tooltip_text: The text to show when the Player hovers over the row. Default is no text.
    :type tooltip_text: BBLocalizedStringData, optional
    :param is_enabled: Set True to enable this row. Set False to disable this row. Default is True.
    :type is_enabled: bool, optional
    :param is_selected: Set True to select this row initially. Default is False.
    :type is_selected: bool, optional
    """
    def __init__(
        self,
        identifier: int,
        value: ValueType,
        header: BBLocalizedStringData,
        description: BBLocalizedStringData,
        tooltip_text: BBLocalizedStringData = None,
        is_enabled: bool = True,
        is_selected: bool = False
    ):
        self._identifier = identifier
        self.header = header
        self.description = description
        self.tooltip_text = tooltip_text
        self.value = value
        self.is_enabled = is_enabled
        self.is_selected = is_selected

    # noinspection PyMissingOrEmptyDocstring
    @property
    def identifier(self) -> int:
        return self._identifier

    def to_picker_row(self) -> ObjectPickerRow:
        return ObjectPickerRow(
            option_id=self._identifier,
            name=self.header.localize(),
            row_description=self.description.localize(),
            row_tooltip=lambda *_, **__: self.tooltip_text.localize(additional_tokens=_) if self.tooltip_text is not None else None,
            is_enable=self.is_enabled,
            is_selected=self.is_selected,
            tag=self.value
        )
