import json
import os
import re
from functools import reduce

import pandas as pd

from lib.tracking_decorator import TrackingDecorator

key_figure_group = "berlin-lor-microcensus-housing-situation"

statistic_properties = [
    "apartments",

    "uninhabited_apartments",
    "inhabited_apartments",
    "inhabited_apartments_living_area",
    "inhabited_apartments_living_area_per_apartment",
    "inhabited_apartments_living_area_per_person",
    "inhabited_apartments_persons_per_apartment",

    "total_inhabited_by_owner",
    "total_inhabited_by_owner_percentage",
    "total_rented_out",
    "total_rented_out_percentage",
    "before_1948_inhabited_by_owner",
    "before_1948_inhabited_by_owner_percentage",
    "before_1948_rented_out",
    "before_1948_rented_out_percentage",
    "1949_and_later_inhabited_by_owner",
    "1949_and_later_inhabited_by_owner_percentage",
    "1949_and_later_rented_out",
    "1949_and_later_rented_out_percentage",

    "total_living_area",
    "total_living_area_per_apartment",
    "total_persons_per_apartment",
    "total_living_area_per_person",
    "owners_apartments_living_area",
    "owners_apartments_living_area_per_apartment",
    "owners_apartments_persons_per_apartment",
    "owners_apartments_living_area_per_person",
    "rental_apartments_living_area",
    "rental_apartments_living_area_per_apartment",
    "rental_apartments_persons_per_apartment",
    "rental_apartments_living_area_per_person",

    "single_family_houses",
    "single_family_houses_detached",
    "single_family_houses_semi_detached",
    "single_family_houses_terraced",
    "multi_family_houses",
    "multi_family_houses_detached",
    "multi_family_houses_terraced",

    "inhabited_by_owner",
    "rented_out_owned_by_private_person",
    "rented_out_owned_by_private_company",
    "rented_out_owned_by_public_institution",
    "rented_out_owned_by_housing_cooperative",

    "living_area_below_40sqm",
    "living_area_between_40_and_60sqm",
    "living_area_between_60_and_80sqm",
    "living_area_between_80_and_100sqm",
    "living_area_between_100_and_120sqm",
    "living_area_between_above_120sqm",

    "gross_rent_below_300_euros",
    "gross_rent_between_300_and_400_euros",
    "gross_rent_between_400_and_500_euros",
    "gross_rent_between_500_and_600_euros",
    "gross_rent_above_600_euros",
    "average_gross_rent",

    "gross_rent_per_sqm_below_6_euros",
    "gross_rent_per_sqm_between_6_and_7_euros",
    "gross_rent_per_sqm_between_7_and_8_euros",
    "gross_rent_per_sqm_between_8_and_9_euros",
    "gross_rent_per_sqm_above_9_euros",
    "average_gross_rent_per_sqm",

    "percentage_of_household_net_income_below_15%",
    "percentage_of_household_net_income_between_15_and_25%",
    "percentage_of_household_net_income_between_25_and_35%",
    "percentage_of_household_net_income_between_35_and_45%",
    "percentage_of_household_net_income_above_45%",
    "average_percentage_of_household_net_income",
]

statistics = [
    f"{key_figure_group}-2014-00",
    f"{key_figure_group}-2018-00",
]


@TrackingDecorator.track_time
def blend_data(source_path, results_path, clean=False, quiet=False):
    # Make results path
    os.makedirs(os.path.join(results_path), exist_ok=True)

    # Initialize statistics
    json_statistics = {}

    # Iterate over LOR area types
    for lor_area_type in ["districts"]:

        # Iterate over statistics
        for statistics_name in sorted(statistics):
            year = re.search(r"\b\d{4}\b", statistics_name).group()
            half_year = re.search(r"\b\d{2}(?<!\d{4})\b", statistics_name).group()

            # Load geojson
            geojson = read_geojson_file(
                os.path.join(source_path, "berlin-lor-geodata", f"berlin-lor-{lor_area_type}.geojson"))

            # Load statistics
            index = 19 if int(year) <= 2014 else 23
            csv_statistics_23 = read_csv_file(os.path.join(source_path, "berlin-microcensus-housing-situation-csv",
                                                           f"berlin-microcensus-housing-situation-{year}-{half_year}-{index}-apartments-in-residential-buildings-by-district-occupancy-and-living-area.csv")) \
                .rename(columns={"district_id": "id"})

            index = 20 if int(year) <= 2014 else 24
            csv_statistics_24_total = read_csv_file(
                os.path.join(source_path, "berlin-microcensus-housing-situation-csv",
                             f"berlin-microcensus-housing-situation-{year}-{half_year}-{index}-apartments-in-residential-buildings-by-district-year-of-construction-and-usage-type-total.csv")) \
                .drop(["apartments"], axis=1) \
                .rename(columns={
                "district_id": "id",
                "inhabited_by_owner": "total_inhabited_by_owner",
                "inhabited_by_owner_percentage": "total_inhabited_by_owner_percentage",
                "rented_out": "total_rented_out",
                "rented_out_percentage": "total_rented_out_percentage"
            })

            index = 20 if int(year) <= 2014 else 24
            csv_statistics_24_before_1948 = read_csv_file(
                os.path.join(source_path, "berlin-microcensus-housing-situation-csv",
                             f"berlin-microcensus-housing-situation-{year}-{half_year}-{index}-apartments-in-residential-buildings-by-district-year-of-construction-and-usage-type-before-1948.csv")) \
                .drop(["apartments"], axis=1) \
                .rename(columns={
                "district_id": "id",
                "inhabited_by_owner": "before_1948_inhabited_by_owner",
                "inhabited_by_owner_percentage": "before_1948_inhabited_by_owner_percentage",
                "rented_out": "before_1948_rented_out",
                "rented_out_percentage": "before_1948_rented_out_percentage"
            })

            index = 20 if int(year) <= 2014 else 24
            csv_statistics_24_1949_and_later = read_csv_file(
                os.path.join(source_path, "berlin-microcensus-housing-situation-csv",
                             f"berlin-microcensus-housing-situation-{year}-{half_year}-{index}-apartments-in-residential-buildings-by-district-year-of-construction-and-usage-type-1949-and-later.csv")) \
                .drop(["apartments"], axis=1) \
                .rename(columns={
                "district_id": "id",
                "inhabited_by_owner": "1949_and_later_inhabited_by_owner",
                "inhabited_by_owner_percentage": "1949_and_later_inhabited_by_owner_percentage",
                "rented_out": "1949_and_later_rented_out",
                "rented_out_percentage": "1949_and_later_rented_out_percentage"
            })

            index = 21 if int(year) <= 2014 else 25
            csv_statistics_25_total = read_csv_file(
                os.path.join(source_path, "berlin-microcensus-housing-situation-csv",
                             f"berlin-microcensus-housing-situation-{year}-{half_year}-{index}-apartments-in-residential-buildings-by-district-usage-type-living-area-and-occupancy-total.csv")) \
                .drop(["apartments"], axis=1) \
                .rename(columns={
                "district_id": "id",
                "living_area": "total_living_area",
                "living_area_per_apartment": "total_living_area_per_apartment",
                "persons_per_apartment": "total_persons_per_apartment",
                "living_area_per_person": "total_living_area_per_person",
            })

            index = 21 if int(year) <= 2014 else 25
            csv_statistics_25_owners_apartments = read_csv_file(
                os.path.join(source_path, "berlin-microcensus-housing-situation-csv",
                             f"berlin-microcensus-housing-situation-{year}-{half_year}-{index}-apartments-in-residential-buildings-by-district-usage-type-living-area-and-occupancy-owners-apartments.csv")) \
                .drop(["apartments"], axis=1) \
                .rename(columns={
                "district_id": "id",
                "living_area": "owners_apartments_living_area",
                "living_area_per_apartment": "owners_apartments_living_area_per_apartment",
                "persons_per_apartment": "owners_apartments_persons_per_apartment",
                "living_area_per_person": "owners_apartments_living_area_per_person",
            })

            index = 21 if int(year) <= 2014 else 25
            csv_statistics_25_rental_apartments = read_csv_file(
                os.path.join(source_path, "berlin-microcensus-housing-situation-csv",
                             f"berlin-microcensus-housing-situation-{year}-{half_year}-{index}-apartments-in-residential-buildings-by-district-usage-type-living-area-and-occupancy-rental-apartments.csv")) \
                .drop(["apartments"], axis=1) \
                .rename(columns={
                "district_id": "id",
                "living_area": "rental_apartments_living_area",
                "living_area_per_apartment": "rental_apartments_living_area_per_apartment",
                "persons_per_apartment": "rental_apartments_persons_per_apartment",
                "living_area_per_person": "rental_apartments_living_area_per_person",
            })

            if int(year) <= 2014:
                csv_statistics_26 = pd.DataFrame(columns=["id"])
            else:
                index = 26
                csv_statistics_26 = read_csv_file(
                    os.path.join(source_path, "berlin-microcensus-housing-situation-csv",
                                 f"berlin-microcensus-housing-situation-{year}-{half_year}-{index}-apartments-in-residential-buildings-by-district-and-building-type.csv")) \
                    .drop(["apartments"], axis=1) \
                    .rename(columns={"district_id": "id"})

            if int(year) <= 2014:
                csv_statistics_27 = pd.DataFrame(columns=["id"])
            else:
                index = 27
                csv_statistics_27 = read_csv_file(
                    os.path.join(source_path, "berlin-microcensus-housing-situation-csv",
                                 f"berlin-microcensus-housing-situation-{year}-{half_year}-{index}-apartments-in-residential-buildings-by-district-and-owner.csv")) \
                    .drop(["apartments"], axis=1) \
                    .rename(columns={"district_id": "id"})

            index = 22 if int(year) <= 2014 else 28
            csv_statistics_28 = read_csv_file(
                os.path.join(source_path, "berlin-microcensus-housing-situation-csv",
                             f"berlin-microcensus-housing-situation-{year}-{half_year}-{index}-apartments-in-residential-buildings-by-district-and-living-area.csv")) \
                .drop(["apartments"], axis=1) \
                .rename(columns={"district_id": "id"})

            index = 23 if int(year) <= 2014 else 29
            csv_statistics_29 = read_csv_file(
                os.path.join(source_path, "berlin-microcensus-housing-situation-csv",
                             f"berlin-microcensus-housing-situation-{year}-{half_year}-{index}-apartments-in-residential-buildings-by-district-and-gross-rent.csv")) \
                .drop(["apartments"], axis=1) \
                .rename(columns={"district_id": "id"})

            index = 24 if int(year) <= 2014 else 30
            csv_statistics_30 = read_csv_file(
                os.path.join(source_path, "berlin-microcensus-housing-situation-csv",
                             f"berlin-microcensus-housing-situation-{year}-{half_year}-{index}-apartments-in-residential-buildings-by-district-and-gross-rent-per-sqm.csv")) \
                .drop(["apartments"], axis=1) \
                .rename(columns={"district_id": "id"})

            index = 25 if int(year) <= 2014 else 31
            csv_statistics_31 = read_csv_file(
                os.path.join(source_path, "berlin-microcensus-housing-situation-csv",
                             f"berlin-microcensus-housing-situation-{year}-{half_year}-{index}-main-tenant-households-in-residential-buildings-by-district-and-rental-burden.csv")) \
                .drop(["apartments"], axis=1) \
                .rename(columns={"district_id": "id"})

            # Merge csv statistics
            csv_statistics = reduce(lambda left, right: pd.merge(left, right, on="id", how="outer"),
                                    [csv_statistics_23, csv_statistics_24_total, csv_statistics_24_before_1948,
                                     csv_statistics_24_1949_and_later, csv_statistics_25_total,
                                     csv_statistics_25_owners_apartments, csv_statistics_25_rental_apartments,
                                     csv_statistics_26, csv_statistics_27, csv_statistics_28, csv_statistics_29,
                                     csv_statistics_30, csv_statistics_31])

            # Extend geojson
            extend(
                year=year,
                half_year=half_year,
                geojson=geojson,
                statistics_name=statistics_name,
                csv_statistics=csv_statistics,
                json_statistics=json_statistics
            )

            # Write geojson file
            write_geojson_file(
                file_path=os.path.join(results_path, statistics_name,
                                       f"{key_figure_group}-{year}-{half_year}-{lor_area_type}.geojson"),
                statistic_name=f"{key_figure_group}-{year}-{half_year}-{lor_area_type}",
                geojson_content=geojson,
                clean=clean,
                quiet=quiet
            )

    # Write json statistics file
    write_json_file(
        file_path=os.path.join(results_path, f"{key_figure_group}-statistics",
                               f"{key_figure_group}-statistics.json"),
        statistic_name=f"{key_figure_group}-statistics",
        json_content=json_statistics,
        clean=clean,
        quiet=quiet
    )


def extend(year, half_year, geojson, statistics_name, csv_statistics, json_statistics):
    """
    Extends geojson and json-statistics by statistical values
    :param year:
    :param half_year:
    :param geojson:
    :param statistics_name:
    :param csv_statistics:
    :param json_statistics:
    :return:
    """

    # Check for missing files
    if csv_statistics is None:
        print(f"✗️ No data in {statistics_name}")
        return

    # Iterate over features
    for feature in sorted(geojson["features"], key=lambda feature: feature["properties"]["id"]):
        feature_id = feature["properties"]["id"]

        # Filter statistics
        statistic_filtered = csv_statistics[csv_statistics["id"].astype(str).str.startswith(feature_id)]

        # Check for missing data
        if statistic_filtered.shape[0] == 0:
            print(f"✗️ No data in {statistics_name} for id={feature_id}")
            continue

        # Blend data
        blend_data_into_feature(feature, statistic_filtered)
        blend_data_into_json(year, half_year, feature_id, feature, json_statistics)

    # Calculate averages
    calculate_averages(year, half_year, csv_statistics, json_statistics)


def blend_data_into_feature(feature, statistics):
    # Add new properties
    for property_name in statistic_properties:
        add_property(feature, statistics, property_name)

    return feature


def blend_data_into_json(year, half_year, feature_id, feature, json_statistics):
    # Build structure
    if year not in json_statistics:
        json_statistics[year] = {}
    if half_year not in json_statistics[year]:
        json_statistics[year][half_year] = {}

    # Add properties
    json_statistics[year][half_year][feature_id] = feature["properties"]


def calculate_averages(year, half_year, csv_statistics, json_statistics):
    values = {}

    values_sums = {property_name: int(sum(csv_statistics[property_name]))
                   for property_name in statistic_properties if property_name in csv_statistics}
    values_averages = {}

    values |= values_sums
    values |= values_averages

    json_statistics[year][half_year][0] = values


def add_property(feature, statistics, property_name):
    if statistics is not None and property_name in statistics:
        try:
            feature["properties"][f"{property_name}"] = int(statistics[property_name].sum())
        except ValueError:
            feature["properties"][f"{property_name}"] = 0


def add_property_with_modifiers(feature, statistics, property_name, total_area_sqkm):
    if statistics is not None and property_name in statistics:
        try:
            feature["properties"][f"{property_name}"] = int(statistics[property_name].sum())
            if total_area_sqkm is not None:
                feature["properties"][f"{property_name}_per_sqkm"] = round(
                    float(statistics[property_name].sum()) / total_area_sqkm, 2)
        except ValueError:
            feature["properties"][f"{property_name}"] = 0

            if total_area_sqkm is not None:
                feature["properties"][f"{property_name}_per_sqkm"] = 0
        except TypeError:
            feature["properties"][f"{property_name}"] = 0

            if total_area_sqkm is not None:
                feature["properties"][f"{property_name}_per_sqkm"] = 0


def read_csv_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as csv_file:
            return pd.read_csv(csv_file, dtype={"id": "str", "district_id": "str"})
    else:
        return None


def read_geojson_file(file_path):
    with open(file=file_path, mode="r", encoding="utf-8") as geojson_file:
        return json.load(geojson_file, strict=False)


def write_geojson_file(file_path, statistic_name, geojson_content, clean, quiet):
    if not os.path.exists(file_path) or clean:

        # Make results path
        path_name = os.path.dirname(file_path)
        os.makedirs(os.path.join(path_name), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as geojson_file:
            json.dump(geojson_content, geojson_file, ensure_ascii=False)

            if not quiet:
                print(f"✓ Blend data from {statistic_name} into {os.path.basename(file_path)}")
    else:
        print(f"✓ Already exists {os.path.basename(file_path)}")


def write_json_file(file_path, statistic_name, json_content, clean, quiet):
    if not os.path.exists(file_path) or clean:

        # Make results path
        path_name = os.path.dirname(file_path)
        os.makedirs(os.path.join(path_name), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(json_content, json_file, ensure_ascii=False)

            if not quiet:
                print(f"✓ Aggregate data from {statistic_name} into {os.path.basename(file_path)}")
    else:
        print(f"✓ Already exists {os.path.basename(file_path)}")
