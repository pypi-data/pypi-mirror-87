[![PyPi version](https://pypip.in/v/python-backup/badge.png)](https://pypi.org/project/python-backup/)
[![PyPi downloads](https://pypip.in/d/python-backup/badge.png)](https://pypi.org/project/python-backup/)
# python-backup
Configuration file based file backup

## Installation
`pip install python-backup`

## Usage
`backup [config-path]`

## Configuration
python-backup assumes the following folder structure:
```
/etc/
  backup.d/
    backup.yml
    sources.d/
      *.yml
```
For examples see the [etc](etc) folder.

## Features
- rdiff-backup back end
- Backup dependency chains
- Multithreaded
- YAML config files
- pre/post hooks for each backup job

## Known deficiencies
- Infinity loops from bad dependency chains
