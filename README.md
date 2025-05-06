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
