
# Data Product Canvas - Berlin Microcensus Housing Situation

## Metadata

* owner: Open Lifeworlds
* description: Data products providing Berlin microcensus housing situation data on different hierarchy levels
* updated: 2025-11-07

## Input Ports

### berlin-lor-geodata

* manifest URL: https://raw.githubusercontent.com/open-data-product/open-data-product-berlin-lor-geodata/refs/heads/main/data-product-manifest.yml

### berlin-lor-microcensus-housing-situation-source-aligned

* manifest URL: https://raw.githubusercontent.com/open-data-product/open-data-product-berlin-microcensus-housing-situation-source-aligned/refs/heads/main/data-product-manifest.yml

## Transformation Steps

* [Data extractor](https://github.com/open-lifeworlds/open-lifeworlds-python-lib/blob/main/openlifeworlds/extract/data_extractor.py) extracts data from inout ports
* [Data blender](https://github.com/open-lifeworlds/open-lifeworlds-python-lib/blob/main/openlifeworlds/transform/data_blender.py) blends csv data into geojson files

## Output Ports

### berlin-microcensus-housing-situation-geojson
name: Berlin Microcensus Housing Situation Geojson
* owner: Open Lifeworlds
* url: https://github.com/open-lifeworlds/open-lifeworlds-data-product-berlin-microcensus-housing-situation/tree/main/data/03-gold/berlin-microcensus-housing-situation-geojson
* updated: 2025-11-07

**Files**

* [berlin-microcensus-housing-situation-2014-00-districts.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-microcensus-housing-situation/refs/heads/main/data/03-gold/berlin-microcensus-housing-situation-geojson/berlin-microcensus-housing-situation-2014-00-districts.geojson)
* [berlin-microcensus-housing-situation-2018-00-districts.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-microcensus-housing-situation/refs/heads/main/data/03-gold/berlin-microcensus-housing-situation-geojson/berlin-microcensus-housing-situation-2018-00-districts.geojson)
* [berlin-microcensus-housing-situation-2022-00-districts.geojson](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-microcensus-housing-situation/refs/heads/main/data/03-gold/berlin-microcensus-housing-situation-geojson/berlin-microcensus-housing-situation-2022-00-districts.geojson)


### berlin-microcensus-housing-situation-statistics
name: Berlin Microcensus Housing Situation Statistics
* owner: Open Lifeworlds
* url: https://github.com/open-lifeworlds/open-lifeworlds-data-product-berlin-microcensus-housing-situation/tree/main/data/03-gold/berlin-microcensus-housing-situation-statistics
* updated: 2025-11-07

**Files**

* [berlin-microcensus-housing-situation-statistics.json](https://media.githubusercontent.com/media/open-lifeworlds/open-lifeworlds-data-product-berlin-microcensus-housing-situation/refs/heads/main/data/03-gold/berlin-microcensus-housing-situation-statistics/berlin-microcensus-housing-situation-statistics.json)


## Observability

### Quality metrics

 * name: geojson_property_completeness
 * description: The percentage of geojson features that have all necessary properties

| Name | Value |
| --- | --- |
| berlin-microcensus-housing-situation-2014-00-districts.geojson | 97 |
| berlin-microcensus-housing-situation-2018-00-districts.geojson | 60 |
| berlin-microcensus-housing-situation-2022-00-districts.geojson | 27 |


## Classification

**The nature of the exposed data (source-aligned, aggregate, consumer-aligned)**

consumer-aligned


---
This data product canvas uses the template of [datamesh-architecture.com](https://www.datamesh-architecture.com/data-product-canvas).