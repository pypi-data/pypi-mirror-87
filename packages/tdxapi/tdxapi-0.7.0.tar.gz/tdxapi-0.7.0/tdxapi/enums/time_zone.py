from enum import Enum


class TimeZone(Enum):
    """Time zones tracked within TeamDynamix."""

    __tdx_type__ = None

    DEFAULT = 0
    ALASKA = 1
    EASTERN = 2
    HAWAII = 3
    CENTRAL = 4
    MOUNTAIN = 5
    PACIFIC = 6
    GMT_EUROPE = 7
    CENTRAL_EUROPEAN = 8
    ARABIA = 9
    ARIZONA = 10
    INDIANA_EAST = 11
    ATLANTIC = 12
    WESTERN_EUROPE = 13
    EASTERN_EUROPE = 14
    WESTERN_AUSTRALIA = 15
    NORTHERN_TERRITORY = 16
    SOUTH_AUSTRALIA = 17
    NEW_SOUTH_WALES = 18
    VICTORIA = 19
    QUEENSLAND = 20
    ACT = 21
    TASMANIA = 22
    SASKATCHEWAN = 25
    NEWFOUNDLAND = 29
    GULF = 43
    PAKISTAN = 44
    AFGHANISTAN = 62
