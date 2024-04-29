import streamlit as st
import pandas as pd

# Define the predefined column names for each type
predefined_columns = {
    "Flowers": ["Name", "Color", "Quantity", "Date"],
    "Fruits": ["Name", "Type", "Quantity", "Date"]
}

# Function to check column names
def check_columns(file, type):
    df = pd.read_excel(file)
    expected_cols = predefined_columns[type]
    if list(df.columns) == expected_cols:
        return "Column names are correct"
    else:
        return f"Column names mismatch. Expected: {expected_cols}, Found: {list(df.columns)}"

# Function to check date formats and other sanity checks
def check_data(df):
    # Implement your checks here
    pass

def main():
    st.title("Data Sanity Check App")

    # Dropdown to select the type of data
    data_type = st.selectbox("Select the type of data", options=["Flowers", "Fruits"])

    # File uploader
    uploaded_file = st.file_uploader("Upload your data file", type="xlsx")
    if uploaded_file:
        # Check columns
        column_check = check_columns(uploaded_file, data_type)
        st.write(column_check)
        
        # Load data for further checks
        data = pd.read_excel(uploaded_file)
        
        # Additional checks
        # Implement your checks here and display results
        
if __name__ == "__main__":
    main()
