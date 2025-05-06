# pip install paramiko
# pip install prometheus_client
########################
### Maksym Tsybulskyi ###
###      2025        ###

from prometheus_client import start_http_server, Gauge, Info, Counter
import time
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *


Firmware_Version = Info('Firmware_Version', 'Description of firmware version')
Uptime = Gauge('Uptime', 'Description of info')
cpu = Gauge('CPU_load', 'CPU load')
memory = Gauge('Memory_load', 'Memory load')
Low_Memory_Usage = Gauge('Low_Memory_Usage', 'Memory load')
Disk_Usage = Gauge('Disk_Usage', 'Memory load')
Sessions = Gauge('Sessions', 'Sessions')
Active_Sessions = Gauge('Active_Sessions', 'Active_Sessions')
FanStatusSpeed_1 = Gauge('FanStatusSpeed_1', 'FanStatusSpeed_1')
FanStatusSpeed_2 = Gauge('FanStatusSpeed_2', 'FanStatusSpeed_2')

CPU_ON_DIE_Temperature_71 = Gauge('CPU_ON_DIE_Temperature_71', 'CPU_ON_DIE_Temperature_71')
MV1514_1_Temperature = Gauge('MV1514_1_Temperature', 'MV1514_1_Temperature')
MV1514_2_Temperature = Gauge('MV1514_2_Temperature', 'MV1514_2_Temperature')
MV1680_Temperature = Gauge('MV1680_Temperature', 'MV1680_Temperature')


async def run_Fortigate71():
    snmpEngine = SnmpEngine()
    results = []
    # Create transport
    transport = await UdpTransportTarget.create(("192.168.26.1", 161))

    # Define SNMP OIDs
    oids = {
        # "sysDescr": ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0")),
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
    }

    # Run SNMP GET
    result = await get_cmd(
        snmpEngine,
        CommunityData("SNMP-12", mpModel=1),  # SNMPv2c
        transport,
        ContextData(),
        *oids.values(),
    )

    errorIndication, errorStatus, errorIndex, varBinds = result

    if errorIndication:
        print("SNMP Error:", errorIndication)
    elif errorStatus:
        print(
            "{} at {}".format(
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        for key, varBind in zip(oids.keys(), varBinds):
            if key == "uptime, days":
                results.append(f"{key} = {round((varBind[1] / 8640000), 1)}")
            else:
                results.append(f"{key} = {varBind[1]}")
        data = dict(item.split(" = ") for item in results)
        return data

    # Clean up
    snmpEngine.close_dispatcher()



def collect_dataMO():
    data = asyncio.run(run_Fortigate71())
    Firmware_Version.info({'version': (data.get("Firmware Version"))})
    Uptime.set(data.get("uptime, days"))
    cpu.set(data.get("cpu, %"))
    memory.set(data.get("memory, %"))
    Disk_Usage.set(data.get("Disk Usage, MB"))
    FanStatusSpeed_1.set(data.get("FanStatusSpeed_1"))
    FanStatusSpeed_2.set(data.get("FanStatusSpeed_2"))
    Sessions.set(data.get("Sessions"))
    Active_Sessions.set(data.get("Active_Sessions"))
    CPU_ON_DIE_Temperature_71.set(data.get("CPU_ON_DIE_Temperature_71"))
    MV1514_1_Temperature.set(data.get("MV1514_1_Temperature"))
    MV1514_2_Temperature.set(data.get("MV1514_2_Temperature"))
    MV1680_Temperature.set(data.get("MV1680_Temperature"))


if __name__ == '__main__':
    # Start a Prometheus metrics server on port 8000
    start_http_server(8024)
    print("Serving metrics on http://localhost:8024/metrics")

    # Collect and update the metric periodically
    while True:
        collect_dataMO()
        time.sleep(60)  # Adjust the interval as needed
