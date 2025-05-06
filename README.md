# FortiGate SNMP Monitoring with Prometheus & Grafana

This project collects SNMP data from a FortiGate firewall (e.g., version info, CPU, memory, bandwidth) and displays it in Grafana via Prometheus.

## 📦 Components

- **FortiGate** with SNMP enabled (v2c or v3 recommended)
- **Prometheus** for metric collection
- **SNMP Exporter** for translating SNMP to Prometheus format
- **Grafana** for dashboards and visualization

---

## 🛠 Configuration

### 1. FortiGate SNMP Setup

Enable SNMP (v2c or v3) on your FortiGate:

- Go to **System > SNMP**
- Create a new community:
  - Version: **v2c**
  - Community Name: `SNMP-12`
  - Allow access from your Prometheus server

---

### 2. SNMP Exporter (`snmp.yml`)

```yaml
modules:
  fortigate:
    version: 2c
    auth:
      community: SNMP-12
    walk:
      - 1.3.6.1.2.1.1        # System (includes sysDescr)
      - 1.3.6.1.4.1.12356    # Fortinet MIB
```
---
### 3. OIDs
```
        "Firmware Version": ObjectType(ObjectIdentity("1.3.6.1.4.1.12356.101.4.1.1.0")),
        "uptime, days": ObjectType(ObjectIdentity("1.3.6.1.2.1.1.3.0")),
        "cpu, %": ObjectType(ObjectIdentity("1.3.6.1.4.1.12356.101.4.1.3.0")),
        "memory, %": ObjectType(ObjectIdentity("1.3.6.1.4.1.12356.101.4.1.4.0")),
        "Low Memory Usage, %": ObjectType(ObjectIdentity("1.3.6.1.4.1.12356.101.4.1.9.0")),
        "Disk Usage, MB": ObjectType(ObjectIdentity("1.3.6.1.4.1.12356.101.4.1.6.0")),
        "Sessions": ObjectType(ObjectIdentity("1.3.6.1.4.1.12356.101.4.1.6.0")),
        "Active_Sessions": ObjectType(ObjectIdentity("1.3.6.1.4.1.12356.101.4.1.8.0")),
        "FanStatusSpeed_1": ObjectType(ObjectIdentity("iso.3.6.1.4.1.12356.101.4.3.2.1.3.3")),
        "FanStatusSpeed_2": ObjectType(ObjectIdentity("iso.3.6.1.4.1.12356.101.4.3.2.1.3.4")),

        "CPU_ON_DIE_Temperature_71": ObjectType(ObjectIdentity("iso.3.6.1.4.1.12356.101.4.3.2.1.3.1")),  # , °C
        "MV1514_1_Temperature": ObjectType(ObjectIdentity("iso.3.6.1.4.1.12356.101.4.3.2.1.3.2")),  # , °C
        "MV1514_2_Temperature": ObjectType(ObjectIdentity("iso.3.6.1.4.1.12356.101.4.3.2.1.3.3")),  # , °C
        "MV1680_Temperature": ObjectType(ObjectIdentity("iso.3.6.1.4.1.12356.101.4.3.2.1.3.4")),  # , °C
        
        "TMP1_External_Temperature": ObjectType(ObjectIdentity("iso.3.6.1.4.1.12356.101.4.3.2.1.3.5")),  # , °C
        "TMP4_ON_DIE_Temperature": ObjectType(ObjectIdentity("iso.3.6.1.4.1.12356.101.4.3.2.1.3.6")),  # , °C
        "CPU_ON_DIE_Temperature": ObjectType(ObjectIdentity("iso.3.6.1.4.1.12356.101.4.3.2.1.3.7")),  # , °C
        "BCM_Switch_Temperature": ObjectType(ObjectIdentity("iso.3.6.1.4.1.12356.101.4.3.2.1.3.8")),  # , °C
        "B50185_Temperature": ObjectType(ObjectIdentity("iso.3.6.1.4.1.12356.101.4.3.2.1.3.9")),  # , °C
        "B50210_1_Temperature": ObjectType(ObjectIdentity("iso.3.6.1.4.1.12356.101.4.3.2.1.3.10")),  # , °C
        "B50210_2_Temperature": ObjectType(ObjectIdentity("iso.3.6.1.4.1.12356.101.4.3.2.1.3.11")),  # , °C
```
