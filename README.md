# Quectel RM5XX ADBKEY Unlock script

This is a modification of Ryan Bradley's script to support RM5XX Series modems. It works for the RM520N-GL, RM502Q-AE, RM500Q-AE, EM120K-GL, and others.
For more information, see [Getting ADB Access](https://github.com/natecarlson/quectel-rgmii-configuration-notes#getting-adb-access).
This will allow you to replace the Quectel Forums step of the guide with an easier and faster method.

Modified by [carp4](https://github.com/carp4) to allow AT+QADBKEY? to be entered directly and result displayed for RM5XX series modems.

Modified by [iamromulan](https://github.com/iamromulan) to remove the sudo reqirement and query the user to input the AT+QADBKEY? response from the modem.

### Full ADB Unlock Sequence

After generating the key, the full sequence on the modem is:

```
# 1. Get the challenge
AT+QADBKEY?
+QADBKEY: 12345678

# 2. Generate the response (this tool), then submit it
AT+QADBKEY="0jXKXQwSwMxYoeg"
OK

# 3. Check current USB composition
AT+QCFG="usbcfg"
+QCFG: "usbcfg",0x2C7C,0x0801,1,1,1,1,1,0,0

# 4. Enable ADB interface (flip the penultimate field from 0 to 1)
AT+QCFG="usbcfg",0x2C7C,0x0801,1,1,1,1,1,1,0

# 5. Reboot the modem for the composition change to take effect
AT+CFUN=1,1
```

Field order for `AT+QCFG="usbcfg"`: `VID, PID, DIAG, NMEA, AT, MODEM, NET, ADB, UAC`.
The only change is the `ADB` field (penultimate): `0` → `1`.

After reboot, `adb devices` should see the modem. See
[natecarlson's guide](https://github.com/natecarlson/quectel-rgmii-configuration-notes#getting-adb-access)
for the full context.

### How To Use
* To use this script, simply go to the following URL:
https://onecompiler.com/python/3znepjcsq

* Then replace the 12345678 with your responce from AT+QADBKEY? and click run

Your adb unlock key command will be generated under output


Alternatively, download and run the script locally. Python 3.13 removed
the stdlib `crypt` module, so we install the drop-in replacement
[`legacycrypt`](https://pypi.org/project/legacycrypt/) in a venv:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

python3 qadbkey-unlock2.py              # prompts for challenge
python3 qadbkey-unlock2.py 29501379     # or pass it as an arg
```

Older Pythons (<= 3.12) ship `crypt` in stdlib — the venv step is still
recommended but `requirements.txt` becomes a no-op.

Example:
```sh
(.venv) user@host:~$ python3 qadbkey-unlock2.py
Enter the AT+QADBKEY? response: 12345678
AT+QADBKEY="0jXKXQwSwMxYoeg"
```

### Original Contributors

* [hornetfighter515](https://github.com/hornetfighter515) — Basic script structure and debugging.
* [Ryan Bradley](https://github.com/rbradley0) – Tweaking and debugging.
* [igem](https://xnux.eu/devices/feature/qadbkey-unlock.c) – Original source code.