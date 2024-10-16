import unittest

from converter.fhir2mip import transform_data, export_to_json


class TestFHIRToMIPTransform(unittest.TestCase):

    def setUp(self):
        # Set up some mock data for testing
        self.valid_input = {
            "entries": [
                {
                    "name": "SampleDataset",
                    "meta": {"versionId": "1.0"},
                    "featureSet": {
                        "features": [
                            {"name": "Age", "description": "Patient's age", "dataType": "NUMERIC", "statistics": {"min": 0, "max": 100, "numOfNotNull": 100}},
                            {"name": "IsSmoker", "description": "Patient's smoking status", "dataType": "BOOLEAN", "statistics": {"numOfNotNull": 0}},
                            {"name": "Gender", "description": "Patient's gender", "dataType": "NOMINAL", "statistics": {"valueset": ["Male", "Female"], "numOfNotNull": 100}}
                        ],
                        "outcomes": [
                            {"name": "HeartDisease", "description": "Whether patient has heart disease", "dataType": "BOOLEAN", "statistics": {"numOfNotNull": 50}}
                        ]
                    }
                }
            ]
        }
        self.invalid_input = {"entries": []}  # Empty entries for error handling tests
        self.rejected_file = "rejected_codes.txt"

    def test_valid_transformation(self):
        result = transform_data(self.valid_input, self.rejected_file)
        self.assertIsNotNone(result, "The transformation should return a result")
        self.assertEqual(result["code"], "SampleDataset", "Dataset name should match")
        self.assertEqual(len(result["groups"][0]["variables"]), 2, "Should have 3 features in the feature group")
        self.assertEqual(len(result["groups"][1]["variables"]), 1, "Should have 1 outcome in the outcome group")

    def test_rejection_logic(self):
        transform_data(self.valid_input, self.rejected_file)
        with open(self.rejected_file, 'r') as f:
            rejected_codes = f.read().splitlines()  # Use splitlines() to avoid newline issues
        self.assertIn("IsSmoker", rejected_codes, "The 'IsSmoker' feature should be rejected")

    def test_export_to_json(self):
        result = transform_data(self.valid_input, self.rejected_file)
        export_to_json(result, "output.json")
        with open("output.json", 'r') as f:
            output_data = f.read()
        self.assertIn('"code": "sampledataset"', output_data, "The exported JSON should contain the correct dataset code")

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            transform_data(self.invalid_input, self.rejected_file)

    def test_missing_num_of_not_null(self):
        """
        Test that the function handles missing 'numOfNotNull' without crashing.
        """
        input_data = {
            "entries": [{
                "name": "SampleDataset",
                "meta": {"versionId": "1.0"},
                "featureSet": {
                    "features": [
                        {
                            "name": "IsSmoker",
                            "description": "Indicates if the patient is a smoker.",
                            "dataType": "BOOLEAN",
                            # Missing 'statistics' or 'numOfNotNull'
                        }
                    ]
                }
            }]
        }

        rejected_file_path = "rejected_codes.txt"
        transformed_data = transform_data(input_data, rejected_file_path)

        # The result should still include the variable since we aren't rejecting based on missing 'numOfNotNull'
        assert len(transformed_data["groups"][0]["variables"]) == 1
        assert transformed_data["groups"][0]["variables"][0]["code"] == "issmoker"

    def test_incorrect_data_type(self):
        """
        Test that the function gracefully handles features with unexpected data types.
        """
        input_data = {
            "entries": [{
                "name": "SampleDataset",
                "meta": {"versionId": "1.0"},
                "featureSet": {
                    "features": [
                        {
                            "name": "IsSmoker",
                            "description": "Indicates if the patient is a smoker.",
                            "dataType": "UNKNOWN",  # Incorrect data type
                            "statistics": {
                                "numOfNotNull": 10
                            }
                        }
                    ]
                }
            }]
        }

        rejected_file_path = "rejected_codes.txt"
        transformed_data = transform_data(input_data, rejected_file_path)

        # The result should skip the feature with unknown data type or handle it accordingly
        assert len(transformed_data["groups"][0]["variables"]) == 0  # No valid variables should be added

    def test_missing_description_field(self):
        """
        Test that the function handles features missing the 'description' field.
        """
        input_data = {
            "entries": [{
                "name": "SampleDataset",
                "meta": {"versionId": "1.0"},
                "featureSet": {
                    "features": [
                        {
                            "name": "IsSmoker",
                            "dataType": "BOOLEAN",
                            "statistics": {
                                "numOfNotNull": 10
                            }
                            # Missing 'description'
                        }
                    ]
                }
            }]
        }

        rejected_file_path = "rejected_codes.txt"
        with self.assertRaises(KeyError):
            transformed_data = transform_data(input_data, rejected_file_path)


    def test_malformed_json_structure(self):
        """
        Test that the function handles unexpected JSON structure gracefully.
        """
        input_data = {
            "entries": [
                {
                    "name": "SampleDataset",
                    "meta": {"versionId": "1.0"},
                    "featureSet": {
                        "features": "unexpected string instead of list"  # Malformed structure
                    }
                }
            ]
        }

        rejected_file_path = "rejected_codes.txt"

        # The function should handle the malformed structure without crashing
        with self.assertRaises(TypeError):
            transform_data(input_data, rejected_file_path)


if __name__ == "__main__":
    unittest.main()
