"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Iterable, Callable, Union

from bbsurvival.bb_lib.dialog.fields.bb_button import BBButton
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from ui.ui_dialog import UiDialog


class _BBButtonUiDialog(UiDialog):

    def __init__(
        self,
        mod_identity: BBModIdentity,
        sim_info: SimInfo,
        buttons: Iterable[BBButton],
        *args,
        title: Callable[..., LocalizedString] = None,
        text: Callable[..., LocalizedString] = None,
        **kwargs
    ):
        if 'dialog_options' in kwargs:
            del kwargs['dialog_options']
        super().__init__(
            sim_info,
            *args,
            title=title,
            text=text,
            dialog_options=0,
            **kwargs
        )
        self.mod_identity = mod_identity
        self.buttons = buttons
        self._responses = tuple([button.to_dialog_response() for button in self.buttons])
        self._chosen_button = None

    @property
    def responses(self):
        return self._responses

    def get_chosen_button(self) -> Union[int, None]:
        return self._chosen_button

    def respond(self, chosen_button_id: int) -> bool:
        try:
            self.response = chosen_button_id
            if chosen_button_id < 0:
                self._chosen_button = None
            else:
                self._chosen_button = None
                for button in self.buttons:
                    if button.identifier == chosen_button_id:
                        self._chosen_button = button
                        self._chosen_button.on_chosen()
                        break
            if self.ui_responses:
                for ui_response in self.ui_responses:
                    if ui_response.dialog_response_id == self.response:
                        if ui_response.loots_for_response is None:
                            self.on_response_received()
                            return False
                        for loot_action in ui_response.loots_for_response:
                            loot_action.apply_to_resolver(self._resolver)
            self._listeners(self)
            return True
        except Exception as ex:
            from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
            _log = BBLogRegistry().register_log(self.mod_identity, 'bb_ui_button_dialog')
            _log.error('An error occurred while responding in the button dialog.', exception=ex)
            return False
