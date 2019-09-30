# ootr-stats
Scripts to process Ocarina of Time Randomizer spoiler logs for statistical analysis

## Requirements
* Python 3.x
* MSSQL 2016+ compatible database (SQL Server Express)
* (Optional) SQL Server Management Studio

## Usage

These scripts are a mess. Unless you want to check different settings, just use [the spreadsheet](https://docs.google.com/spreadsheets/d/1rHg-Qf86kY9sjYbnLbJL0D-XBcpEWvJLDpIXhvVKUyg/edit?usp=sharing) for analysis.

1. Check out copies of the randomizer from [the official repo](https://github.com/testrunnersrl/OoT-Randomizer). For the fall settings poll use the 5.1 release tag.
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
6. If you are using anything other than 10000 logs, edit the views in dbUpdate.py with the total number of logs to analyze
7. Run the scripts in the following order. This will take a while.
    1. ext_spoiler_mssql.py
    2. ext_hints_mssql.py
    3. dbUpdate.py

Several views will be generated in the database:
* ad_seeds
    * returns list of seeds requiring OoT logically to complete
    * Spreadsheet checks for Burning Kak instead of OoT for the Stone Bridge + GBK LACS settings
* total_spheres
    * returns total spheres to complete each seed
* woth_area
    * returns list of woth areas as a percent of all seeds
* woth_item_area
    * returns list of woth areas excluding songs as a percent of all seeds
* woth_loc
    * returns list of woth checks as a percent of all seeds
* fool_area
    * returns list of foolish areas as a percent of all seeds
* non_hinted_loc
    * returns list of logically required checks per seed that are not found in any hint (woth or sometimes/always)
    * excludes skulls, keys, songs, beans, ocarinas, light arrows, Zelda's letter, Gerudo card, tunics, shop items, and sphere 0 checks
* checks_per_area
    * intermediate view, calculates checks per area excluding keys
* prog_areas
    * intermediate view, determines medallion/stone dungeons and which are required

The various SQL files in this repo are used to generate most of the tables in the spreadsheet. Filenames should be mostly self-explanatory.

## Limitations
* Assumes no MQ dungeons
* Assumes no sanities (key, scrub, shop, skull, cow, bean)
* Sphere analysis does not consider advanced tricks/out-of-logic checks
* Hint analysis does not go beyond direct hints. WOTH chains are not considered