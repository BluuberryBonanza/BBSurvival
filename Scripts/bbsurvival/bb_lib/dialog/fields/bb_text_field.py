"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Iterable, Any

from bbsurvival.bb_lib.dialog.bb_character_restrictions import BBCharacterRestriction
from bluuberrylibrary.utils.text.bb_localization_utils import BBLocalizationUtils
from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from bluuberrylibrary.utils.text.bb_localized_tooltip_data import BBLocalizedTooltipData


class BBTextField:
    """BBTextField(\
        identifier,\
        initial_value,\
        title=None,\
        character_restriction=BBCharacterRestriction.NONE,\
        default_text=None,\
        min_value=None,\
        max_value=None,\
        min_length=None,\
        max_length=20,\
        input_too_short_tooltip=None,\
        input_too_small_tooltip=None,\
        input_too_big_tooltip=None,\
        check_profanity=False,\
        height=None\
    )

    A field used in dialogs that display text fields.

    :param identifier: This identifies the text field.
    :type identifier: str
    :param initial_value: The initial value to display in the dialog. Default is empty string.
    :type initial_value: str, optional
    :param title: The localization data for the title. Default is no title.
    :type title: BBLocalizedStringData, optional
    :param character_restriction: Restrictions on the characters that can be used in the dialog. Default is no restrictions.
    :type character_restriction: BBCharacterRestriction, optional
    :param default_text: Placeholder text to show in the field when no text is entered. Default is no placeholder text.
    :type default_text: BBLocalizedStringData, optional
    :param min_value: The minimum allowed value. This is useful when the text is a number. Default is no minimum.
    :type min_value: int, optional
    :param max_value: The maximum allowed value. This is useful when the text is a number. Default is no maximum.
    :type max_value: int, optional
    :param min_length: The minimum length the text must be to be valid. Default is no minimum length.
    :type min_length: int, optional
    :param max_length: The maximum length the text is allowed, to be valid. Default is a max of 20 characters in length.
    :type max_length: int, optional
    :param input_too_short_tooltip: A tooltip shown when the entered text is too short. Default is no tooltip.
    :type input_too_short_tooltip: BBLocalizedTooltipData, optional
    :param input_too_small_tooltip: A tooltip shown when the entered number is below the min_value. Default is no tooltip.
    :type input_too_small_tooltip: BBLocalizedTooltipData, optional
    :param input_too_big_tooltip: A tooltip shown when the entered number is above the max_value. Default is no tooltip.
    :type input_too_big_tooltip: BBLocalizedTooltipData, optional
    :param check_profanity: Set True, if the text should be checked for profanity. Set False, to ignore profanity. Default is False.
    :type check_profanity: bool, optional
    :param height: The height is the number of pixels added to the height of a single line of text in the UI. Default is the default height.
    :type height: int, optional
    """
    def __init__(
        self,
        identifier: str,
        initial_value: str = None,
        title: BBLocalizedStringData = None,
        character_restriction: BBCharacterRestriction = BBCharacterRestriction.NONE,
        default_text: BBLocalizedStringData = None,
        min_value: int = None,
        max_value: int = None,
        min_length: int = None,
        max_length: int = 20,
        input_too_short_tooltip: BBLocalizedTooltipData = None,
        input_too_small_tooltip: BBLocalizedTooltipData = None,
        input_too_big_tooltip: BBLocalizedTooltipData = None,
        check_profanity: bool = False,
        height: int = None
    ):
        self._identifier = identifier
        self.initial_value = initial_value
        if initial_value is None:
            initial_value = ''
        self.initial_value_text = BBLocalizedStringData(initial_value)
        self.title = title
        self.character_restriction = character_restriction
        self.default_text = default_text
        self.max_length = max_length
        self.min_length = min_length
        self.min_value = min_value
        self.max_value = max_value
        self.invalid_max_tooltip = input_too_big_tooltip
        self.invalid_min_tooltip = input_too_small_tooltip
        self.input_too_short_tooltip = input_too_short_tooltip
        self.check_profanity = check_profanity
        self.height = height

    # noinspection PyMissingOrEmptyDocstring
    @property
    def identifier(self) -> str:
        return self._identifier

    def parse_value(self, value: str) -> str:
        """parse_value(value)

        When this input field has its value submitted, this will convert the value to the expected type for the field.

        :param value: The value to parse.
        :type value: str
        :return: The result of the parse.
        :rtype: str
        """
        return value

    def build_msg(
        self,
        msg,
        additional_tokens: Iterable[Any] = ()
    ):
        text_input_msg = msg.text_input.add()
        text_input_msg.text_input_name = self.identifier
        if self.initial_value_text is not None:
            text_input_msg.initial_value = self.initial_value_text.localize(additional_tokens=additional_tokens)
        if self.default_text is not None:
            text_input_msg.default_text = self.default_text.localize(additional_tokens=additional_tokens)
        if self.title:
            text_input_msg.title = self.title.localize(additional_tokens=additional_tokens)
        if self.character_restriction is not None and self.character_restriction != BBCharacterRestriction.NONE:
            text_input_msg.restricted_characters = BBLocalizationUtils.to_localized_string(BBCharacterRestriction.get_display_string_id(self.character_restriction))
        if self.max_value is not None:
            text_input_msg.max_value = self.max_value
            if self.invalid_max_tooltip is not None:
                text_input_msg.input_invalid_max_tooltip = self.invalid_max_tooltip.localize(additional_tokens=(self.title.localize(additional_tokens=additional_tokens), *additional_tokens) if self.title else additional_tokens)()
        if self.min_value is not None:
            text_input_msg.min_value = self.min_value
            if self.invalid_min_tooltip is not None:
                text_input_msg.input_invalid_min_tooltip = self.invalid_min_tooltip.localize(additional_tokens=(self.title.localize(additional_tokens=additional_tokens), *additional_tokens) if self.title else additional_tokens)()
        text_input_msg.check_profanity = self.check_profanity

        if self.max_length is not None:
            text_input_msg.max_length = self.max_length
        if self.min_length is not None:
            text_input_msg.min_length = self.min_length
            if self.input_too_short_tooltip is not None:
                text_input_msg.input_too_short_tooltip = self.input_too_short_tooltip.localize(additional_tokens=(self.title.localize(additional_tokens=additional_tokens), *additional_tokens) if self.title else additional_tokens)()

        text_input_msg.height = self.height if self.height is not None else -1
