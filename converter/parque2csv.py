import pandas as pd


def parquet_to_csv(parquet_file, csv_file, columns_to_remove=None):
    # Read the Parquet file into a DataFrame
    df = pd.read_parquet(parquet_file)
    encounters_columns = df.filter(like='cause_of_death')

    total = 0
    # Loop through all columns in the DataFrame
    for col in df.columns:
        if df[col].dtype == 'object' or df[
            col].dtype == 'bool':  # Check if the column contains string or boolean values
            # Convert column to string type to avoid errors, then check for 'True'
            true_count = df[col].astype(str).str.contains('True', na=False).sum()
            total += true_count
            if true_count > 0:
                print(f"Column '{col}' has {true_count} rows with the string 'True'.")

    print(f"Total number of encounters: {total}")
    df["dataset"] = "study1"

    # Remove specified columns if any are provided
    if columns_to_remove:
        df = df.drop(columns=columns_to_remove)
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')

    # Write the DataFrame to a CSV file
    # df.to_csv(csv_file, index=False)
    print(f"Conversion complete: {parquet_file} -> {csv_file}")


# Example of how to call the function
if __name__ == "__main__":
    parquet_file = "../input_file.parquet"  # Replace with your input Parquet file
    csv_file = "/home/kfilippopolitis/Desktop/mip-deployment/data/fhir/study1.csv"  # Replace with your desired output CSV file
    columns_to_remove = ["Patient","Encounter","referenceTimePoint","eligibilityEventTime","eligibilityExitTime","nextReferenceTimePoint","previousReferenceTimePoint", 'lab_results_hba1c_value_stddev', 'lab_results_hba1c_value_min', 'lab_results_hba1c_value_avg', 'lab_results_hba1c_value_first', 'lab_results_hba1c_value_max', 'lab_results_hba1c_value_last'] + [
    "encounters_primaryReasonCode",
    "vital_signs_weight_value_stddev",
    "vital_signs_height_value_stddev",
    "vital_signs_systolicBp_value_last",
    "vital_signs_systolicBp_value_max",
    "vital_signs_systolicBp_value_avg",
    "vital_signs_systolicBp_value_min",
    "vital_signs_systolicBp_value_first",
    "vital_signs_systolicBp_value_stddev",
    "vital_signs_diastolicBp_value_last",
    "vital_signs_diastolicBp_value_max",
    "vital_signs_diastolicBp_value_avg",
    "vital_signs_diastolicBp_value_min",
    "vital_signs_diastolicBp_value_first",
    "vital_signs_diastolicBp_value_stddev",
    "vital_signs_heartRate_value_last",
    "vital_signs_heartRate_value_max",
    "vital_signs_heartRate_value_avg",
    "vital_signs_heartRate_value_min",
    "vital_signs_heartRate_value_first",
    "vital_signs_heartRate_value_stddev",
    "vital_signs_oxygenSaturation_value_last",
    "vital_signs_oxygenSaturation_value_max",
    "vital_signs_oxygenSaturation_value_avg",
    "vital_signs_oxygenSaturation_value_min",
    "vital_signs_oxygenSaturation_value_first",
    "vital_signs_oxygenSaturation_value_stddev",
    "lab_results_hemoglobin_value_stddev",
    "lab_results_ferritin_value_stddev",
    "lab_results_tfs_value_stddev",
    "lab_results_ntProBnp_value_avg",
    "lab_results_ntProBnp_value_last",
    "lab_results_ntProBnp_value_min",
    "lab_results_ntProBnp_value_stddev",
    "lab_results_ntProBnp_value_first",
    "lab_results_ntProBnp_value_max",
    "lab_results_bnp_value_avg",
    "lab_results_bnp_value_last",
    "lab_results_bnp_value_min",
    "lab_results_bnp_value_stddev",
    "lab_results_bnp_value_first",
    "lab_results_bnp_value_max",
    "lab_results_crpHs_value_avg",
    "lab_results_crpHs_value_last",
    "lab_results_crpHs_value_min",
    "lab_results_crpHs_value_stddev",
    "lab_results_crpHs_value_first",
    "lab_results_crpHs_value_max",
    "lab_results_crpNonHs_value_avg",
    "lab_results_crpNonHs_value_last",
    "lab_results_crpNonHs_value_min",
    "lab_results_crpNonHs_value_stddev",
    "lab_results_crpNonHs_value_first",
    "lab_results_crpNonHs_value_max",
    "lab_results_tropIHs_value_avg",
    "lab_results_tropIHs_value_last",
    "lab_results_tropIHs_value_min",
    "lab_results_tropIHs_value_stddev",
    "lab_results_tropIHs_value_first",
    "lab_results_tropIHs_value_max",
    "lab_results_tropInHs_value_avg",
    "lab_results_tropInHs_value_last",
    "lab_results_tropInHs_value_min",
    "lab_results_tropInHs_value_stddev",
    "lab_results_tropInHs_value_first",
    "lab_results_tropInHs_value_max",
    "lab_results_tropTHs_value_stddev",
    "lab_results_tropTnHs_value_stddev",
    "lab_results_triGly_value_stddev",
    "lab_results_cholTot_value_stddev",
    "lab_results_hdl_value_stddev",
    "lab_results_ldl_value_avg",
    "lab_results_ldl_value_last",
    "lab_results_ldl_value_min",
    "lab_results_ldl_value_stddev",
    "lab_results_ldl_value_first",
    "lab_results_ldl_value_max",
    "lab_results_potassium_value_stddev",
    "lab_results_sodium_value_stddev",
    "lab_results_creatBS_value_stddev",
    "lab_results_creatUS_value_stddev",
    "lab_results_albuminBS_value_stddev",
    "lab_results_albuminUS_value_stddev",
    "lab_results_eGFR_value_avg",
    "lab_results_eGFR_value_last",
    "lab_results_eGFR_value_min",
    "lab_results_eGFR_value_stddev",
    "lab_results_eGFR_value_first",
    "lab_results_eGFR_value_max",
    "lab_results_bun_value_stddev",
    "lab_results_acr_value_stddev",
    "lab_results_hba1c%_value_avg",
    "lab_results_hba1c%_value_last",
    "lab_results_hba1c%_value_min",
    "lab_results_hba1c%_value_stddev",
    "lab_results_hba1c%_value_first",
    "lab_results_hba1c%_value_max",
    "lab_results_hba1c_value_stddev",
    "electrocardiographs_ecg_qrs_duration",
    "electrocardiographs_ecg_qrs_axis",
    "electrocardiographs_ecg_qt_duration_corrected",
    "electrocardiographs_ecg_st",
    "electrocardiographs_ecg_ischemia_without_st",
    "electrocardiographs_ecg_type_of_rhythm",
    "nyha_value",
    "ckd_severity_categorizedValue"
]
    parquet_to_csv(parquet_file, csv_file, columns_to_remove)
