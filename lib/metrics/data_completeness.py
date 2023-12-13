import json
import os
import unittest

file_path = os.path.realpath(__file__)
script_path = os.path.dirname(file_path)

data_path = os.path.join(script_path, "..", "..", "data")

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


class FilesTestCase(unittest.TestCase):
    pass


for year in [2014, 2018]:
    for half_year in ["00"]:
        for lor_area_type in ["districts"]:
            file = os.path.join(data_path, f"{key_figure_group}-{year}-{half_year}",
                                f"{key_figure_group}-{year}-{half_year}-{lor_area_type}.geojson")
            setattr(
                FilesTestCase,
                f"test_{key_figure_group}_{year}_{half_year}_{lor_area_type}".replace('-', '_'),
                lambda self, file=file: self.assertTrue(os.path.exists(file))
            )


class PropertiesTestCase(unittest.TestCase):
    pass


for year in [2014, 2018]:
    for half_year in ["00"]:
        for lor_area_type in ["districts"]:
            file = os.path.join(data_path, f"{key_figure_group}-{year}-{half_year}",
                                f"{key_figure_group}-{year}-{half_year}-{lor_area_type}.geojson")
            if os.path.exists(file):
                with open(file=file, mode="r", encoding="utf-8") as geojson_file:
                    geojson = json.load(geojson_file, strict=False)

                for feature in geojson["features"]:
                    feature_id = feature["properties"]["id"]
                    setattr(
                        PropertiesTestCase,
                        f"test_{key_figure_group}_{year}_{half_year}_{lor_area_type}_{feature_id}".replace('-', '_'),
                        lambda self, feature=feature: self.assertTrue(
                            all(property_name in feature["properties"] for property_name in statistic_properties)
                        )
                    )

if __name__ == '__main__':
    unittest.main()
