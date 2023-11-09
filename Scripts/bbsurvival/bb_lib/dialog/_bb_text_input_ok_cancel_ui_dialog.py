"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any, Iterable, Callable

from bbsurvival.bb_lib.dialog.fields.bb_text_field import BBTextField
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from ui.ui_dialog_generic import UiDialogTextInputOkCancel


class _BBTextInputOkCancelUiDialog(UiDialogTextInputOkCancel):
    def __init__(
        self,
        sim_info: SimInfo,
        text_fields: Iterable[BBTextField],
        *args,
        title: Callable[..., LocalizedString] = None,
        text: Callable[..., LocalizedString] = None,
        **kwargs
    ):
        super().__init__(
            sim_info,
            *args,
            title=title,
            text=text,
            **kwargs
        )
        self.text_fields = text_fields
        self.text_input_responses = {}

    def on_text_input(self, text_input_name: str = '', text_input: str = '') -> bool:
        for text_field in self.text_fields:
            if text_field.identifier == text_input_name:
                self.text_input_responses[text_input_name] = text_field.parse_value(text_input)
        return False

    def build_msg(self, text_input_overrides=None, additional_tokens: Iterable[Any] = (), **kwargs):
        msg = super().build_msg(additional_tokens=(), **kwargs)
        for text_field in self.text_fields:
            if text_field.initial_value is not None and text_field.initial_value != '':
                self.text_input_responses[text_field.identifier] = text_field.initial_value
            text_field.build_msg(
                msg
            )
        return msg
