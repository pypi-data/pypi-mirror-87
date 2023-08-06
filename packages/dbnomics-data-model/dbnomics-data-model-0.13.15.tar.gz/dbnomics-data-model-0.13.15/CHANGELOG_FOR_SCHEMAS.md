# Changelog for JSON schemas

Starting from version 0.8.1, the versions of the schemas are different than the version of the Python package.

## provider.json

### 0.8 -> 0.9.0
Breaking changes
- remove `notes` property; use `description` instead


## dataset.json

### 0.8.1 -> 0.9.0
Breaking changes
- remove `notes` property; use `description` instead

### 0.9.0 -> 0.9.1
Non-breaking changes
- re-add `notes` property; complementary of `description` property


## series.json

### 0.8 -> 0.9.0
Breaking changes
- remove `notes` property; use `description` instead

Non-breaking changes
- add `attributes`, `description`, `doc_href`, `next_release_at`, `updated_at` properties
    - example: see [here](./tests/fixtures/provider3-json-data/dataset1/dataset.json)

### 0.9.0 -> 0.9.1
Non-breaking changes
- re-add `notes` property; complementary of `description` property
