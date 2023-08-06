# DBnomics Data Package Cheat Sheet

## Tree

```
/
|- category_tree.json # Optional
|- provider.json
|- dataset1
|  |- dataset.json
|  |- A1.B1.C1.tsv
|  |- A1.B1.C2.tsv
|  |- A1.B2.C1.tsv
|  |- A1.B2.C2.tsv
|  |- etc.
|
|- dataset2
|  |- dataset.json
|  |- I1.J1.tsv
|  |- I1.J2.tsv
|  |- etc.
```

## provider.json

```json
{
    "code": "SOB",
    "name": "Statistics Office of Borduria",
    "region": "World",
    "terms_of_use": "https://stats.borduria.org/tos",
    "website": "https://stats.borduria.org/tos"
}
```

## dataset.json

```json
{
    "attributes_labels": {
        "OBS_STATUS": "Observation Status",
    },
    "code": "unemployment",
    "name": "Unemployment in Borduria",
    "next_release_at": "2050-11-01",
    "dimensions_codes_order": [
        "freq",
        "unit",
        "geo"
    ],
    "dimensions_labels": {
        "freq": "Frequency",
        "geo": "Geopolitical entity",
        "unit": "Unit of measure"
    },
    "dimensions_values_labels": {
        "freq": {
            "A": "Annual",
            "M": "Monthly"
        },
        "geo": {
            "AT": "Austria",
            "BE": "Belgium"
        },
        "unit": {
            "MIO_M3": "Million cubic metres",
            "TJ_GCV": "Terajoules (gross calorific value = GCV)"
        }
    },
    "doc_href": "http:\/\/ec.europa.eu\/eurostat\/cache\/metadata\/en\/nrg_12m_esms.htm",
    "series": [
        {
            "code": "M.MIO_M3.AL.4100.AT",
            "dimensions": {
                "FREQ": "M",
                "geo": "AT",
                "partner": "AL",
                "product": "4100",
                "unit": "MIO_M3"
            }
        },
        {
            "code": "M.MIO_M3.AL.4100.BE",
            "dimensions": {
                "FREQ": "M",
                "geo": "BE",
                "partner": "AL",
                "product": "4100",
                "unit": "MIO_M3"
            }
        }
    ]
}
```

## category_tree.json 
#### (not mandatory)

```
[
  {
    "children":[
      {
        "code":"ap",
        "name":"Average Price Data"
      },
      {
        "code":"cw",
        "name":"Urban Wage Earners and Clerical Workers (Current Series)"
      },
      {
        "code":"cu",
        "name":"All Urban Consumers (Current Series)"
      },
      {
        "code":"pc",
        "name":"Industry Data"
      },
      {
        "code":"wp",
        "name":"Commodity Data including \"headline\" FD-ID indexes"
      }
    ],
    "code":"inflation_and_prices",
    "name":"Inflation & Prices"
  },
  {
    "children":[
      {
        "code":"fm",
        "name":"Marital and family labor force statistics"
      },
      {
        "code":"lu",
        "name":"Union Affiliation Data"
      },
      {
        "code":"sm",
        "name":"Employment, Hours, and Earnings - State and Metro Area"
      }
    ],
    "code":"employment",
    "name":"Employment"
  },
  {
    "children":[
      {
        "code":"la",
        "name":"Local Area Unemployment Statistics (LAUS)"
      }
    ],
    "code":"unemployment",
    "name":"Unemployment"
  }
  ]
  ```

  ## Observations.tsv 
```
PERIOD  VALUE
2013    78
2014    75.3

```
- Conventions for observations files
    * File values must me SORTED in ASCENDING Values
    * Remove M13 Q5 S3 W54 
    * Add a `\n` at the end of the file
    * Periods must be consistant and continous
    * File an have an additionnal column

- Conventions for PERIOD
    - `YYYY` for years
    - `YYYY-MM` for months (MUST be padded for `MM`)
    - `YYYY-MM-DD` for days (MUST be padded for `MM` and `DD`)
    - `YYYY-Q[1-4]` for year quarters
    - `YYYY-S[1-2]` for year semesters
    - `YYYY-W[01-53]` for year weeks (MUST be padded)
- Conventions for VALUE
    - decimal with `.`
    - if value is blank write `NA`
