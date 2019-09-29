# ootr-stats
Scripts to process Ocarina of Time Randomizer spoiler logs for statistical analysis

## Requirements
* Python 3.x
* MSSQL 2016+ compatible database (SQL Server Express)
* (Optional) SQL Server Management Studio

## Usage

These scripts are a mess. Unless you want to check different settings, just use the spreadsheet [here](https://docs.google.com/spreadsheets/d/1rHg-Qf86kY9sjYbnLbJL0D-XBcpEWvJLDpIXhvVKUyg/edit?usp=sharing) for analysis.

1. Check out copies of the randomizer from [here](https://github.com/testrunnersrl/OoT-Randomizer). For the fall settings poll use the 5.1 release tag.
2. Update relative path to the randomizer root folder near the top of the following files:
    1. ext_hints_mssql.py
    2. dbUpdate.py
3. Create the database where spoiler data will be stored
4. Edit connection information near the top of the following files:
    1. ext_spoiler_mssql.py
    2. ext_hints_mssql.py
    3. dbUpdate.py
5. Save pre-generated spoiler logs somewhere and update the folder path in the following files:
    1. ext_spoiler_mssql.py
    2. ext_hints_mssql.py
6. 

## Limitations
* Assumes no MQ dungeons
* Assumes no sanities (key, scrub, shop, skull, cow, bean)
* Sphere analysis does not consider advanced tricks/out-of-logic checks
