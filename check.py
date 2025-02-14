import streamlit as st
import pandas as pd

# Define required columns and their expected data types for each option
REQUIRED_COLUMNS_OPTIONS = {
    "Option_A": {
        "dealername": "str",
        "dealercode": "str",
        "component": "str",
        "partnumber": "str",
        "repair_date": "date",
        "quantity": "number",
        "expected_date": "date"
    },
    "Option_B": {
        "Name": "str",
        "Type": "str",
        "Quantity": "number",
        "Date": "date"
    }
}

def validate_excel_data(df, option):
    """
    Validate the DataFrame based on the expected schema:
    1. Check if all required columns are present.
    2. Validate that each column's data matches the expected type.
    
    Returns a report dictionary.
    """
    report = {"columns": None, "data": {}}  # Initialize the report dictionary
    required_columns = REQUIRED_COLUMNS_OPTIONS[option]  # Get the required columns for the selected option
    df_columns = df.columns.tolist()  # Get the columns of the DataFrame
    # Check for missing columns (order is not important)
    missing = [col for col in required_columns if col not in df_columns]
    if missing:
        report["columns"] = f"Missing columns: {missing}"
    else:
        report["columns"] = "All required columns are present."

    
    # Validate the data types of the columns
    for col, expected_type in required_columns.items():
        if col in df_columns:
            if expected_type == "date":
                try:
                    pd.to_datetime(df[col])
                    report["data"][col] = "Valid date format"
                except Exception as e:
                    report["data"][col] = f"Invalid date format: {e}"
            elif expected_type == "number":
                if pd.api.types.is_numeric_dtype(df[col]):
                    report["data"][col] = "Valid numeric format"
                else:
                    report["data"][col] = "Invalid numeric format"
            elif expected_type == "str":
                if pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
                    report["data"][col] = "Valid string format"
                else:
                    report["data"][col] = "Invalid string format"
        else:
            report["data"][col] = "Column missing"


    # Determine overall status
    if missing or any("Invalid" in status for status in report["data"].values()):
        report["status"] = "failed"
    else:
        report["status"] = "passed"
    
    return report
    

def main():
    st.title("Data Sanity Check App with Multiple Options")
    
    # Let the user select which schema to validate against
    data_option = st.selectbox("Select the type of data", options=["Option_A", "Option_B"])
    
    # File uploader for Excel files
    uploaded_file = st.file_uploader("Upload your data file (Excel)", type=["xlsx"])
    
    if uploaded_file is not None:
        try:
            # Read the Excel file into a DataFrame
            data = pd.read_excel(uploaded_file)
            
            st.subheader("Data Preview:")
            st.dataframe(data.head())
            
            # Validate the Excel data using our combined approach
            validation_report = validate_excel_data(data, data_option)
            
            st.subheader("Column Check:")
            st.write(validation_report["columns"])
            
            st.subheader("Data Type Checks:")
            for col, result in validation_report["data"].items():
                st.write(f"**{col}**: {result}")
            
            st.subheader("Overall Status:")
            if validation_report["status"] == "passed":
                st.success("Data validation passed!")
            else:
                st.error("Data validation failed!")
                
        except Exception as e:
            st.error(f"Error reading Excel file: {e}")
        
if __name__ == "__main__":
    main()
