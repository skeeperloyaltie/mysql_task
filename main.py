import pandas as pd
import sqlite3

def clean_data(df):
    # Drop columns with all NaN values
    df = df.dropna(axis=1, how='all')

    # Drop rows with any NaN values
    df = df.dropna()

    # Drop columns with blank values
    df = df.replace('', pd.NA).dropna(axis=1, how='all')

    return df

def create_tables_from_excel(filename):
    # Read the Excel file
    excel_data = pd.read_excel(filename, sheet_name=None)

    # Initialize SQLite connection and cursor
    conn = sqlite3.connect('tables.db')
    cursor = conn.cursor()

    # Iterate over each sheet in the Excel file
    for sheet_name, sheet_data in excel_data.items():
        # Clean the data for each sheet
        cleaned_data = clean_data(pd.DataFrame(sheet_data))

        # Create a table for each sheet based on the sheet name
        table_name = sheet_name.replace(" ", "_").lower()

        # Exclude cleaned column names from table creation
        cleaned_columns = cleaned_data.columns
        print(cleaned_columns)
        columns = ", ".join(cleaned_columns)
        create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns})"
        cursor.execute(create_table_query)

        # Insert data into the table
        for row in cleaned_data.itertuples(index=False):
            # Exclude cleaned column names from values
            values = ", ".join([f"'{value}'" if isinstance(value, str) else str(value) for value in row if value in cleaned_columns])
            if values:
                insert_query = f"INSERT INTO `{table_name}` VALUES ({values})"
                cursor.execute(insert_query)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

import sqlite3


def print_tables():
    # Open a connection to the SQLite database file
    conn = sqlite3.connect('tables.db')
    cursor = conn.cursor()

    # Get the table names from the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = cursor.fetchall()

    # Print the table names
    for table in table_names:
        print(table[0])

    # Prompt the user for a query until 'q' is entered
    while True:
        user_input = input("Enter a query (enter 'q' to quit): ")
        if user_input == 'q':
            break

        # Execute the user's query
        cursor.execute(user_input)

        # Fetch and print each row
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    # Close the connection
    conn.close()

# Example usage
print_tables()

    
print_tables()
