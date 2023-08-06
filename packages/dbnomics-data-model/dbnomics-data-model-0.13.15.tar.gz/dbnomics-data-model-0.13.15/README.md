# DBnomics data model

Define, validate and transform DBnomics data.

For a quick schematic look at the data model, please read the [cheat_sheet.md](./cheat_sheet.md) file.
If you are a developer working on fetchers, you can print it!

See also [these sample directories](./tests/fixtures).

Note: The `✓` symbol means that a constraint is validated by the [validation script](./dbnomics_data_model/validate_storage.py).

## Entities and relationships

```
provider -> dataset -> time series -> observations
```

- Each provider contains datasets
- Each dataset contains time series
- Each time series contains observations
- Each observation is a tuple like `(period, value, attribute1, attribute2, ..., attributeN)`, where attributes are optional

Note: the singluar and plural forms of "time series" are identical (cf [Wiktionary](https://en.wiktionary.org/wiki/time_series)).

## Storage

DBnomics data is stored in regular directories of the file-system.

A directory containing data from a provider converted by a fetcher.

- ✓ The directory name MUST be `{provider_code}-json-data`.

## Revisions

Each storage directory is versioned using Git in order to track revisions.

## General constraints

### Minimal data

Data MUST NOT be stored if it adds no value or if it can be computed from any other data.

As a consequence:

- series names MUST NOT be generated when not provided by source data;

DBnomics can generate a name from the dimensions values codes

### Data stability

Any commit in the storage directory of a provider MUST reflect a change from the side of the provider.

Data conversions MUST be stable: running a conversion script on the same source-data MUST NOT change converted data.

As a consequence:

- when series codes are generated from a dimensions `dict`, always use the same order;
- properties of JSON objects MUST be sorted alphabetically;

## `/provider.json`

This JSON file contains meta-data about the provider.

See [its JSON schema](./dbnomics_data_model/schemas/v0.8/provider.json).

## `/category_tree.json`

This JSON file contains a tree of categories whose leaves are datasets and nodes are categories.

This file is optional:

- if categories are provided by source data, it SHOULD exist;
- if it's missing, DBnomics will generate the tree as a list of datasets ordered lexicographically;
- it MUST NOT be written if it is identical to the generated list mentioned above (due to the general constraint about minimal data)

See [its JSON schema](./dbnomics_data_model/schemas/v0.8/category_tree.json).

## `/{dataset_code}/`

This directory contains data about a dataset of the provider.

- The directory name MUST be equal to the dataset code.

## `/{dataset_code}/dataset.json`

This JSON file contains meta-data about a dataset of the provider.

See [its JSON schema](./dbnomics_data_model/schemas/v0.8/dataset.json).

The `series` property if optional: see [storing time series](#storing-time-series) section.

## `/{dataset_code}/series.jsonl`

This [JSON-lines](http://jsonlines.org/) file contains meta-data about time series of a dataset of a provider.

Each line is a JSON object validated against [this JSON schema](./dbnomics_data_model/schemas/v0.8/series.json).

This file is optional: see [storing time series](#storing-time-series) section.

## `/{dataset_code}/{series_code}.tsv`

This [TSV](https://en.wikipedia.org/wiki/Tab-separated_values) file contains observations of a time series of a dataset of a provider.

These files are optional: see [storing time series](#storing-time-series) section.

## Constraints on time series

- With providers using series codes composed of dimensions values codes:
  - The separator MUST be '.' to be compatible with series codes masks. It is allowed to change the separator used originally by the provider. Example: [this commit on BIS](https://git.nomics.world/dbnomics-fetchers/bis-fetcher/commit/dce6f0caf32762aa859f657467161a397a9b60f6).
  - The parts of the series code MUST follow the order defined by `dimensions_codes_order`. Example: if `dimensions_codes_order = ["FREQ", "COUNTRY"]`, the series code MUST be `A.FR` and not `FR.A`.
  - When dimensions codes order is not defined by the provider, the lexicographic order of the dimensions codes SHOULD be used, and the `dimensions_codes_order` key MUST NOT be written. Example: if dimensions are `FREQ` and `COUNTRY`, the series code is `FR.A` because dimensions codes are sorted alphabetically: `["COUNTRY", "FREQ"]`.

## Constraints on TSV files

Note: The `✓` symbol means that a constraint is validated by the [validation script](./dbnomics_data_model/validate_storage.py).

- TSV files MUST be encoded in UTF-8.
- ✓ The two first columns of the header MUST be named `PERIOD` and `VALUE`.
- ✓ Each row MUST have the same number of columns than the header.
- The values of the `PERIOD` column:
  - ✓ MUST respect a specific format:
    - `YYYY` for years
    - `YYYY-MM` for months (MUST be padded for `MM`)
    - `YYYY-MM-DD` for days (MUST be padded for `MM` and `DD`)
    - `YYYY-Q[1-4]` for year quarters
      - example: `2018-Q1` represents jan to mar 2018, and `2018-Q4` represents oct to dec 2018
    - `YYYY-S[1-2]` for year semesters (aka bi-annual, semi-annual)
      - example: `2018-S1` represents jan to jun 2018, and `2018-S2` represents jul to dec 2018
    - `YYYY-B[1-6]` for pairs of months (aka bi-monthly)
      - example: `2018-B1` represents jan + feb 2018, and `2018-B6` represents nov + dec 2018
    - `YYYY-W[01-53]` for year weeks (MUST be padded)
  - ✓ MUST all have the same format
  - ✓ MUST NOT include average values, like `M13` or `Q5` periods (some providers do this)
  - MUST be consistent with the frequency (ie use `YYYY-Q[1-4]` for quarterly observations, not `YYYY-MM-DD`, even if those daily periods have 3 months between them)
- ✓ The `PERIOD` column MUST be sorted in an ascending order.
- ✓ The values of the `VALUE` column MUST either:
  - follow that of decimal in [XMLSchema](https://www.w3.org/TR/xmlschema-2/#decimal): a non-empty finite-length sequence of decimal digits separated by a period as a decimal indicator. An optional leading sign is allowed. If the sign is omitted, "+" is assumed. Leading and trailing zeroes are optional. If the fractional part is zero, the period and following zero(es) can be omitted. For example: '-1.23', '12678967.543233', '+100000.00', '210'.
  - OR be `NA` meaning "not available".
- TSV files CAN have supplementary columns in order to tag some observation values.
  - The values of these columns are free, empty string `""` means no tag
  - Reuse values defined by the provider if possible; otherwise define values with DBnomics team

## Storing time series

### Meta-data

Time series meta-data can be stored either:

- in `{dataset_code}/dataset.json` under the `series` property as a JSON array of objects
- in `{dataset_code}/series.jsonl`, a [JSON-lines](http://jsonlines.org/) file, each line being a (non-indented) JSON object

When a dataset contains a huge number of time series, the `dataset.json` file grows drastically. In this case, the `series.jsonl` format is recommended because parsing a JSON-lines file line-by-line consumes less memory than opening a whole JSON file. A maximum limit of 1000 time series in `dataset.json` is recommended. In this case, the `series` key of `dataset.json` file should be: `{'path': 'series.jsonl'}`.

Whatever format you choose, the JSON objects are validated against [this JSON schema](./dbnomics_data_model/schemas/v0.8/series.json).

Constraints additional to the schema:

- ✓ The `code` properties of the series list MUST be unique

Examples:

- [this dataset](./tests/fixtures/provider1-json-data/dataset1) stores time series meta-data in `dataset.json` under the `series` property
- [this dataset](./tests/fixtures/provider2-json-data/dataset1) stores time series meta-data in `series.jsonl`

### Dimensions values order

Sometimes the dimensions values order is different than the lexicographic one.

Example: for the dimension "country", we have "All countries [ALL]", "Afghanistan [AF]" "France [FR]", "Germany [DE]", "Other countries [OTHER]". In this case it seems more natural to display "All countries" first, and "Other countries" last. We don't want "Afghanistan" to come before "All countries" just because of lexicographic order.

It is possible to encode this order in `dataset.json` like this:

```json
{
  "dimensions_values_labels": {
    "country": [
      ["ALL", "All countries"],
      ["AF", "Afghanistan"],
      ["FR", "France"],
      ["DE", "Germany"],
      ["OTHER", "Other countries"]
    ]
  }
}
```

Another case is when the dimensions values talk about units, and we want to order units from the smallest to the largest. For example, "millimeter", "centimeter", "meter", "kilometer".

### Series attributes

In conjunction with dimensions, series can have `attributes`. They behave like dimensions: labels and codes.

Example: (from provider1-json-data/dataset2/dataset.json)

- in `dataset.json`:

```json
  "attributes_labels": {
      "UNIT_MULT": "Unit of multiplier"
  },
  "attributes_values_labels": {
      "UNIT_MULT": {
          "9": "× 10^9"
      }
  },
```

- then, for each series (in dataset.json or series.jonl files)

```json
  "attributes": {
      "UNIT_MULT": "9"
  },

```

### Observations

Time-series observations can be stored either:

- in `{dataset_code}/{series_code}.tsv` [TSV](https://en.wikipedia.org/wiki/Tab-separated_values) files
- in `{dataset_code}/series.jsonl`, a [JSON-lines](http://jsonlines.org/) file, each line being a (non-indented) JSON object, under the `observations` property of each object.

When a dataset contains a huge number of time series, the number of TSV files file grows drastically. In this case, the `series.jsonl` format is recommended because a single file consumes less disk space than thousands of files (each file taking some kilo-bytes in the file-system table of contents), and because Git is slower when the number of committed files increases. A maximum limit of 1000 TSV files is recommended.

Whatever format you choose, the JSON objects are validated against [this JSON schema](./dbnomics_data_model/schemas/v0.8/series.json).

Examples:

- [this dataset](./tests/fixtures/provider2-json-data/dataset1) stores observations in TSV files
- [this dataset](./tests/fixtures/provider2-json-data/dataset2) stores observations in `series.jsonl`

## Adding documentation to data (description and notes fields)

Datasets and series can be documented using `description` and `notes` fields.

- `description` presents what is the meaning of the data
- `notes` presents some remarks about the data. Example: "Before March 2002, exposures were netted across the banking and trading books. This has necessitated a break in the series."

=> see [this example](tests/fixtures/provider3-json-data/dataset1/dataset.json)

## Data validation

dbnomics-data-model comes with a validation script. Validate a JSON data directory:

```sh
dbnomics-validate <storage_dir>

# for example:
dbnomics-validate wto-json-data
```

Note that some of the constraints expressed above are not yet checked by the validation script.

Some errors are warnings and are not displayed by default. Use the `--developer-mode` option to display all errors.

## Testing

Run unit tests:

```sh
python setup.py test
```

Code quality:

```sh
pylint --rcfile ../code-style/pylintrc *.py dbnomics_data_model
```

See also: https://git.nomics.world/dbnomics-fetchers/documentation/wikis/code-style

Run validation script against dummy providers:

```bash
dbnomics-validate tests/fixtures/provider1-json-data
dbnomics-validate tests/fixtures/provider2-json-data
```

## Changelog

See [CHANGELOG.md](./CHANGELOG.md). It contains an upgrade guide explaining how to modify the source code of your fetcher, if the data model changes in unexpected ways.

## Publish a new version

For package maintainers:

```bash
git tag x.y.z
git push
git push --tags
```

GitLab CI will publish the package to https://pypi.org/project/dbnomics-data-model/ (see [`.gitlab-ci.yml`](./.gitlab-ci.yml)).
