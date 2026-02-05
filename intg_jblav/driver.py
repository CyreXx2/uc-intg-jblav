"""
JBL AV Receiver driver for Unfolded Circle Remote.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
from ucapi_framework import BaseIntegrationDriver
from intg_jblav.config import JBLAVConfig
from intg_jblav.device import JBLAV
from intg_jblav.media_player import JBLAVMediaPlayer
from intg_jblav.remote import JBLAVRemote
from intg_jblav.select import JBLAVInputSelect, JBLAVSurroundModeSelect
from intg_jblav.sensor import (
    JBLAVModelSensor,
    JBLAVVolumeSensor,
    JBLAVInputSensor,
    JBLAVSurroundModeSensor,
    JBLAVMutedSensor,
    JBLAVConnectionSensor,
)

_LOG = logging.getLogger(__name__)


class JBLAVDriver(BaseIntegrationDriver[JBLAV, JBLAVConfig]):
    """JBL AV Receiver integration driver."""

    def __init__(self):
        super().__init__(
            device_class=JBLAV,
            entity_classes=[
                JBLAVMediaPlayer,  # Media Player entity
                JBLAVRemote,  # Remote entity with comprehensive controls
                JBLAVInputSelect,  # Input source select
                JBLAVSurroundModeSelect,  # Surround mode select
                # Sensors (lambda for multiple sensor creation)
                lambda cfg, dev: [
                    JBLAVModelSensor(cfg, dev),
                    JBLAVVolumeSensor(cfg, dev),
                    JBLAVInputSensor(cfg, dev),
                    JBLAVSurroundModeSensor(cfg, dev),
                    JBLAVMutedSensor(cfg, dev),
                    JBLAVConnectionSensor(cfg, dev),
                ],
            ],
            driver_id="jblav",
        )
