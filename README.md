# JBL AV Receiver Integration for Unfolded Circle Remote 2/3

Control your JBL MA Series AV Receiver directly from your Unfolded Circle Remote 2 or Remote 3 with comprehensive media player control, **real-time state monitoring**, and **complete TCP binary protocol-based control**.

![JBL](https://img.shields.io/badge/JBL-AV%20Receiver-blue)
[![GitHub Release](https://img.shields.io/github/v/release/mase1981/uc-intg-jblav?style=flat-square)](https://github.com/mase1981/uc-intg-jblav/releases)
![License](https://img.shields.io/badge/license-MPL--2.0-blue?style=flat-square)
[![GitHub issues](https://img.shields.io/github/issues/mase1981/uc-intg-jblav?style=flat-square)](https://github.com/mase1981/uc-intg-jblav/issues)
[![Community Forum](https://img.shields.io/badge/community-forum-blue?style=flat-square)](https://unfolded.community/)
[![Discord](https://badgen.net/discord/online-members/zGVYf58)](https://discord.gg/zGVYf58)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/mase1981/uc-intg-jblav/total?style=flat-square)
[![Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=flat-square)](https://buymeacoffee.com/meirmiyara)
[![PayPal](https://img.shields.io/badge/PayPal-donate-blue.svg?style=flat-square)](https://paypal.me/mmiyara)
[![Github Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-30363D?&logo=GitHub-Sponsors&logoColor=EA4AAA&style=flat-square)](https://github.com/sponsors/mase1981)

## Features

This integration provides comprehensive control of JBL MA Series AV Receivers through the native TCP binary protocol, delivering seamless integration with your Unfolded Circle Remote for complete home theater control.

---
## ❤️ Support Development ❤️

If you find this integration useful, consider supporting development:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-pink?style=for-the-badge&logo=github)](https://github.com/sponsors/mase1981)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/meirmiyara)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/mmiyara)

Your support helps maintain this integration. Thank you! ❤️
---

### 🎵 **Media Player Control**
### 🎛️ **Select Entities**
### 📊 **Sensor Entities**
### 🎮 **Remote Entity**
### **Protocol Requirements**

- **Protocol**: JBL IP Control Protocol v1.7 (Binary)
- **TCP Port**: 50000 (fixed)
- **Network Access**: Receiver must be on same local network
- **Connection**: Persistent TCP connection with automatic reconnection
- **Real-time Updates**: Receiver sends unsolicited state change notifications

### **Network Requirements**

- **Local Network Access** - Integration requires same network as JBL receiver
- **TCP Protocol** - Binary protocol on port 50000
- **Static IP Recommended** - Receiver should have static IP or DHCP reservation
- **Firewall** - Must allow TCP traffic on port 50000
- **Power Mode** - IP control disabled in "Green" power mode

---

## 🎛️ **Supported Models**

This integration supports all JBL MA Series receivers with identical protocol support.

### Protocol Notes

All models use the same TCP binary protocol on port 50000. The integration automatically detects the receiver model during setup and adjusts available features accordingly.

**Important:** IP control is disabled when the receiver is in "Green" standby mode or disconnected from the network. Ensure the receiver is in normal standby or powered on for IP control to function.

---

## Installation

### Option 1: Remote Web Interface (Recommended)
1. Navigate to the [**Releases**](https://github.com/mase1981/uc-intg-jblav/releases) page
2. Download the latest `uc-intg-jblav-<version>-aarch64.tar.gz` file
3. Open your remote's web interface (`http://your-remote-ip`)
4. Go to **Settings** → **Integrations** → **Add Integration**
5. Click **Upload** and select the downloaded `.tar.gz` file

### Option 2: Docker (Advanced Users)

The integration is available as a pre-built Docker image from GitHub Container Registry:

**Image**: `ghcr.io/mase1981/uc-intg-jblav:latest`

**Docker Compose:**
```yaml
services:
  uc-intg-jblav:
    image: ghcr.io/mase1981/uc-intg-jblav:latest
    container_name: uc-intg-jblav
    network_mode: host
    volumes:
      - </local/path>:/data
    environment:
      - UC_CONFIG_HOME=/data
      - UC_INTEGRATION_HTTP_PORT=9090
      - UC_INTEGRATION_INTERFACE=0.0.0.0
      - PYTHONPATH=/app
    restart: unless-stopped
```

**Docker Run:**
```bash
docker run -d --name uc-jblav --restart unless-stopped --network host -v jblav-config:/app/config -e UC_CONFIG_HOME=/app/config -e UC_INTEGRATION_INTERFACE=0.0.0.0 -e UC_INTEGRATION_HTTP_PORT=9090 -e PYTHONPATH=/app ghcr.io/mase1981/uc-intg-jblav:latest
```

---

## 📄 License

This project is licensed under the **Mozilla Public License 2.0** (MPL-2.0).

See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Unfolded Circle** - For the amazing Remote hardware and integration framework
- **JBL/Harman** - For the IP control protocol specification
- **Community** - For testing, feedback, and support

---

## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/mase1981/uc-intg-jblav/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mase1981/uc-intg-jblav/discussions)
- **Forum**: [Unfolded Circle Community](https://unfolded.community/)
- **Developer**: [Meir Miyara](https://www.linkedin.com/in/meirmiyara)
- **Discord**: [Unfolded Circle Discord](https://discord.gg/zGVYf58)

---

Made with ❤️ by **Meir Miyara**

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-pink?style=for-the-badge&logo=github)](https://github.com/sponsors/mase1981)
