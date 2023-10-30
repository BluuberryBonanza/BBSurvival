from typing import TypeVar

from bluuberrylibrary.enums.classes.bb_int_flags import BBIntFlags
from enum import IntFlags

BBFlagsType = TypeVar('BBFlagsType', int, BBIntFlags, IntFlags)


class BBBitwiseUtils:
    """Utilities for performing bitwise operations. (Without having to think about it)"""
    @classmethod
    def add_bits(cls, original_bits: BBFlagsType, to_add_bits: BBFlagsType) -> BBFlagsType:
        """add_bits(original_bits, to_add_bits)

        Add bit flags to an existing set of bit flags.

        :param original_bits: The original bits to add to.
        :type original_bits: BBFlagsType
        :param to_add_bits: The bits being added.
        :type to_add_bits: BBFlagsType
        :return: The original bits with the "to add" bits added.
        :rtype: BBFlagsType
        """
        return original_bits | to_add_bits

    @classmethod
    def remove_bits(cls, original_bits: BBFlagsType, to_remove_bits: BBFlagsType) -> BBFlagsType:
        """remove_bits(original_bits, to_remove_bits)

        Remove bit flags from an existing set of bit flags.

        :param original_bits: The original bits to remove from.
        :type original_bits: BBFlagsType
        :param to_remove_bits: The bits being removed.
        :type to_remove_bits: BBFlagsType
        :return: The original bits with the "to remove" bits removed.
        :rtype: BBFlagsType
        """
        return original_bits & ~to_remove_bits

    @classmethod
    def has_all_bits(cls, original_bits: BBFlagsType, to_check_bits: BBFlagsType) -> bool:
        """has_all_bits(original_bits, to_check_bits)

        Check if all bits exist within a set of bits.

        :param original_bits: The bits to check.
        :type original_bits: BBFlagsType
        :param to_check_bits: The bits to check for.
        :type to_check_bits: BBFlagsType
        :return: True, if the original bits contains all the "to check" bits. False, if some or all the "to check" bits were not found.
        :rtype: bool
        """
        return original_bits == (original_bits & to_check_bits)

    @classmethod
    def has_any_bits(cls, original_bits: BBFlagsType, to_check_bits: BBFlagsType) -> bool:
        """has_any_bits(original_bits, to_check_bits)

        Check if any bits exist within a set of bits.

        :param original_bits: The bits to check.
        :type original_bits: BBFlagsType
        :param to_check_bits: The bits to check for.
        :type to_check_bits: BBFlagsType
        :return: True, if the original bits contains any of the "to check" bits. False, if all the "to check" bits were not found.
        :rtype: bool
        """
        return (original_bits & to_check_bits) != 0
