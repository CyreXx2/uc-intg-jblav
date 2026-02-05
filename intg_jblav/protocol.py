"""
JBL MA Series binary protocol handler.

Implements the JBL IP Control protocol v1.7 for MA510/MA710/MA7100HP/MA9100HP receivers.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
from enum import IntEnum
from typing import Any

_LOG = logging.getLogger(__name__)


class JBLCommand(IntEnum):
    """JBL command IDs."""

    POWER = 0x00
    DISPLAY_DIM = 0x01
    VERSION = 0x02
    SIMULATE_IR = 0x04
    INPUT_SOURCE = 0x05
    VOLUME = 0x06
    MUTE = 0x07
    SURROUND_MODE = 0x08
    PARTY_MODE = 0x09
    PARTY_VOLUME = 0x0A
    TREBLE_EQ = 0x0B
    BASS_EQ = 0x0C
    ROOM_EQ = 0x0D
    DIALOG_ENHANCED = 0x0E
    DOLBY_AUDIO_MODE = 0x0F
    DRC = 0x10
    STREAMING_STATE = 0x11
    INITIALIZATION = 0x50
    HEARTBEAT = 0x51
    REBOOT = 0x52
    FACTORY_RESET = 0x53


class JBLResponseCode(IntEnum):
    """JBL response codes."""

    STATUS_UPDATE = 0x00
    COMMAND_NOT_RECOGNIZED = 0xC1
    PARAMETER_NOT_RECOGNIZED = 0xC2
    COMMAND_INVALID = 0xC3
    INVALID_DATA_LENGTH = 0xC4


class JBLModel(IntEnum):
    """JBL receiver models."""

    MA510 = 0x01
    MA710 = 0x02
    MA7100HP = 0x03
    MA9100HP = 0x04


class JBLInputSource(IntEnum):
    """JBL input sources."""

    TV_ARC = 0x01
    HDMI_1 = 0x02
    HDMI_2 = 0x03
    HDMI_3 = 0x04
    HDMI_4 = 0x05
    HDMI_5 = 0x06  # MA710/MA7100HP/MA9100HP only
    HDMI_6 = 0x07  # MA710/MA7100HP/MA9100HP only
    COAX = 0x08
    OPTICAL = 0x09
    ANALOG_1 = 0x0A
    ANALOG_2 = 0x0B
    PHONO = 0x0C  # MA710/MA7100HP/MA9100HP only
    BLUETOOTH = 0x0D
    NETWORK = 0x0E


class JBLSurroundMode(IntEnum):
    """JBL surround modes."""

    DOLBY_SURROUND = 0x01  # MA710/MA7100HP/MA9100HP only
    DTS_NEURAL_X = 0x02  # MA710/MA7100HP/MA9100HP only
    STEREO_2_0 = 0x03
    STEREO_2_1 = 0x04
    ALL_STEREO = 0x05
    NATIVE = 0x06
    DOLBY_PROLOGIC_II = 0x07  # MA510 only


class JBLProtocol:
    """JBL MA Series binary protocol handler."""

    # Protocol constants
    CMD_START = 0x23
    RESP_START = bytes([0x02, 0x23])
    END = 0x0D
    REQUEST_DATA = 0xF0

    # Input source names
    INPUT_SOURCE_NAMES = {
        JBLInputSource.TV_ARC: "TV (ARC)",
        JBLInputSource.HDMI_1: "HDMI 1",
        JBLInputSource.HDMI_2: "HDMI 2",
        JBLInputSource.HDMI_3: "HDMI 3",
        JBLInputSource.HDMI_4: "HDMI 4",
        JBLInputSource.HDMI_5: "HDMI 5",
        JBLInputSource.HDMI_6: "HDMI 6",
        JBLInputSource.COAX: "Coax",
        JBLInputSource.OPTICAL: "Optical",
        JBLInputSource.ANALOG_1: "Analog 1",
        JBLInputSource.ANALOG_2: "Analog 2",
        JBLInputSource.PHONO: "Phono",
        JBLInputSource.BLUETOOTH: "Bluetooth",
        JBLInputSource.NETWORK: "Network",
    }

    # Surround mode names
    SURROUND_MODE_NAMES = {
        JBLSurroundMode.DOLBY_SURROUND: "Dolby Surround",
        JBLSurroundMode.DTS_NEURAL_X: "DTS Neural:X",
        JBLSurroundMode.STEREO_2_0: "Stereo 2.0",
        JBLSurroundMode.STEREO_2_1: "Stereo 2.1",
        JBLSurroundMode.ALL_STEREO: "All Stereo",
        JBLSurroundMode.NATIVE: "Native",
        JBLSurroundMode.DOLBY_PROLOGIC_II: "Dolby Pro Logic II",
    }

    # Model names
    MODEL_NAMES = {
        JBLModel.MA510: "MA510",
        JBLModel.MA710: "MA710",
        JBLModel.MA7100HP: "MA7100HP",
        JBLModel.MA9100HP: "MA9100HP",
    }

    # IR Remote codes (NEC format, 24-bit)
    # Navigation
    IR_POWER = 0x010E03
    IR_UP = 0x010E99
    IR_DOWN = 0x010E59
    IR_LEFT = 0x010E83
    IR_RIGHT = 0x010E43
    IR_OK = 0x010E21
    IR_MENU = 0x010ECA
    IR_BACK = 0x010EA1
    IR_DIM = 0x010EC9

    # Volume controls
    IR_VOL_UP = 0x010EE3
    IR_VOL_DOWN = 0x010E13
    IR_MUTE = 0x010EC3

    # Source navigation
    IR_SOURCE_UP = 0x010E8C
    IR_SOURCE_DOWN = 0x010E0C

    # Surround navigation
    IR_SURR_UP = 0x010EF4
    IR_SURR_DOWN = 0x010E74

    # Discrete power
    IR_MAIN_POWER_ON = 0x010ED9
    IR_MAIN_POWER_OFF = 0x010EF9

    # Discrete input sources (all models)
    IR_TV = 0x010E71
    IR_HDMI1 = 0x010E11
    IR_HDMI2 = 0x010E91
    IR_HDMI3 = 0x010E51
    IR_HDMI4 = 0x010ED1
    IR_HDMI5 = 0x010E31  # MA710+ only
    IR_HDMI6 = 0x010EB1  # MA710+ only
    IR_COAX = 0x010E81
    IR_OPTICAL = 0x010EDB
    IR_ANALOG1 = 0x010E23
    IR_ANALOG2 = 0x010E33
    IR_PHONO = 0x010E0B  # MA710+ only
    IR_BLUETOOTH = 0x010E53
    IR_NETWORK = 0x010ED3

    # Party mode (MA710+ only)
    IR_PARTY_ON = 0x010E73
    IR_PARTY_OFF = 0x010E8B
    IR_PARTY_VOL_UP = 0x010E39
    IR_PARTY_VOL_DOWN = 0x010EB9

    @staticmethod
    def build_command(cmd_id: int, *data: int) -> bytes:
        """
        Build a JBL command message.

        Format: <Start><CmdID><DataLen><Data1>...<DataN><End>

        Args:
            cmd_id: Command ID
            *data: Variable number of data bytes

        Returns:
            Complete command as bytes
        """
        data_len = len(data)
        command = bytes([JBLProtocol.CMD_START, cmd_id, data_len])
        command += bytes(data)
        command += bytes([JBLProtocol.END])
        return command

    @staticmethod
    def parse_response(data: bytes) -> dict[str, Any] | None:
        """
        Parse a JBL response message.

        Format: <Start><CmdID><RspCode><DataLen><Data1>...<DataN><End>
        Start is TWO bytes: 0x02 0x23

        Args:
            data: Raw response bytes

        Returns:
            Parsed response dict or None if invalid
        """
        if len(data) < 5:  # Minimum: 2-byte start + cmd + rsp + len + end
            _LOG.debug("Response too short: %d bytes", len(data))
            return None

        # Check start bytes
        if data[0:2] != JBLProtocol.RESP_START:
            _LOG.debug("Invalid start bytes: %s", data[0:2].hex())
            return None

        # Check end byte
        if data[-1] != JBLProtocol.END:
            _LOG.debug("Invalid end byte: 0x%02X", data[-1])
            return None

        cmd_id = data[2]
        rsp_code = data[3]
        data_len = data[4]

        # Extract data bytes (if any)
        response_data = []
        if data_len > 0:
            if len(data) < 5 + data_len + 1:  # start(2) + cmd + rsp + len + data + end
                _LOG.debug("Incomplete data: expected %d bytes, got %d", data_len, len(data) - 6)
                return None
            response_data = list(data[5:5 + data_len])

        return {
            "cmd_id": cmd_id,
            "rsp_code": rsp_code,
            "data": response_data,
        }

    # Command builders
    @staticmethod
    def cmd_power_on() -> bytes:
        """Power on command."""
        return JBLProtocol.build_command(JBLCommand.POWER, 0x01)

    @staticmethod
    def cmd_power_off() -> bytes:
        """Power off command."""
        return JBLProtocol.build_command(JBLCommand.POWER, 0x00)

    @staticmethod
    def cmd_power_query() -> bytes:
        """Query power state."""
        return JBLProtocol.build_command(JBLCommand.POWER, JBLProtocol.REQUEST_DATA)

    @staticmethod
    def cmd_volume_set(volume: int) -> bytes:
        """Set volume (0-99)."""
        volume = max(0, min(99, volume))
        return JBLProtocol.build_command(JBLCommand.VOLUME, volume)

    @staticmethod
    def cmd_volume_query() -> bytes:
        """Query current volume."""
        return JBLProtocol.build_command(JBLCommand.VOLUME, JBLProtocol.REQUEST_DATA)

    @staticmethod
    def cmd_mute_on() -> bytes:
        """Mute on command."""
        return JBLProtocol.build_command(JBLCommand.MUTE, 0x01)

    @staticmethod
    def cmd_mute_off() -> bytes:
        """Mute off command."""
        return JBLProtocol.build_command(JBLCommand.MUTE, 0x00)

    @staticmethod
    def cmd_mute_query() -> bytes:
        """Query mute status."""
        return JBLProtocol.build_command(JBLCommand.MUTE, JBLProtocol.REQUEST_DATA)

    @staticmethod
    def cmd_input_source_set(source: int) -> bytes:
        """Set input source."""
        return JBLProtocol.build_command(JBLCommand.INPUT_SOURCE, source)

    @staticmethod
    def cmd_input_source_query() -> bytes:
        """Query current input source."""
        return JBLProtocol.build_command(JBLCommand.INPUT_SOURCE, JBLProtocol.REQUEST_DATA)

    @staticmethod
    def cmd_surround_mode_set(mode: int) -> bytes:
        """Set surround mode."""
        return JBLProtocol.build_command(JBLCommand.SURROUND_MODE, mode)

    @staticmethod
    def cmd_surround_mode_query() -> bytes:
        """Query current surround mode."""
        return JBLProtocol.build_command(JBLCommand.SURROUND_MODE, JBLProtocol.REQUEST_DATA)

    @staticmethod
    def cmd_initialization() -> bytes:
        """
        Initialize connection and request model identification.

        This should be sent immediately after connection is established.
        """
        return JBLProtocol.build_command(JBLCommand.INITIALIZATION, JBLProtocol.REQUEST_DATA)

    @staticmethod
    def cmd_heartbeat() -> bytes:
        """
        Heartbeat command to check device is connected.

        Also resets auto-standby timer on the receiver.
        """
        return JBLProtocol.build_command(JBLCommand.HEARTBEAT)

    @staticmethod
    def cmd_version_query(version_type: int = 0xF0) -> bytes:
        """
        Query software version.

        Args:
            version_type: 0xF0=IP control, 0xF1=Host, 0xF2=DSP, 0xF3=OSD, 0xF4=NET
        """
        return JBLProtocol.build_command(JBLCommand.VERSION, version_type)

    @staticmethod
    def cmd_display_dim_set(level: int) -> bytes:
        """
        Set display brightness (0-3).

        Args:
            level: 0=Off, 1=Dim, 2=Mid, 3=Bright
        """
        level = max(0, min(3, level))
        return JBLProtocol.build_command(JBLCommand.DISPLAY_DIM, level)

    @staticmethod
    def cmd_display_dim_query() -> bytes:
        """Query current display brightness."""
        return JBLProtocol.build_command(JBLCommand.DISPLAY_DIM, JBLProtocol.REQUEST_DATA)

    @staticmethod
    def cmd_ir_simulate(ir_code: int) -> bytes:
        """
        Simulate IR remote command.

        Args:
            ir_code: NEC-encoded IR command (24-bit)
        """
        # Split 24-bit IR code into 3 bytes (MSB to LSB)
        byte1 = (ir_code >> 16) & 0xFF
        byte2 = (ir_code >> 8) & 0xFF
        byte3 = ir_code & 0xFF
        return JBLProtocol.build_command(JBLCommand.SIMULATE_IR, byte1, byte2, byte3)

    @staticmethod
    def cmd_party_mode_on() -> bytes:
        """Enable party mode (MA710/MA7100HP/MA9100HP only)."""
        return JBLProtocol.build_command(JBLCommand.PARTY_MODE, 0x01)

    @staticmethod
    def cmd_party_mode_off() -> bytes:
        """Disable party mode (MA710/MA7100HP/MA9100HP only)."""
        return JBLProtocol.build_command(JBLCommand.PARTY_MODE, 0x00)

    @staticmethod
    def cmd_party_mode_query() -> bytes:
        """Query party mode status (MA710/MA7100HP/MA9100HP only)."""
        return JBLProtocol.build_command(JBLCommand.PARTY_MODE, JBLProtocol.REQUEST_DATA)

    @staticmethod
    def cmd_party_volume_set(volume: int) -> bytes:
        """
        Set party mode volume (MA710/MA7100HP/MA9100HP only).

        Args:
            volume: Volume level (0-99)
        """
        volume = max(0, min(99, volume))
        return JBLProtocol.build_command(JBLCommand.PARTY_VOLUME, volume)

    @staticmethod
    def cmd_party_volume_query() -> bytes:
        """Query party mode volume (MA710/MA7100HP/MA9100HP only)."""
        return JBLProtocol.build_command(JBLCommand.PARTY_VOLUME, JBLProtocol.REQUEST_DATA)

    @staticmethod
    def cmd_treble_eq_set(level: int) -> bytes:
        """
        Set treble EQ level (-6 to +6).

        Args:
            level: EQ level from -6 to +6 dB (encoded as 0-12)
        """
        level = max(0, min(12, level + 6))  # Convert -6:+6 to 0:12
        return JBLProtocol.build_command(JBLCommand.TREBLE_EQ, level)

    @staticmethod
    def cmd_treble_eq_query() -> bytes:
        """Query treble EQ level."""
        return JBLProtocol.build_command(JBLCommand.TREBLE_EQ, JBLProtocol.REQUEST_DATA)

    @staticmethod
    def cmd_bass_eq_set(level: int) -> bytes:
        """
        Set bass EQ level (-6 to +6).

        Args:
            level: EQ level from -6 to +6 dB (encoded as 0-12)
        """
        level = max(0, min(12, level + 6))  # Convert -6:+6 to 0:12
        return JBLProtocol.build_command(JBLCommand.BASS_EQ, level)

    @staticmethod
    def cmd_bass_eq_query() -> bytes:
        """Query bass EQ level."""
        return JBLProtocol.build_command(JBLCommand.BASS_EQ, JBLProtocol.REQUEST_DATA)

    @staticmethod
    def cmd_room_eq_on() -> bytes:
        """Enable room EQ."""
        return JBLProtocol.build_command(JBLCommand.ROOM_EQ, 0x01)

    @staticmethod
    def cmd_room_eq_off() -> bytes:
        """Disable room EQ."""
        return JBLProtocol.build_command(JBLCommand.ROOM_EQ, 0x00)

    @staticmethod
    def cmd_room_eq_query() -> bytes:
        """Query room EQ status."""
        return JBLProtocol.build_command(JBLCommand.ROOM_EQ, JBLProtocol.REQUEST_DATA)

    @staticmethod
    def cmd_dialog_enhanced_on() -> bytes:
        """Enable dialog enhanced."""
        return JBLProtocol.build_command(JBLCommand.DIALOG_ENHANCED, 0x01)

    @staticmethod
    def cmd_dialog_enhanced_off() -> bytes:
        """Disable dialog enhanced."""
        return JBLProtocol.build_command(JBLCommand.DIALOG_ENHANCED, 0x00)

    @staticmethod
    def cmd_dialog_enhanced_query() -> bytes:
        """Query dialog enhanced status."""
        return JBLProtocol.build_command(JBLCommand.DIALOG_ENHANCED, JBLProtocol.REQUEST_DATA)

    @staticmethod
    def cmd_dolby_audio_mode_on() -> bytes:
        """Enable Dolby audio mode."""
        return JBLProtocol.build_command(JBLCommand.DOLBY_AUDIO_MODE, 0x01)

    @staticmethod
    def cmd_dolby_audio_mode_off() -> bytes:
        """Disable Dolby audio mode."""
        return JBLProtocol.build_command(JBLCommand.DOLBY_AUDIO_MODE, 0x00)

    @staticmethod
    def cmd_dolby_audio_mode_query() -> bytes:
        """Query Dolby audio mode status."""
        return JBLProtocol.build_command(JBLCommand.DOLBY_AUDIO_MODE, JBLProtocol.REQUEST_DATA)

    @staticmethod
    def cmd_drc_on() -> bytes:
        """Enable DRC (MA710/MA7100HP/MA9100HP only)."""
        return JBLProtocol.build_command(JBLCommand.DRC, 0x01)

    @staticmethod
    def cmd_drc_off() -> bytes:
        """Disable DRC (MA710/MA7100HP/MA9100HP only)."""
        return JBLProtocol.build_command(JBLCommand.DRC, 0x00)

    @staticmethod
    def cmd_drc_query() -> bytes:
        """Query DRC status (MA710/MA7100HP/MA9100HP only)."""
        return JBLProtocol.build_command(JBLCommand.DRC, JBLProtocol.REQUEST_DATA)

    @staticmethod
    def cmd_streaming_state_query() -> bytes:
        """Query streaming server state."""
        return JBLProtocol.build_command(JBLCommand.STREAMING_STATE, JBLProtocol.REQUEST_DATA)

    @staticmethod
    def cmd_reboot() -> bytes:
        """Reboot the receiver."""
        return JBLProtocol.build_command(JBLCommand.REBOOT)

    @staticmethod
    def cmd_factory_reset() -> bytes:
        """Factory reset the receiver."""
        return JBLProtocol.build_command(JBLCommand.FACTORY_RESET)
