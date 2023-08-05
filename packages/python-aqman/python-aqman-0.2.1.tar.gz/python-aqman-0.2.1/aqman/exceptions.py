"""Exceptions for AQMAN101 from RadonFTLabs"""


class AqmanError(Exception):
    """Generic Aqman Exception"""
    pass


class AqmanConnectionError(AqmanError):
    """Aqman connection Exception"""
    pass
