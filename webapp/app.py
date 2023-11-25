from flask import Flask, render_template, request
import pandas as pd
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

from flask import Flask, render_template, request
import pandas as pd
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection details
host = 'localhost'
user = 'fr34k'
password = '1391'
database = 'task_x'

# Read the Excel file and create datasets
filename = 'data.xlsx'
xls = pd.ExcelFile(filename)
sheet_names = xls.sheet_names

datasets = {}

for sheet_name in sheet_names:
    dataset = pd.read_excel(filename, sheet_name=sheet_name)
    dataset = dataset.dropna(axis=1, how='all')
    dataset = dataset.replace(to_replace=float('nan'), value=None)
    datasets[sheet_name] = dataset

# Access specific datasets
sheet1_data = datasets['hpsa_primary_care']
sheet2_data = datasets['hpsa_mental_health']
sheet3_data = datasets['hpsa_dental_health']
sheet4_data = datasets['hpsa_mua']

# Function to create tables and initialize the database# Function to create tables and initialize the database
def initialize_database():
    conn = None  # Initialize conn to None

    try:
        conn = mysql.connector.connect(host=host, user=user, password=password)
        if conn.is_connected():
            cursor = conn.cursor()

            # Create the database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            cursor.execute(f"USE {database}")

            # Create tables and insert data
            datasets = [
                (sheet1_data.iloc[:, :10], 'hpsa_primary_care'),
                (sheet2_data.iloc[:, :10], 'hpsa_mental_health'),
                (sheet3_data.iloc[:, :10], 'hpsa_dental_health'),
                (sheet4_data.iloc[:, :10], 'hpsa_mua')
            ]

            for dataset, table_name in datasets:
                column_names = list(dataset.columns)
                values = dataset.values.tolist()

                # Generate column definitions with types
                column_definitions = ', '.join([f'{column} VARCHAR(255)' for column in column_names])

                # Create table with column names and types
                create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})"
                cursor.execute(create_table_query)

                placeholders = ', '.join(['%s'] * len(column_names))

                # Insert data into table
                insert_query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"
                cursor.executemany(insert_query, values)

            # Commit the changes
            conn.commit()

    except Error as e:
        print(f"Error: {e}")

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Initialize the database when the script runs
if initialize_database():
    print("Successfuly Inserted Data")


# Function to execute queries and return results
def execute_query(query):
    conn = None  # Initialize conn outside the try block

    try:
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)

            cursor.execute(query)
            result = pd.read_sql(query, conn)

            return result

    except Error as e:
        return f"Error: {e}"

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Execute query route
# Execute query route
@app.route('/execute_query', methods=['POST'])
def execute_query_route():
    user_query = request.form.get('user_query')
    result = execute_query(user_query)

    if isinstance(result, str):  # Check if the result is an error message
        return render_template('result.html', user_query=user_query, error=result)
    else:
        return render_template('result.html', user_query=user_query, result=result)


if __name__ == '__main__':
    app.run(debug=True)
