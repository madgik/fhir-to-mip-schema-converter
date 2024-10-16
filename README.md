# FHIR to MIP Schema Conversion

This repository provides a tool to convert FHIR data into MIP schema data models, transforming features and outcomes, adjusting field names, and ensuring proper handling of categorical and numerical variables.

## Features

- Converts FHIR JSON data to MIP schema format.
- Transforms boolean fields and handles numeric min/max values.
- Logs rejected features and outcomes based on validation.
- Dynamically set input/output file paths using `argparse`.

## Usage

1. Install dependencies using [Poetry](https://python-poetry.org/):
    ```bash
    poetry install
    ```

2. Run the conversion script:
    ```bash
    poetry run python converter/converter.py --input_file <input_path> --output_file <output_path> --rejected_file <rejected_file_path>
    ```

    Example:
    ```bash
    poetry run python converter/converter.py --input_file original_data.json --output_file transformed_data.json --rejected_file rejected_codes.txt
    ```

## Testing

Run the tests using `pytest`:
```bash
poetry run pytest
```

## Files

- **converter.py**: Main script to handle the transformation from FHIR to MIP schema.
- **tests/**: Contains unit tests for validation of the transformation logic.