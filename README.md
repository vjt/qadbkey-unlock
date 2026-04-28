# Quectel RM5XX ADBKEY Unlock script

This is a modification of Ryan Bradley's script to support RM5XX Series modems. It works for the RM520N-GL, RM502Q-AE, RM500Q-AE, EM120K-GL, and others.
For more information, see [Getting ADB Access](https://github.com/natecarlson/quectel-rgmii-configuration-notes#getting-adb-access).

### Full ADB Unlock Sequence

**Step 1 — Get the challenge from the modem**

```
AT+QADBKEY?
+QADBKEY: 12345678
```

**Step 2 — Generate the unlock key**

Online: paste the challenge into https://onecompiler.com/python/3znepjcsq and click run.

Locally:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

python3 qadbkey-unlock2.py 12345678
AT+QADBKEY="0jXKXQwSwMxYoeg"
```

Older Pythons (<= 3.12) ship `crypt` in stdlib — the venv step is still
recommended but `requirements.txt` becomes a no-op.

**Step 3 — Submit the key to the modem**

```
AT+QADBKEY="0jXKXQwSwMxYoeg"
OK
```

The key is stored on modem NVRAM and survives reboots and firmware upgrades.

**Step 4 — Enable the ADB interface in the USB composition**

```
AT+QCFG="usbcfg"
+QCFG: "usbcfg",0x2C7C,0x0801,1,1,1,1,1,0,0

AT+QCFG="usbcfg",0x2C7C,0x0801,1,1,1,1,1,1,0
AT+CFUN=1,1
```

Field order: `VID, PID, DIAG, NMEA, AT, MODEM, NET, ADB, UAC`. The only
change is the `ADB` field (penultimate): `0` → `1`. Reboot takes effect.

After reboot, `adb devices` should see the modem.

### Original Contributors

* [hornetfighter515](https://github.com/hornetfighter515) — Basic script structure and debugging.
* [Ryan Bradley](https://github.com/rbradley0) – Tweaking and debugging.
* [carp4](https://github.com/carp4) — RM5XX support, direct AT+QADBKEY? entry.
* [iamromulan](https://github.com/iamromulan) — Remove sudo requirement.
* [igem](https://xnux.eu/devices/feature/qadbkey-unlock.c) – Original source code.
