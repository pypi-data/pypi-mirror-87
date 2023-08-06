# microchain
Toolchain for micropython and microcontrollers

Example usage on Debian:
```
apt install micropython

python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

python -m microchain --port /dev/ttyUSB0 project --path example-project deploy
python -m microchain --port /dev/ttyUSB0 mcu terminal
```