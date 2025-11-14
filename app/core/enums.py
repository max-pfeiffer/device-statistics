"""Enums."""

from enum import Enum


class DeviceType(str, Enum):
    """Device type enum."""

    IOS = "iOS"
    ANDROID = "Android"
    WATCH = "Watch"
    TV = "TV"
