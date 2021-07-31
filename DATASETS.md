# The Datasets

## Data Locations

| Name       | File name      | URL   |
| ---------- | -------------- | ----- |
| EMSHR Lite | emshr_lite.txt | (https://www.ncdc.noaa.gov/homr/file/emshr_lite.txt) |

## EMSHR Lite

### Field Descriptions

| Name         | Description                                  | Extracted? |
| ----         | -----------                                  | ---------- |
| NCDC         | Unique station identifier                    | Yes        |
| BEG_DT       | Begin date for physical location of station. | Yes        |
| BEG_DT       | End date for physical location of station.   | Yes        |
| STATION_NAME | Station name.                                | Yes        |
| COOP         | Numerical identifier within the COOP network.| No         |                                | Yes |

### Interesting Things

1. Some station names include encoded unicode characters. The resulting field expansion throws off the fixed column widths upon which the value parser depends. Examples include: UTQIAGVIK, ESPANOL, PREVOST, QUEBEC and MONTREAL. These names have been converted to ASCII.
1. There are a number of records without lat/long as they are high altitude balloon records. The coordinates are set to (None, None).
1. Some date ranges have inverted orders for beginning and end dates. This seems to affect Colorado stations.
1. The location records are sorted by date range and are generally contiguous, though there are the occasional gaps in time coverage.
1. There are a couple of hundred duplicate location records. These have been removed by deleting the prior record with the same date range. Some stations even have multiple duplicates.
1. Coordinates have variable significant figures. They often vary in location slightly, even though the history indicates no physical move took place. 
1. Some locations have dates that show digit swaps.

### Statistics

```
Station count: 144597
Location count: 276373
Valid period count: 144561
```

There were 386 records that failed the valid periods test.
When duplicate records were removed the failures dropped to 36 records. 