# Changelog

## next

## 0.13.15

Non-breaking changes:

- Fix series alignment with periods having day format ([#709](https://git.nomics.world/dbnomics-fetchers/management/-/issues/709))

## 0.13.14

Non-breaking changes:

- Handle releases metadata for each provider, defining a list of release codes for each dataset. ([#755](https://git.nomics.world/dbnomics-fetchers/management/-/issues/755))
- Validate releases in validation script.

## 0.13.13

Non-breaking changes:

- Do not fail if offset is wrong during `iter_observations_by_seeking` reading a `series.jsonl` file. This happens when there are obsolete series Solr documents. ([#761](https://git.nomics.world/dbnomics-fetchers/management/-/issues/761))

## 0.13.12

Non-breaking changes:

- Allow `:` character in dataset codes ([#41](https://git.nomics.world/dbnomics/dbnomics-data-model/-/merge_requests/41))

## 0.13.11

Non-breaking changes:

- Switch from `orjson` to Python standard library `json` module ([#39](https://git.nomics.world/dbnomics/dbnomics-data-model/-/merge_requests/39))
- Switch to setuptools_scm to read version from Git tags ([#38](https://git.nomics.world/dbnomics/dbnomics-data-model/-/merge_requests/38))

## 0.13.10

Non-breaking changes:

- Switch from `ujson` to `orjson` ([#37](https://git.nomics.world/dbnomics/dbnomics-data-model/-/merge_requests/37))

## 0.13.9

Non-breaking changes:

- Fix weeks handling (cf https://git.nomics.world/dbnomics-fetchers/management/issues/635)

## 0.13.8

Non-breaking changes in validation script:

- Make `dataset-not-found-in-category-tree` error a warning

## 0.13.7

Non-breaking changes in validation script:

- Make `no-observations` error a warning

## 0.13.6

Non-breaking changes in validation script:

- Add `--developer-mode` option which (false by default), if not used, ignores some errors like `duplicated-series-name`
- Fix a crash when dataset code is not defined in data
- Add new `duplicated-observations-period` check

## 0.13.5

Non-breaking changes in validation script:

- Fix validation script when series has no observations or observations file is empty (cf https://git.nomics.world/dbnomics-fetchers/management/issues/558)

## 0.13.4

Non-breaking changes in validation script:

- Fix error code and message (mentioned in [this comment](https://git.nomics.world/dbnomics-fetchers/management/issues/483#note_10815))

## 0.13.3

Non-breaking changes in Python API:

- Fix another case for https://git.nomics.world/dbnomics-fetchers/management/issues/478

## 0.13.2

Non-breaking changes in Python API:

- Fix https://git.nomics.world/dbnomics-fetchers/management/issues/478

## 0.13.1

Non-breaking changes in validation script:

- Rename error code `duplicate-series-name` to `duplicated-series-name`
- Check category_tree datasets synchronisation
- Implement "discontinued" dataset proposal
- Don't emit `dataset-not-found-in-category-tree` if the dataset is discontinued
- Fix misc errors

## 0.13.0

Breaking changes in Python API:

- `AbstractDatasetDir.iter_observations` yields tuples like `(exception, series_code, observations)`, allowing the caller to get data loading errors.

## 0.12.10 -> 0.12.11

Non-breaking changes:

- in `FileSystemDatasetDir.iter_observations_from_jsonl`, load series from JSON-lines by scanning if seeking fails

## 0.12.9 -> 0.12.10

Non-breaking changes:

- fix series name generation

## 0.12.8 -> 0.12.9

Non-breaking changes in validation script:

- disable checking duplicate dimensions values labels in the same dimension
  - as a consequence: enhance series name generation to dedupe series that would have 2 different values for a dimension, having the same label
- use whitelist instead of blacklist for series codes validation

## 0.12.7 -> 0.12.8

Non-breaking changes in validation script:

- fix return code

## 0.12.6 -> 0.12.7

Non-breaking changes:

- Set dimensions_codes_order if not defined in `dataset.json`.

## 0.12.5 -> 0.12.6

- configure continuous integration to validate DBnomics data

Changes in `dbnomics-validate` script:

- add `--only-datasets` option
- put values of error messages in context dict
- fix bugs

## 0.12.4 -> 0.12.5

- fix bug: don't fail during series completion
- add `to_dimension_code` method to `observations.Frequency`

## 0.12.3 -> 0.12.4

Add `include_package_data=True` to `setup.py` to distribute schemas JSON files.

## 0.12.2 -> 0.12.3

Changes in `dbnomics-validate` script:

- rename "json" choice of `--format` option to "jsonl"
- enhance output formatting
- add summary of error types
- fix line numbers in error messages
- clarify error codes

## 0.12.1 -> 0.12.2

Soften dependencies to ease installation.

## 0.12.0 -> 0.12.1

Install validation script as `dbnomics-validate`.

## 0.11.0 -> 0.12.0

Breaking changes in schemas:

- `dataset.json`: make empty `dimensions_values_labels` values invalid

Breaking changes in validation script:

- validation script: make duplicate series names invalid

## 0.10.1 -> 0.11.0

Non-breaking changes:

- improve validation script: display errors location more precisely

Breaking changes in Python API:

- `StorageError` class now stores which provider/dataset/series is concerned.
- Low-level functions in `dbnomics_data_model.git` and `dbnomics_data_model.filesystem` now return `None` or a value, and higher-level methods raise exceptions.
- `dbnomics_data_model.iter_storages` handles `StorageError` exceptions and yields them (so the yielded tuple is now `(storage, series_codes_by_dataset_code, error)`).

## 0.10.0 -> 0.10.1

Non-breaking changes in Python API:

- remove some calls to `warnings.warn` which were used to notify about errors loading files, but keep calls used to notify deprecations.

## 0.9.1 -> 0.10.0

Breaking changes in Python API (`dbnomics_data_model.observations`):

- change the signature of `detect_frequency`, `detect_period_format`, `detect_period_format_strict` and `normalize_observations` to return a `Frequency` enum instance instead of a `str`
- change the signature of `period_to_start_day` to return a `date` instead of a `str`

Non-breaking changes in Python API (`dbnomics_data_model.observations`):

- add new functions: `iter_periods_dates`, `next_period_date`, `complete_series`, `complete_series_list` and `start_day_to_period`, `series_obs_to_json`
- add a new `Frequency` enum classes

## 0.9.0 -> 0.9.1

Non-breaking changes in Python API:

- add `period_to_start_day` function to `dbnomics_data_model.observations`

## 0.8.3 -> 0.9.0

Drop SQLite support, use Solr to index offsets.

Breaking changes in Python API:

- `AbstractDatasetDir.iter_observations`, `AbstractDatasetDir.iter_observations_from_jsonl` and `AbstractDatasetDir.iter_observations_from_tsv` now yield tuples like `(series_code, file_path, observations)`.
- Storages do not use SQLite anymore:
  - module `dbnomics_data_model.storages.indexes` is deleted
  - `AbstractDatasetDir.iter_observations` now takes an optional argument `offset_by_series_code`.

Non-breaking changes in Python API:

- 2 methods added to `AbstractDatasetDir`: `series_id` and `series_id_str`.

## 0.8.2 -> 0.8.3

Validation script improvements:

- check that the `code` properties of the series meta-data are unique (in `dataset.json` or `series.jsonl`)
  - example: tests/fixtures/provider1-json-data/dataset3/dataset.json

## 0.8.1 -> 0.8.2

- add period format for bi-monthly observations (every 2 months): `YYYY-B[1-6]`
  - example: `2018-B1`, `2018-B6`

## 0.8.0 -> 0.8.1

- allow `dimensions_values_labels` (property of `dataset.json`) to contain ordered list of values when lexicography sort is not appropriate:

```json
{
  "dimensions_values_labels": {
    "geo": [
      ["fr", "France Métropolitaine"],
      ["dom", "DOM"],
      ["autres", "Autres"]
    ]
  }
}
```

Python API:

- new `get_dimensions_values_labels` function in `datasets.py`

## 0.7.9 -> 0.8.0

- introduce an abstraction for storage directories via `GitStorage` and `FileSystemStorage` classes
- add semantic versioning version numbers to JSON schemas

## 0.7.8 -> 0.7.9

- add `updated_at` (optional) property to `dataset.json` schema

## 0.7.7 -> 0.7.8

- introduce new name for category tree: `category_tree.json` and deprecate `categories_tree.json`

## 0.7.5 -> 0.7.6

- add `attribution` (optional) property to `provider.json` schema

## 0.7.4 -> 0.7.5

- add `source_href` (optional) property to `dataset.json` schema

## 0.7.3 -> 0.7.4

- allow categories with only a name, only a code, or both

## 0.7.2 -> 0.7.3

- allow "notes" property for provider and dataset
- check that JSON repo dirname ends with "-json-data"

## 0.7.1 -> 0.7.2

- add `definition` property to categories tree and provider

## 0.7 -> 0.7.1

- rename `tree_sample` to `tree-sample`
- allow `next_release_at` to `dataset.json`
- allow `notes` to `provider.json` and `dataset.json`

## 0.6 -> 0.7

- categories directories were removed: now datasets are stored at the root of the repository
- new `categories_tree.json` (see [schema](/dbnomics_data_model/schemas/categories_tree.json) and [sample](/dbnomics_data_model/samples/categories_tree.json)): it stores the categories tree and the datasets codes and names.
- new `datapackage.json` (see [sample](/dbnomics_data_model/samples/datapackage.json)): it stores the version number of the data model which the fetcher followed when writing the files
- series directories were removed: `observations.tsv` were renamed to `<series_code>.tsv` and `series.json` files were included in `dataset.json` under a `series` property.

Python API changes:

- `validators.validate_category` and `validators.get_category_validation_errors` functions were removed because `category.json` files do not exist anymore
- `validators.validate_series` and `validators.get_series_validation_errors` functions were removed because `series.json` files do not exist anymore
- `validators.validate_categories_tree` and `validators.get_categories_tree_validation_errors` functions were added to validate the new `categories_tree.json` file
