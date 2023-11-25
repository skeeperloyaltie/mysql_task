# %% [markdown]
# ### Introduction
# 
# The application idea revolves around managing and analyzing healthcare workforce data, specifically focusing on Health Professional Shortage Areas (HPSAs) and Medically Underserved Areas (MUAs). The data source is a set of tables representing these areas, obtained from reliable healthcare databases or government health agencies.
# 
# The primary goal of the application is to provide insights into the distribution and characteristics of healthcare resources across different regions. It aims to assist healthcare planners, policymakers, and researchers in making informed decisions about resource allocation, identifying areas with shortages, and addressing healthcare disparities.
# 
# The core data includes information about various health facilities, their designations, and the status of different HPSAs and MUAs. This data is crucial for understanding the availability of healthcare services in different geographical areas. The application can be a valuable tool for optimizing workforce distribution, improving access to care, and ultimately enhancing overall health outcomes.
# 
# The database schema is designed to capture essential information about Health Professional Shortage Areas (HPSAs) and Medically Underserved Areas (MUAs). Here's a brief overview of the schema:
# 
# ### Tables:
# hpsa_primary_care:
# 
#     Source_ID (Primary Key)
#     Source_Name
#     Status_Code
#     Status_Description
#     Type_Code
#     Type_Desc
#     Address
#     City
#     State_Abbr
#     Postal_Code
# 
# hpsa_mental_health:
# 
#     Source_ID (Primary Key)
#     Source_Name
#     Status_Code
#     Status_Description
#     Type_Code
#     Type_Desc
#     State_Abbr
#     Degree_of_Shortage
#     Designation_Date
#     Designation_Last_Update_Date
# 
# hpsa_dental_health:
# 
#     Source_ID (Primary Key)
#     Source_Name
#     Status_Code
#     Status_Description
#     Type_Code
#     Type_Desc
#     Address
#     City
#     State_Abbr
#     Postal_Code
# 
# hpsa_mua:
# 
#     MUA_SOURCE_ID (Primary Key)
#     MUA_AREA_CD
#     MUA_DESIGNATION_TYP_CD
#     MUA_DESIGNATION_TYP_DESC
#     MUA_STATUS_CD
#     MUA_STATUS_DESC
#     CENSUS_TRACT
#     MUA_DESIGNATION_DT
#     MUA_DESIGNATION_DT_TXT
#     MUA_SCORE
# ### Rationale:
# - Normalization: The schema follows normalization principles to minimize data redundancy and improve data integrity.
# 
# - Primary Keys: Each table has a primary key to uniquely identify records.
# 
# Consistent Naming: Column names are consistent across tables for similar attributes, facilitating ease of understanding and query writing.
# 
# Relationships: While the schema presented here doesn't explicitly show foreign keys, they would be used to establish relationships between tables, ensuring data consistency.
# 
# This schema allows for efficient querying and analysis of healthcare workforce data, providing a foundation for the application's functionality.

# %%
import pandas as pd

import mysql.connector
from mysql.connector import Error

# Read the Excel file
filename = 'data.xlsx'
xls = pd.ExcelFile(filename)

# Get the sheet names
sheet_names = xls.sheet_names

# Create a dictionary to store the datasets
datasets = {}

# Loop through each sheet and save the data as a dataset
for sheet_name in sheet_names:
    dataset = pd.read_excel(filename, sheet_name=sheet_name)
    
    # Remove columns with NaN values
    dataset = dataset.dropna(axis=1, how='all')
    
    # Replace NaN values with None
    dataset = dataset.replace(to_replace=float('nan'), value=None)
    
    # Convert columns to appropriate types if needed
    # dataset['column_name'] = pd.to_numeric(dataset['column_name'], errors='coerce')
    
    datasets[sheet_name] = dataset

# Access a specific dataset
sheet1_data = datasets['hpsa_primary_care'] 
sheet2_data = datasets['hpsa_mental_health'] 
sheet3_data = datasets['hpsa_dental_health']
sheet4_data = datasets['hpsa_mua']


# %%
sheet1_data.head()

# %%
sheet2_data.head()


# %%
sheet3_data.columns

# %%
sheet3_data.head()

# %%
sheet4_data.columns

# %%
sheet4_data.head()

# %% [markdown]
# ### Stored Procedures:
# 1. usp_GetAverageScoreByMUAStatus
# Purpose: This stored procedure calculates and returns the average MUA score for each MUA status.
# 
# - How it works:
# ```
# CREATE PROCEDURE usp_GetAverageScoreByMUAStatus
#     AS
#     BEGIN
#         SELECT
#             MUA_STATUS_DESC,
#             AVG(CAST(MUA_SCORE AS FLOAT)) AS Average_Score
#         FROM
#             hpsa_mua
#         GROUP BY
#             MUA_STATUS_DESC;
#     END;
# ```
# - Usage in Application:
# This procedure provides a quick overview of the average MUA scores based on different MUA statuses. It aids in identifying trends and disparities in healthcare accessibility across various designations.
# 
# 2. usp_GetHPSAByStateAndType
# Purpose: This stored procedure retrieves HPSAs based on the provided state abbreviation and type code.
# 
# How it works:
# ```
# CREATE PROCEDURE usp_GetHPSAByStateAndType
#     @StateAbbreviation NVARCHAR(2),
#     @TypeCode NVARCHAR(10)
# AS
# BEGIN
#     SELECT *
#     FROM
#         hpsa_primary_care
#     WHERE
#         State_Abbr = @StateAbbreviation
#         AND Type_Code = @TypeCode;
# END;
# ```
# - Usage in Application:
# It allows the application to fetch specific HPSAs based on user-inputted criteria, helping healthcare planners to focus on areas of interest and address shortages effectively.
# 
# ### Queries
# 1. Average Score of Designated MUAs:
# Purpose: To retrieve the average MUA score for designated areas.
# ```
# SELECT
#     MUA_STATUS_DESC,
#     AVG(CAST(MUA_SCORE AS FLOAT)) AS Average_Score
# FROM
#     hpsa_mua
# WHERE
#     MUA_STATUS_DESC = 'Designated'
# GROUP BY
#     MUA_STATUS_DESC;
# ```
# 2. HPSAs in a Specific State and Type:
# Purpose: To fetch HPSAs in a particular state and of a specific type.
# ```
# SELECT *
# FROM
#     hpsa_primary_care
# WHERE
#     State_Abbr = 'CA'
#     AND Type_Code = 'IHS';
# ```
# 
# 3. Designated Mental Health HPSAs:
# Purpose: To retrieve information about designated mental health HPSAs.
# 
# ```
# SELECT *
# FROM
#     hpsa_mental_health
# WHERE
#     Status_Description = 'Designated';
# ```
# 
# 4. MUAs with the Highest Scores:
# Purpose: To find MUAs with the highest scores.
# 
# ```
# SELECT TOP 5
#     *
# FROM
#     hpsa_mua
# ORDER BY
#     MUA_SCORE DESC;
# ```
# 
# How they are used in Application:
# 
# - The average MUA score query aids in displaying a summary of MUA scores.
# - The HPSA retrieval query allows users to explore specific HPSAs based on state and type.
# - The designated mental health HPSAs query provides insights into areas specifically designated for mental health.
# - The query for MUAs with the highest scores helps identify areas with the greatest need for attention and resources.
# - These queries and procedures collectively empower the application to offer detailed insights into healthcare workforce distribution and shortages, supporting informed decision-making.

# %% [markdown]
# - Database Connection:
# 
# Attempts to connect to a MySQL database using the provided host, user, password, and database information.
# - Table Creation and Data Insertion:
# 
# Defines four datasets, each representing a table (hpsa_primary_care, hpsa_mental_health, hpsa_dental_health, and hpsa_mua).
# For each dataset, it dynamically generates a CREATE TABLE query based on the column names and their types (assumed VARCHAR(255)).
# Executes the CREATE TABLE query to create a table in the MySQL database.
# Prepares and executes an INSERT query to insert the data from the dataset into the corresponding table.
# - Commit Changes:
# 
# Commits the changes to the database. This step is crucial for the changes to take effect permanently.
# - Error Handling:
# 
# If any error occurs during the process (such as a connection error, SQL syntax error, etc.), it prints an error message.
# - Connection Closure:
# 
# Closes the cursor and the database connection, ensuring proper cleanup.
# This script is designed to initialize a MySQL database by creating tables based on provided datasets and inserting data into these tables. It's a common approach when setting up a database for the first time or when updating the schema with new data.

# %%
import pandas as pd
import mysql.connector
from mysql.connector import Error

# Database connection details
host = 'localhost'
user = 'root'
password = ''
database = 'task_x'

# Create a MySQL connection
try:
    conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
    if conn.is_connected():
        print('Connected to MySQL database')

        # Create a cursor
        cursor = conn.cursor()

        # Drop tables if they exist
        cursor.execute("DROP TABLE IF EXISTS hpsa_primary_care")
        cursor.execute("DROP TABLE IF EXISTS hpsa_mental_health")
        cursor.execute("DROP TABLE IF EXISTS hpsa_dental_health")
        cursor.execute("DROP TABLE IF EXISTS hpsa_mua")

        # Insert datasets into MySQL tables
        datasets = [(sheet1_data.iloc[:, :10], 'hpsa_primary_care'), 
                    (sheet2_data.iloc[:, :10], 'hpsa_mental_health'),
                    (sheet3_data.iloc[:, :10], 'hpsa_dental_health'), 
                    (sheet4_data.iloc[:, :10], 'hpsa_mua')]

        for dataset, table_name in datasets:
            column_names = list(dataset.columns)
            values = dataset.values.tolist()

            # Generate column definitions with types
            column_definitions = ', '.join([f'{column} VARCHAR(255)' for column in column_names])

            # Create table with column names and types
            create_table_query = f"CREATE TABLE {table_name} ({column_definitions})"
            cursor.execute(create_table_query)

            placeholders = ', '.join(['%s'] * len(column_names))

            # Insert data into table
            insert_query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.executemany(insert_query, values)

        # Commit the changes
        conn.commit()
        print('Data inserted into MySQL tables')

except Error as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    if conn.is_connected():
        cursor.close()
        conn.close()
        print('You can now select from tables')


# %% [markdown]
# This Python code establishes a connection to a MySQL database using the mysql.connector library. It prompts the user to input a SQL query, then executes the query and fetches all rows from the result. Finally, it prints each row to the console.
# 
# Here's a breakdown:
# 
# - Database Connection:
# 
# It attempts to connect to a MySQL database using the provided host, user, password, and database information.
# 
# - User Input:
# 
# The user is prompted to enter a SQL query they want to perform on the connected database.
# 
# - Query Execution:
# 
# The provided SQL query is executed using the database cursor.
# - Fetching and Printing Rows:
# 
# All rows resulting from the query execution are fetched.
# Each row is printed to the console.
# - Error Handling:
# 
# If any error occurs during the process, it prints an error message.
# - Connection Closure:
# 
# Finally, it closes the cursor and the database connection.
# This code allows users to interactively input and execute SQL queries on the connected MySQL database, providing a flexible way to explore and retrieve data.

# %%
def print_tables():
    try:
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)

            # Fetch table names
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            # Print tables with headers
            for table in tables:
                table_name = table['Tables_in_task_x']
                print(f"Table: {table_name}")

                # Fetch and print table data with headers
                cursor.execute(f"SELECT * FROM {table_name}")
                result = cursor.fetchall()

                if result:
                    df = pd.DataFrame(result)
                    print(df)

                print("\n")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Print tables with headers
print_tables()
# Create a MySQL connection
# %%
# print all columns for all tables 
sheet1_data.columns


# %%
sheet2_data.columns 


# %%
sheet3_data.columns 


# %%
sheet4_data.columns

# %% [markdown]
# ### Usage - Queries Procedures
# 

# %%
# Function to fetch and print tables with headers


# %%
import mysql.connector
from mysql.connector import Error

# Database connection details
host = 'localhost'
user = 'root'
password = ''
database = 'task_x'

# Function to create stored procedures
def create_stored_procedures():
    try:
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        if conn.is_connected():
            cursor = conn.cursor()

            # Stored Procedure 1: Get data from hpsa_primary_care
            sp1_query = """
                CREATE PROCEDURE GetPrimaryCareData()
                BEGIN
                    SELECT * FROM hpsa_primary_care;
                END
            """
            cursor.execute(sp1_query)
            print("Stored Procedure 1 created successfully.")

            # Stored Procedure 2: Get data from hpsa_dental_health
            sp2_query = """
                CREATE PROCEDURE GetDentalHealthData()
                BEGIN
                    SELECT * FROM hpsa_dental_health;
                END
            """
            cursor.execute(sp2_query)
            print("Stored Procedure 2 created successfully.")

            # Commit the changes
            conn.commit()

    except Error as e:
        print(f"Error: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Create stored procedures
create_stored_procedures()


# %%


# %%
import pandas as pd

# Function to execute queries and print results
def execute_queries():
    try:
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)

            # Query 1: Get unique cities from hpsa_primary_care
            query1 = "SELECT DISTINCT City FROM hpsa_primary_care;"
            result1 = pd.read_sql(query1, conn)
            print("Query 1:")
            print(result1)

            # Query 2: Get the count of each Type_Desc from hpsa_dental_health
            query2 = "SELECT Type_Desc, COUNT(*) as Count FROM hpsa_dental_health GROUP BY Type_Desc;"
            result2 = pd.read_sql(query2, conn)
            print("\nQuery 2:")
            print(result2)
            
            # Query 3: Get the average MUA_SCORE for each MUA_STATUS_DESC in hpsa_mua
            query3 = "SELECT MUA_STATUS_DESC, AVG(MUA_SCORE) as Average_Score FROM hpsa_mua GROUP BY MUA_STATUS_DESC;"
            result3 = pd.read_sql(query3, conn)
            print("\nQuery 3:")
            print(result3)

                        
            query4 = """
                SELECT Source_Name, Address
                FROM hpsa_primary_care
                ORDER BY Address DESC
                LIMIT 5;
            """
            result4 = pd.read_sql(query4, conn)
            print("\nQuery 4:")
            print(result4)


    except Error as e:
        print(f"Error: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Execute queries
execute_queries()


# %% [markdown]
# ### Conclusion:
# The project successfully leverages Python and MySQL to initialize and populate a database with four tables (hpsa_primary_care, hpsa_mental_health, hpsa_dental_health, and hpsa_mua). The script utilizes the pandas library to handle datasets, dynamically generates SQL queries for table creation and data insertion, and ensures proper error handling and connection closure.
# 
# The database is structured to store information related to healthcare provider shortage areas, mental health designations, dental health designations, and medically underserved areas. This organized data lays the foundation for efficient querying and analysis.
# 
# Additionally, the script includes functionality to perform user-defined SELECT queries, allowing users to retrieve specific information from the populated tables interactively.
# 
# Overall, the project combines data management, database creation, and user interaction, providing a robust foundation for further development and analysis in the realm of healthcare data.


try:
    conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
    if conn.is_connected():
        print('Connected to MySQL database')

        # Create a cursor
        cursor = conn.cursor()

        # Select all rows from a table
        select_query = input(str("Enter a query to perform: ")) #"SELECT * FROM hpsa_mua where hpsa_mua.mua_source_ID > 1000;"
        cursor.execute(select_query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Print the rows
        for row in rows:
            print(row)

except Error as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    if conn.is_connected():
        cursor.close()
        conn.close()
        print('Connection closed')

