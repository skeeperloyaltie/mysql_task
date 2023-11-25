import pandas as pd
import mysql.connector
import random

# Step 1: Read the Excel File
df = pd.read_excel('data.xlsx')

# Step 2: Connect to MySQL Database
db_config = {
    'host': 'localhost',
    'user': 'fr34k',
    'password': '1391',
    'database': 'task_x'
}

conn = mysql.connector.connect(**db_config)

# Clean the sheet name to be a valid MySQL table name
table_name = 'dat_a'
create_table_query = f"CREATE TABLE {table_name} ("

# Function to clean column names
def clean_column_name(column):
    # Remove special characters and spaces
    return ''.join(e for e in column if e.isalnum())

for column in df.columns:
    cleaned_column_name = clean_column_name(column)
    
    # Determine data type based on column content
    data_type = 'TEXT' if df[column].apply(lambda x: isinstance(x, str) and len(x) > 255).any() else 'VARCHAR(255)'
    
    create_table_query += f"`{cleaned_column_name}` {data_type}, "

    # Handle nulls by setting them to a default value (e.g., 'N/A')
    df[column].fillna('N/A', inplace=True)

# Remove the trailing comma and add the closing parenthesis
create_table_query = create_table_query[:-2] + ");"

# Select the first 10 columns randomly
# Filter out columns with names starting with 'Unnamed'
valid_columns = [col for col in df.columns if not col.startswith('Unnamed')]
selected_columns = random.sample(valid_columns, min(10, len(valid_columns)))

for column in selected_columns:
    cleaned_column_name = column.replace(' ', '_')
    
    # Determine data type based on column content
    data_type = 'TEXT' if df[column].apply(lambda x: isinstance(x, str) and len(x) > 255).any() else 'VARCHAR(255)'
    
    create_table_query += f"`{cleaned_column_name}` {data_type}, "
    selected_columns.append(cleaned_column_name)

    # Handle nulls by setting them to a default value (e.g., 'N/A')
    df[column].fillna('N/A', inplace=True)

# Remove the trailing comma and add the closing parenthesis
create_table_query = create_table_query[:-2] + ");"

# Execute the query
with conn.cursor() as cursor:
    cursor.execute(create_table_query)

# Insert Data into the Table
def insert_data_into_table(dataframe, connection, table_name, selected_columns):
    # Select only the first 10 columns randomly
    dataframe = dataframe[selected_columns]

    with connection.cursor() as cursor:
        for index, row in dataframe.iterrows():
            # Prepare the INSERT query dynamically
            insert_query = f"INSERT INTO {table_name} ({', '.join(dataframe.columns)}) VALUES ({', '.join(['%s']*len(dataframe.columns))})"
            
            # Insert data into the table
            cursor.execute(insert_query, tuple(row))

    # Commit the changes
    connection.commit()

# Insert Data
insert_data_into_table(df, conn, table_name, selected_columns)

# Clean Up
conn.close()
print('Data imported successfully.')
