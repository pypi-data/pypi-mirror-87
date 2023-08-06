# cmstool

![snr](./images/snr_example.png)

Cable Modem Statistics Tool 

## Introduction

`cmstool` can be used to generate SNR and Power statistics for cable modems by scraping this data from modem's Web UI interface. The statistics generated can help to identify a source of interference in one or multiple DOCSIS channels, that could lead to a degradation of the downstream signal.

The tool is composed by two main scripts:

* `cmsraper`: command line tool used to scrape SNR and Power values from cable modem's Web UI interface and store them in a `.csv` file.

* `cmstats`: command line tool used to parse `.csv` file and generate statistics.

## Requirements

- Python 3.x
- Pip
- Docker (for cmstats)

## Supported devices

For this beta version just only one:

- Technicolor DPC3848VE

## Installation

`cmscraper` can be installed using pip:
```
pip install cmstool
```

`cmstats` can be executed using Docker. You can find the docker image in dockerhub 

## Usage

Just run the tool with `--help` argument to get a list of supported commands:
```
$ cmscraper_cli --help
usage: cmscraper_cli [-h] [-d DEVICE_NAME] [-i MODEM_IP_ADDRESS] [-o OUTPUT_PATH] [-t HTTP_TIMEOUT]

A Python tool that extracts statistics data from modem status web page.

optional arguments:
  -h, --help           show this help message and exit
  -d DEVICE_NAME       Device Name (Supported devices: technicolor-dpc384ve)
  -i MODEM_IP_ADDRESS  Modem IP Address (Default: 192.168.0.1)
  -o OUTPUT_PATH       Output path to store statistics
  -t HTTP_TIMEOUT      HTTP Client Timeout (Default: 10s)
```

### Example
Now, supposing your modem's gateway `is 192.168.0.1`, try to scrap some data to `./stats` folder:

```
$ cmscraper_cli -d technicolor-dpc384ve -o ./stats
```

Check `./stats` directory, you should see a list of `.csv` files (one per channel):
```
$ls -lha ./stats
drwxr-xr-x  27 cgm  staff   864B Dec  7 00:12 .
drwxr-xr-x  23 cgm  staff   736B Dec  7 00:07 ..
-rw-r--r--   1 cgm  staff    92B Nov 22 20:08 0.csv
-rw-r--r--   1 cgm  staff   134B Dec  7 00:11 1.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 10.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 11.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 12.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 13.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 14.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 15.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 16.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 17.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 18.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 19.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 2.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 20.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 21.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 22.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 23.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 24.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 3.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 4.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 5.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 6.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 7.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 8.csv
-rw-r--r--   1 cgm  staff    88B Nov 22 20:08 9.csv
```

Have a look at one of those:
```
cat stats/14.csv
1606075264,3.4,37.63
1606076909,3.5,37.35
1606086304,5.0,37.35
1606086513,5.0,37.35
```

Each row contains the following columns: `timestamp`, `snr`, `power`

You should be ready to get some statistics using `cmstats` cli tool:

```
docker run -it --rm -p 8888:8888 -v ${PWD}/stats:/opt/cmstats/data  cmstats_cli --chr 0 24
```

The above will execute cmstats cli tool and map `./stats` folder to `/opt/cmstats/data` on your container 
(the default path containing the your `.csv` files) and parse channel range through 0 to 24. 

**Note**: channel `0` is the average value of the whole set of channels.

Expected results:

```
Ch 00: PWR avg: 03.82 dBmV / PWR std: 00.66 - SNR avg: 37.08 dB  / SNR std: 00.04
Ch 01: PWR avg: 02.67 dBmV / PWR std: 00.75 - SNR avg: 36.53 dB  / SNR std: 00.11
Ch 02: PWR avg: 04.97 dBmV / PWR std: 00.47 - SNR avg: 37.54 dB  / SNR std: 00.13
Ch 03: PWR avg: 04.60 dBmV / PWR std: 00.50 - SNR avg: 37.44 dB  / SNR std: 00.13
Ch 04: PWR avg: 04.87 dBmV / PWR std: 00.47 - SNR avg: 37.44 dB  / SNR std: 00.13
Ch 05: PWR avg: 04.37 dBmV / PWR std: 00.47 - SNR avg: 37.44 dB  / SNR std: 00.13
Ch 06: PWR avg: 04.50 dBmV / PWR std: 00.50 - SNR avg: 37.54 dB  / SNR std: 00.13
Ch 07: PWR avg: 04.43 dBmV / PWR std: 00.52 - SNR avg: 37.44 dB  / SNR std: 00.13
Ch 08: PWR avg: 04.07 dBmV / PWR std: 00.47 - SNR avg: 36.95 dB  / SNR std: 00.48
Ch 09: PWR avg: 04.43 dBmV / PWR std: 00.52 - SNR avg: 37.54 dB  / SNR std: 00.13
Ch 10: PWR avg: 04.63 dBmV / PWR std: 00.66 - SNR avg: 37.44 dB  / SNR std: 00.13
Ch 11: PWR avg: 04.63 dBmV / PWR std: 00.66 - SNR avg: 37.54 dB  / SNR std: 00.13
Ch 12: PWR avg: 04.63 dBmV / PWR std: 00.73 - SNR avg: 37.44 dB  / SNR std: 00.13
Ch 13: PWR avg: 04.40 dBmV / PWR std: 00.71 - SNR avg: 37.54 dB  / SNR std: 00.13
Ch 14: PWR avg: 04.50 dBmV / PWR std: 00.71 - SNR avg: 37.35 dB  / SNR std: 00.00
Ch 15: PWR avg: 04.07 dBmV / PWR std: 00.75 - SNR avg: 37.35 dB  / SNR std: 00.00
Ch 16: PWR avg: 03.83 dBmV / PWR std: 00.73 - SNR avg: 36.93 dB  / SNR std: 00.31
Ch 17: PWR avg: 03.77 dBmV / PWR std: 00.75 - SNR avg: 36.86 dB  / SNR std: 00.35
Ch 18: PWR avg: 03.30 dBmV / PWR std: 00.78 - SNR avg: 36.61 dB  / SNR std: 00.00
Ch 19: PWR avg: 02.97 dBmV / PWR std: 00.75 - SNR avg: 36.46 dB  / SNR std: 00.11
Ch 20: PWR avg: 03.03 dBmV / PWR std: 00.80 - SNR avg: 36.46 dB  / SNR std: 00.11
Ch 21: PWR avg: 02.53 dBmV / PWR std: 00.80 - SNR avg: 36.46 dB  / SNR std: 00.11
Ch 22: PWR avg: 02.13 dBmV / PWR std: 00.80 - SNR avg: 36.61 dB  / SNR std: 00.00
Ch 23: PWR avg: 02.43 dBmV / PWR std: 00.80 - SNR avg: 36.53 dB  / SNR std: 00.11
Ch 24: PWR avg: 01.90 dBmV / PWR std: 00.85 - SNR avg: 36.46 dB  / SNR std: 00.11

Serving to http://0.0.0.0:8888/    [Ctrl-C to exit]
172.17.0.1 - - [07/Dec/2020 03:23:43] "GET / HTTP/1.1" 200 -
```

From the above listing you could already arrive to a conclusion just by looking at the standard deviation value (SNR std), 
but if you want 

