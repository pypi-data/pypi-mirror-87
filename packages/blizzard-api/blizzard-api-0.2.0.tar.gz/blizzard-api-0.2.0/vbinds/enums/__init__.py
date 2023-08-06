
"""
vbinds - Useful enumeration definitions.
"""

# built-in
from enum import Enum


class Region(Enum):
    """
    See "Regions" table at:
    https://develop.battle.net/documentation/guides/regionality-partitions-and-localization
    """

    US = "us"
    EU = "eu"
    KR = "kr"
    TW = "tw"
    CN = "cn"


class Locale(Enum):
    """
    See "Region Host List" table at:
    https://develop.battle.net/documentation/guides/regionality-partitions-and-localization
    """

    # US
    en_US = "en_US"
    es_MX = "es_MX"
    pt_BR = "pt_BR"

    # Europe
    en_GB = "en_GB"
    es_ES = "es_ES"
    fr_FR = "fr_FR"
    ru_RU = "ru_RU"
    de_DE = "de_DE"
    pt_PT = "pt_PT"
    it_IT = "it_IT"

    # Korea
    ko_KR = "ko_KR"

    # Taiwan
    zh_TW = "zh_TW"

    # China
    zh_CN = "zh_CN"


class Namespace(Enum):
    """
    See "World of Warcraft Namespaces" table at:
    https://develop.battle.net/documentation/guides/game-data-apis-wow-namespaces
    """

    Static = "static-{}"
    Dynamic = "dynamic-{}"
    Profile = "profile-{}"


def get_query_str(region: Region, query_str: str) -> str:
    """ Build a query URL based on the region and the query sub-String. """

    query_format_str = "https://gateway.battlenet.com.{0}/{1}"
    if Region != Region.CN:
        query_format_str = "https://{0}.api.blizzard.com/{1}"
    return query_format_str.format(region.value, query_str)


def get_namespace_str(namespace: Namespace, region: Region):
    """ Get a fully-qualified namespace String. """

    return namespace.value.format(region.value)


class IconSize(Enum):
    """
    Required parameter for retrieving in-game icons. See:
    https://us.battle.net/forums/en/bnet/topic/20755767469
    """

    SMALL = 18
    MEDIUM = 36
    LARGE = 56


def get_icon_url(name: str, size: IconSize):
    """ Get the web-url for a named icon. """

    file_name = "{}.jpg".format(name)
    icon_url_fmt = "http://media.blizzard.com/wow/icons/{}/{}"
    return icon_url_fmt.format(str(size.value), file_name)
