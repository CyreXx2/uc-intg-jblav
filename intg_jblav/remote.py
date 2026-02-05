"""
JBL AV Receiver Remote entity for comprehensive control.

This entity exposes all receiver commands through organized UI pages.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
from typing import Any
from ucapi import StatusCodes
from ucapi.remote import Attributes, Commands, Features, Remote, States
from ucapi.ui import Buttons, DeviceButtonMapping, create_btn_mapping, UiPage
from ucapi_framework.entity import Entity
from intg_jblav.config import JBLAVConfig
from intg_jblav.device import JBLAV
from intg_jblav.protocol import JBLProtocol

_LOG = logging.getLogger(__name__)

# Standard button sizes (JSON-serializable)
SIZE_1X1 = {"width": 1, "height": 1}


class JBLAVRemote(Remote, Entity):
    """Remote entity for JBL AV receiver with comprehensive controls."""

    def __init__(self, device_config: JBLAVConfig, device: JBLAV):
        """Initialize remote entity."""
        self._device = device
        self._device_config = device_config

        entity_id = f"remote.{device_config.identifier}"
        entity_name = f"{device_config.name} Remote"

        ui_pages = self._create_ui_pages()
        simple_commands = self._create_simple_commands()
        button_mapping = self._create_button_mapping()

        attributes = {
            Attributes.STATE: States.UNAVAILABLE,
        }

        features = [
            Features.SEND_CMD,
            Features.ON_OFF,
        ]

        super().__init__(
            entity_id,
            entity_name,
            features,
            attributes,
            simple_commands=simple_commands,
            button_mapping=button_mapping,
            ui_pages=ui_pages,
            cmd_handler=self.handle_command,
        )

        device.events.on(device.identifier, self._on_device_update)
        _LOG.info("[%s] Remote entity initialized", self.id)

    def _create_simple_commands(self) -> list[str]:
        return [
            "POWER_ON", "POWER_OFF", "POWER_TOGGLE",
            "VOLUME_UP", "VOLUME_DOWN", "MUTE_TOGGLE",
            "CURSOR_UP", "CURSOR_DOWN", "CURSOR_LEFT", "CURSOR_RIGHT",
            "CURSOR_ENTER", "BACK", "MENU",
            "TV", "HDMI_1", "HDMI_2", "HDMI_3", "HDMI_4", "HDMI_5", "HDMI_6",
            "COAX", "OPTICAL", "ANALOG_1", "ANALOG_2", "PHONO",
            "BLUETOOTH", "NETWORK",
            "SURROUND_MODE_STEREO_2_0", "SURROUND_MODE_STEREO_2_1",
            "SURROUND_MODE_ALL_STEREO", "SURROUND_MODE_NATIVE",
            "SURROUND_MODE_DOLBY_SURROUND", "SURROUND_MODE_DTS_NEURAL_X",
        ]

    def _create_button_mapping(self) -> list[DeviceButtonMapping]:
        return [
            create_btn_mapping(Buttons.POWER, "POWER_TOGGLE"),
            create_btn_mapping(Buttons.VOLUME_UP, "VOLUME_UP"),
            create_btn_mapping(Buttons.VOLUME_DOWN, "VOLUME_DOWN"),
            create_btn_mapping(Buttons.MUTE, "MUTE_TOGGLE"),
            create_btn_mapping(Buttons.DPAD_UP, "CURSOR_UP"),
            create_btn_mapping(Buttons.DPAD_DOWN, "CURSOR_DOWN"),
            create_btn_mapping(Buttons.DPAD_LEFT, "CURSOR_LEFT"),
            create_btn_mapping(Buttons.DPAD_RIGHT, "CURSOR_RIGHT"),
            create_btn_mapping(Buttons.DPAD_MIDDLE, "CURSOR_ENTER"),
            create_btn_mapping(Buttons.BACK, "BACK"),
            create_btn_mapping(Buttons.HOME, "MENU"),
        ]

    def _create_ui_pages(self) -> list[dict[str, Any]]:
        return [
            {
                "page_id": "navigation",
                "name": "Navigation",
                "grid": {"columns": 3, "rows": 4},
                "items": [
                    {"command": "MENU", "location": {"x": 0, "y": 0}, "size": SIZE_1X1, "icon": "uc:menu", "text": "Menu"},
                    {"command": "CURSOR_UP", "location": {"x": 1, "y": 0}, "size": SIZE_1X1, "icon": "uc:up-arrow-bold"},
                    {"command": "BACK", "location": {"x": 2, "y": 0}, "size": SIZE_1X1, "icon": "uc:back", "text": "Back"},
                    {"command": "CURSOR_LEFT", "location": {"x": 0, "y": 1}, "size": SIZE_1X1, "icon": "uc:left-arrow-bold"},
                    {"command": "CURSOR_ENTER", "location": {"x": 1, "y": 1}, "size": SIZE_1X1, "icon": "uc:circle", "text": "OK"},
                    {"command": "CURSOR_RIGHT", "location": {"x": 2, "y": 1}, "size": SIZE_1X1, "icon": "uc:right-arrow-bold"},
                    {"command": "CURSOR_DOWN", "location": {"x": 1, "y": 2}, "size": SIZE_1X1, "icon": "uc:down-arrow-bold"},
                    {"command": "VOLUME_UP", "location": {"x": 0, "y": 3}, "size": SIZE_1X1, "icon": "uc:volume-up", "text": "Vol+"},
                    {"command": "MUTE_TOGGLE", "location": {"x": 1, "y": 3}, "size": SIZE_1X1, "icon": "uc:mute", "text": "Mute"},
                    {"command": "VOLUME_DOWN", "location": {"x": 2, "y": 3}, "size": SIZE_1X1, "icon": "uc:volume-down", "text": "Vol-"},
                ],
            },
        ]

    def _on_device_update(self, entity_id: str, attributes: dict[str, Any]) -> None:
        if "power" in attributes:
            self.attributes[Attributes.STATE] = States.ON if attributes["power"] else States.OFF
            self.emit_update()

    async def handle_command(self, entity: Remote, cmd_id: str, params: dict[str, Any] | None) -> StatusCodes:
        try:
            return StatusCodes.OK
        except Exception as err:
            _LOG.error("[%s] Command error: %s", self.id, err)
            return StatusCodes.SERVER_ERROR

    def emit_update(self) -> None:
        if hasattr(self, "api") and self.api:
            self.api.configured_entities.update(self)
