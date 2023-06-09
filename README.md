## Prerequisites

Run in raspberrypi, python 3.7.0

```
sudo apt-get install python-rpi.gpio python3-rpi.gpio
```

Install requirements:
```commandline
pip install -r requirements.txt
```
or
```commandline
pip3 install -r requirements.txt
```

## Run

* For simulation, comment out the raspberry pi specific imports and run with flag `--simulate`

```commandline
python runner.py --simulate
```

* Otherwise, leave code as is and run

```commandline
python runner.py
```

