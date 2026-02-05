"""
JBL AV Receiver configuration for Unfolded Circle integration.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

from dataclasses import dataclass
from ucapi_framework import BaseConfigManager


@dataclass
class JBLAVConfig:
    """JBL AV Receiver configuration."""

    identifier: str
    name: str
    host: str
    port: int = 50000


class JBLAVConfigManager(BaseConfigManager[JBLAVConfig]):
    """Configuration manager with automatic JSON persistence."""

    pass
