"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.mod_identity import ModIdentity
from bbsurvival.prologue.bbs_prologue_data import BBSPrologueData
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from careers.school.school_tuning import SchoolTuning
from sims.sim_info import SimInfo


class BBSSchoolTuningOverride:
    @staticmethod
    def remove_school_data(sim_info: SimInfo, school_tuning: SchoolTuning):
        for (_school_age, _school_data) in school_tuning.school_data.items():
            _school_career_type = _school_data.school_career
            sim_info.career_tracker.remove_career(_school_career_type.guid64, post_quit_msg=False)

@BBInjectionUtils.inject(ModIdentity(), SchoolTuning, SchoolTuning.update_school_data.__name__)
def _bbs_override_school_tuning_update_school_data(original, self, sim_info, *_, **__):
    if not BBSPrologueData().is_mod_fully_active():
        def _create_on_activate(_sim_info: SimInfo, school_tuning: SchoolTuning):
            def _on_activate():
                BBSSchoolTuningOverride.remove_school_data(_sim_info, school_tuning)

            return _on_activate
        BBSPrologueData().register_on_activate(_create_on_activate(sim_info, self))
        return original(self, sim_info, *_, **__)

    BBSSchoolTuningOverride.remove_school_data(sim_info, self)