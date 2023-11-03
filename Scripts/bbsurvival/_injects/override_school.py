"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bbsurvival.mod_identity import ModIdentity
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from careers.school.school_tuning import SchoolTuning


@BBInjectionUtils.inject(ModIdentity(), SchoolTuning, SchoolTuning.update_school_data.__name__)
def _bbs_override_school_tuning_update_school_data(original, self, sim_info, *_, **__):
    for (school_age, school_data) in self.school_data.items():
        school_career_type = school_data.school_career
        sim_info.career_tracker.remove_career(school_career_type.guid64, post_quit_msg=False)