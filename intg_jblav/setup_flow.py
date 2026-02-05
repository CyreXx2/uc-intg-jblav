"""
JBL AV Receiver setup flow for Unfolded Circle integration.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import asyncio
import logging
from typing import Any
from ucapi import RequestUserInput
from ucapi_framework import BaseSetupFlow
from intg_jblav.config import JBLAVConfig
from intg_jblav.device import JBLAV

_LOG = logging.getLogger(__name__)


class JBLAVSetupFlow(BaseSetupFlow[JBLAVConfig]):
    """Setup flow for JBL AV Receiver integration."""

    def get_manual_entry_form(self) -> RequestUserInput:
        """Define manual entry fields."""
        return RequestUserInput(
            {"en": "JBL AV Receiver Setup"},
            [
                {
                    "id": "name",
                    "label": {"en": "Receiver Name"},
                    "field": {"text": {"value": ""}},
                },
                {
                    "id": "host",
                    "label": {"en": "IP Address"},
                    "field": {"text": {"value": ""}},
                },
                {
                    "id": "port",
                    "label": {"en": "Port"},
                    "field": {"text": {"value": "50000"}},
                },
            ]
        )

    async def query_device(
        self, input_values: dict[str, Any]
    ) -> JBLAVConfig | RequestUserInput:
        """
        Validate connection and create config.

        Called after user provides setup information.
        """
        host = input_values.get("host", "").strip()
        if not host:
            raise ValueError("IP address is required")

        port = int(input_values.get("port", 50000))
        name = input_values.get("name", f"JBL AV ({host})").strip()

        _LOG.info("Testing connection to JBL receiver at %s:%d", host, port)

        # Test connection
        try:
            test_config = JBLAVConfig(
                identifier=f"jblav_{host.replace('.', '_')}_{port}",
                name=name,
                host=host,
                port=port
            )

            # Quick connection test
            test_device = JBLAV(test_config)

            _LOG.info("Attempting to connect to receiver...")
            connected = await asyncio.wait_for(
                test_device.connect(),
                timeout=15.0
            )

            if not connected:
                raise ValueError(f"Failed to connect to receiver at {host}:{port}")

            _LOG.info("Connection successful - Model: %s", test_device.model_name)

            # Disconnect test device
            await test_device.disconnect()

            _LOG.info("Setup successful for %s", name)
            return test_config

        except asyncio.TimeoutError:
            _LOG.error("Connection timeout to %s:%d", host, port)
            raise ValueError(
                f"Connection timeout to {host}:{port}\n\n"
                "Please verify:\n"
                "• Receiver is powered on\n"
                "• Receiver is connected to your network\n"
                "• IP address is correct\n"
                "• Receiver is not in Green mode (IP control disabled)"
            ) from None

        except ConnectionError as err:
            _LOG.error("Connection failed: %s", err)
            raise ValueError(
                f"Failed to connect to receiver at {host}:{port}\n\n"
                "Please check:\n"
                "• IP address is correct\n"
                "• Receiver is powered on and network connected\n"
                "• No firewall blocking port 50000"
            ) from err

        except Exception as err:
            _LOG.error("Setup error: %s", err, exc_info=True)
            raise ValueError(f"Setup failed: {err}") from err
