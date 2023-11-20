"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.bb_lib.dialog.bb_character_restrictions import BBCharacterRestriction
from bbsurvival.bb_lib.dialog.fields.bb_text_field import BBTextField
from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from bluuberrylibrary.utils.text.bb_localized_tooltip_data import BBLocalizedTooltipData


class BBIntegerField(BBTextField):
    """BBIntegerField(\
        identifier,\
        title,\
        initial_value,\
        min_value=0,\
        max_value=2147483647,\
        character_restriction=BBCharacterRestriction.NUMBERS,\
        default_text=None,\
        min_length=None,\
        max_length=20,\
        input_too_short_tooltip=None,\
        input_too_small_tooltip=None,\
        input_too_big_tooltip=None,\
        height=None\
    )

    A field used in dialogs that display integer fields.

    :param identifier: This identifies the text field.
    :type identifier: str
    :param title: The localization data for the title.
    :type title: BBLocalizedStringData
    :param initial_value: The initial value to set the input field to.
    :type initial_value: int
    :param character_restriction: Restrictions on the characters that can be used in the dialog. Default is numbers restriction.
    :type character_restriction: BBCharacterRestriction, optional
    :param default_text: Placeholder text to show in the field when no number is entered. Default is no placeholder text.
    :type default_text: BBLocalizedStringData, optional
    :param min_value: The minimum allowed value. Default is 0.
    :type min_value: int, optional
    :param max_value: The maximum allowed value. Default is 2147483647.
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
    :param height: The height is the number of pixels added to the height of a single line of text in the UI. Default is the default height.
    :type height: int, optional
    """
    def __init__(
        self,
        identifier: str,
        title: BBLocalizedStringData,
        initial_value: int,
        min_value: int = 0,
        max_value: int = 2147483647,
        character_restriction: BBCharacterRestriction = BBCharacterRestriction.NUMBERS,
        default_text: BBLocalizedStringData = None,
        min_length: int = None,
        max_length: int = 20,
        input_too_short_tooltip: BBLocalizedTooltipData = None,
        input_too_small_tooltip: BBLocalizedTooltipData = None,
        input_too_big_tooltip: BBLocalizedTooltipData = None,
        height: int = None
    ):
        super().__init__(
            identifier,
            str(initial_value),
            title=title,
            character_restriction=character_restriction,
            default_text=default_text,
            min_value=min_value,
            max_value=max_value,
            min_length=min_length,
            max_length=max_length,
            input_too_short_tooltip=input_too_short_tooltip,
            input_too_small_tooltip=input_too_small_tooltip,
            input_too_big_tooltip=input_too_big_tooltip,
            check_profanity=False,
            height=height
        )
        self.initial_value = initial_value

    def parse_value(self, value: str) -> int:
        """parse_value(value)

        When this input field has its value submitted, this will convert the value to the expected type for the field.

        :param value: The value to parse.
        :type value: str
        :return: The result of the parse.
        :rtype: int
        """
        return int(value)
