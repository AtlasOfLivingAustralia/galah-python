## 0.11.1 (2025-02-21)

### Fix

- **fixes-to-code-on-website**: fixed bugs found in the code on the galah website

## 0.11.0 (2025-02-20)

### Feat

- **all-package-update**: updated APIs for most atlases; added option for custom config file; fixed occurrences for most atlases

## 0.10.0 (2024-10-23)

### Feat

- **added-ability-to-mint-a-DOI**: added ability to mint a doi

### Fix

- **fixed-atlas_media-so-it-correctly-downloads-images**: fixed atlas_media so it correctly downloads images
- **corrected-typo-in-poetry.lock**: corrected typo in poetry file
- **updated-poetry-file-again**: updated poetry file again to fix security issue
- **changed-version-of-idna-in-poetry.lock**: changed version of idna
- **fixing-documentation-and-updating-show_all-functions**: fixing documentation and updating show_all functions

## 0.9.1 (2024-05-20)

### Perf

- **add-0.8.2-distributions**: add distributions

## 0.9.0 (2024-05-20)

### Perf

- **add-0.8.2-distributions**: add distributions

## 0.9.0 (2024-04-11)

### Feat

- **added-guatemalan-and-swedish-atlases**: added guatemalan and swedish atlases

## 0.8.3 (2024-03-08)

### Fix

- **galah_select.py**: fixed galah_select to have the correct string representation of fields

## 0.8.2 (2024-02-13)

### Fix

- **show_all.py**: changed name of list id from dataResourceUid to species_list_uid

## 0.8.1 (2023-12-20)

### Fix

- **removed-a-check-that-was-impeding-galah_geolocate**: removed a check that was impeding galah_geolocate

## 0.8.0 (2023-12-18)

### Feat

- **added-ability-to-simplify-polygons-by-drawing-bounding-box-around-polygon**: added ability to simplify polygons by drawing bounding box around polygon
- **adding-ability-to-buffer-regions,-as-well-as-choose-your-coordinate-reference-system**: adding ability to buffer regions, as well as choose your coordinate reference system
- **Added-ability-for-users-to-add-a-buffer-region-around-a-shape-file-for-atlas_counts,-atlas_species-and-atlas_occurrences**: Added ability for users to add a buffer region around a shape file for atlas_counts, atlas_species and atlas_occurrences

### Fix

- **fixed-the-ability-to-get-warned-about-homonyms-and-search-for-the-correct-name**: fixed the ability to get warned about homonyms and search for the correct name
- **fixed-a-bug-in-galah_group_by-for-expand=True-option**: fixed a bug in galah_group_by for expand=True option
- **fixed-a-bug-in-galah_group_by-where-the-data-quality-filter-wasn't-working**: fixed a bug in galah_group_by where the data quality filter wasn't working
- **changed-default-fields-to-only-8-but-kept-option-for-having-all-of-them**: changed default fields to only 8 but kept option for having all of them
- **fixed-a-bug-where-the-wrong-URL-was-being-given-for-an-expand=True-option-for-the-ALA**: fixed a bug where the wrong URL was being given for an expand=True option for the ALA
- **remove-unnecessary-keys**: remove unnecessary keys
- **Fixed-a-bug-in-galah_group_by-whereby-data-quality-filter-wasn't-added-correctly**: fixed a bug in galah_group_by whereby data quality filter wasn't added correctly
- **Fixed-galah_filter-to-have-quotes-around-the-filters-so-they-are-recognized-correctly**: Fixed galah_filter to have quotes around the filters so they are recognized correctly

### Refactor

- **Refactored-atlas_media-to-return-correct-metadata-and-be-faster**: Refactored atlas_media to return correct metadata and be faster
- **adding-build-files-and-api-tracker**: adding build files and api tracker

## 0.7.0 (2023-10-12)

### Feat

- **added-ability-in-galah_group_by-to-expand-number-of-groups-to-three**: added ability in galah_group_by to expand number of groups to three

## 0.6.0 (2023-10-04)

## 1.0.0 (2023-10-04)

### Feat

- **adding-new-APIs-and-fixing-a-lot-of-bugs**: adding new apis, fixing lots of bugs, testing out post query
- **Added-new-ALA-API-structure**: Added new ALA API structure, refactored atlas_occurrences

### Fix

- **fixed-a-bug-in-galah_group_by-that-did-not-account-for-empty-payloads-and-fixed-verbose-options**: fixed a bug in galah_group_by that did not account for empty payloads and fixed verbose options
- **fixed-documentation,-a-few-bugs-regarding-indexing-of-results**: fixed documentation, a few bugs regarding indexing of results
- **Adding-commitizen**: Adding commitizen for automatic change logs and versioning

### Refactor

- **Refactored-atlas_counts**: Refactored atlas_counts

## v0.5.0 (2023-06-30)

## v0.1.0 (2023-05-01)
