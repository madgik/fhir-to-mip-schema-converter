import json
import argparse


def validate_data_type(data_type):
    """
    Validate the data type of a feature/outcome.
    Accepted types are 'BOOLEAN', 'NOMINAL', 'NUMERIC'.
    """
    valid_data_types = {"BOOLEAN", "NOMINAL", "NUMERIC"}
    if data_type not in valid_data_types:
        raise ValueError(f"Invalid dataType: {data_type}. Expected one of {valid_data_types}.")
    return data_type


def transform_feature(feature, rejected_codes):
    """
    Transform a single feature or outcome into the expected format.
    Adjust the name, check for 'min' and 'max' equality, and ensure boolean fields are handled as nominal with True/False enumerations.
    """
    # Modify the name to replace spaces with underscores and make it lowercase
    code_name = feature["name"].replace(" ", "_").replace("-", "_").lower()  # Ensure lowercase

    # Check if 'numOfNotNull' exists and is 0
    if "statistics" in feature and feature["statistics"].get("numOfNotNull") == 0:
        rejected_codes.append(feature["name"])
        return None

    # Validate or default the dataType
    data_type = feature.get("dataType", "NOMINAL")  # Default to 'NOMINAL' if dataType is missing
    try:
        validate_data_type(data_type)  # Validate the data type
    except ValueError as e:
        print(f"Validation error for {code_name}: {e}")
        return None  # Skip feature with invalid dataType

    # Adjust for boolean fields, ensuring they are treated as nominal
    if feature["dataType"] == "BOOLEAN":
        new_item = {
            "code": code_name,
            "label": feature["description"],
            "description": feature["description"],
            "sql_type": "text",
            "isCategorical": True,
            "type": "nominal",
            "methodology": ", ".join(feature.get("generatedDescription", [])),
            "units": "",
            "enumerations": [
                { "code": "True", "label": "True" },
                { "code": "False", "label": "False" }
            ]
        }
    else:
        # Standard handling for non-boolean fields
        new_item = {
            "code": code_name,
            "label": feature["description"],
            "description": feature["description"],
            "sql_type": "text" if feature["dataType"] == "NOMINAL" else "real" if feature["dataType"] == "NUMERIC" else "text",
            "isCategorical": feature["dataType"] == "NOMINAL",
            "type": "nominal" if feature["dataType"] == "NOMINAL" else "real" if feature["dataType"] == "NUMERIC" else "nominal",
            "methodology": ", ".join(feature.get("generatedDescription", [])),
            "units": ""  # Empty as no units are provided in the original data
        }

        # Handle enumerations for categorical data
        if feature["dataType"] == "NOMINAL" and "valueset" in feature["statistics"]:
            enumerations = [{"code": value, "label": value} for value in feature["statistics"]["valueset"]]
            new_item["enumerations"] = enumerations
        else:
            new_item["enumerations"] = []

        # Handle numeric variables' min/max values and remove them if they are equal
        if feature["dataType"] == "NUMERIC" and "statistics" in feature:
            stats = feature["statistics"]
            if "min" in stats and "max" in stats and stats["min"] != stats["max"]:
                new_item["minValue"] = stats.get("min")
                new_item["maxValue"] = stats.get("max")
            elif "min" in stats and "max" in stats and stats["min"] == stats["max"]:
                # If min and max are equal, remove both
                pass

    return new_item

def create_dataset_variable(dataset_name):
    """
    Create the 'dataset' variable as an enumeration based on the dataset name.
    """
    return {
        "code": dataset_name.lower(),  # Ensure the code is lowercase
        "label": "Dataset Variable",
        "description": "The dataset from which the variables are sourced.",
        "sql_type": "text",
        "isCategorical": True,
        "enumerations": [
            {
                "code": dataset_name.lower(),  # Ensure enumeration code is lowercase
                "label": dataset_name
            }
        ],
        "type": "nominal",
        "methodology": "Automatically generated to represent the dataset name",
        "units": ""
    }

def transform_data(original_data, rejected_file_path):
    """
    Transform the entire dataset from the original format to the expected format,
    separating features and outcomes into different groups, and adding the 'dataset' variable.
    Rejected feature codes with 'numOfNotNull' == 0 are logged to a file.
    """
    # Check if the original data contains entries
    if not original_data["entries"]:
        raise ValueError("No entries found in the original data.")

    dataset = original_data["entries"][0]

    # Initialize transformed data structure
    transformed_data = {
        "code": dataset["name"],
        "version": dataset["meta"]["versionId"],
        "label": dataset["name"],
        "longitudinal": False,  # Based on the information provided, set longitudinal to False
        "variables": [],
        "groups": []
    }

    # Create the 'dataset' variable based on the dataset name and add it to variables
    dataset_variable = create_dataset_variable(dataset["name"])

    # Track rejected feature codes
    rejected_codes = []

    # Transform features into a group
    feature_group = {
        "code": "features",
        "label": "Features",
        "variables": [transform_feature(feature, rejected_codes) for feature in dataset["featureSet"]["features"]]
    }

    # Remove None values (rejected features)
    feature_group["variables"] = [var for var in feature_group["variables"] if var]

    # Transform outcomes into a separate group if it exists
    outcome_group = {
        "code": "outcomes",
        "label": "Outcomes",
        "variables": [transform_feature(outcome, rejected_codes) for outcome in
                      dataset["featureSet"].get("outcomes", [])]
    }

    # Remove None values (rejected outcomes)
    outcome_group["variables"] = [var for var in outcome_group["variables"] if var]

    # Add the 'dataset' variable and both feature and outcome groups
    transformed_data["variables"] = [dataset_variable]  # Always include the dataset variable first
    transformed_data["groups"] = [feature_group, outcome_group]

    # Write rejected codes to the text file
    with open(rejected_file_path, 'w') as rejected_file:
        for code in rejected_codes:
            rejected_file.write(f"{code}\n")

    return transformed_data


def read_from_json(filename):
    """
    Read data from a JSON file.
    """
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data


def export_to_json(transformed_data, filename="transformed_data.json"):
    """
    Export transformed data to a JSON file.
    """
    with open(filename, 'w') as json_file:
        json.dump(transformed_data, json_file, indent=4)
    print(f"Data has been exported to {filename}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The input JSON file to transform")
    parser.add_argument("output_file", help="The output JSON file to save the transformed data")
    parser.add_argument("rejected_file", help="The file to save rejected feature codes")

    args = parser.parse_args()

    # Read the JSON input file
    with open(args.input_file, 'r') as f:
        original_data = json.load(f)

    # Transform the data
    transformed_data = transform_data(original_data, args.rejected_file)

    # Export the transformed data to the output file
    export_to_json(transformed_data, args.output_file)

if __name__ == "__main__":
    main()

