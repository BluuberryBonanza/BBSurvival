"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from sims.sim_info import SimInfo
from sims.sim_info_types import Age


class BBSimAgeUtils:
    """Utilities for manipulating the Age of Sims."""
    @classmethod
    def is_baby(cls, sim_info: SimInfo) -> bool:
        return cls.get_age(sim_info) == Age.BABY

    @classmethod
    def is_infant(cls, sim_info: SimInfo) -> bool:
        return cls.get_age(sim_info) == Age.INFANT

    @classmethod
    def is_toddler(cls, sim_info: SimInfo) -> bool:
        return cls.get_age(sim_info) == Age.TODDLER

    @classmethod
    def is_child(cls, sim_info: SimInfo) -> bool:
        return cls.get_age(sim_info) == Age.CHILD

    @classmethod
    def is_teen(cls, sim_info: SimInfo) -> bool:
        return cls.get_age(sim_info) == Age.TEEN

    @classmethod
    def is_young_adult(cls, sim_info: SimInfo) -> bool:
        return cls.get_age(sim_info) == Age.YOUNGADULT

    @classmethod
    def is_adult(cls, sim_info: SimInfo) -> bool:
        return cls.get_age(sim_info) == Age.ADULT

    @classmethod
    def is_elder(cls, sim_info: SimInfo) -> bool:
        return cls.get_age(sim_info) == Age.ELDER

    @classmethod
    def get_age(cls, sim_info: SimInfo) -> Age:
        return sim_info.age
