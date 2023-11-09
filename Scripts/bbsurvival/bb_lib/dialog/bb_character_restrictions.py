class BBCharacterRestriction:
    NONE = ...
    NUMBERS = ...

    @classmethod
    def get_display_string_id(cls, value: 'BBCharacterRestriction') -> int:
        if value == BBCharacterRestriction.NUMBERS:
            return 0x8FE40C44  # 0-9
        return 0
