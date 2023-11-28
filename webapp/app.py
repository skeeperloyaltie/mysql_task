from flask import Flask, render_template
import pandas as pd
# %%
import pandas as pd
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Read the Excel file and store datasets
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

# Function for Function 1



# Database connection details
host = 'localhost'
user = 'fr34k'
password = '1391'
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



def function1_logic():
    # Create a dictionary with HTML representations of all sheets
    all_data_html = {
        'sheet1_data': sheet1_data.to_html(),
        'sheet2_data': sheet2_data.to_html(),
        'sheet3_data': sheet3_data.to_html(),
        'sheet4_data': sheet4_data.to_html(),
    }
    
    # For demonstration purposes, let's just return the dictionary
    return all_data_html
# Function for Function 2
# Function for Function 2
def function2_logic():
    try:
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)

            # Fetch table names
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            # Create a dictionary to store HTML representations of tables
            all_table_html = {}

            for table in tables:
                table_name = table['Tables_in_task_x']

                # Fetch and store HTML representation of each table
                cursor.execute(f"SELECT * FROM {table_name} limit 20")
                result = cursor.fetchall()

                if result:
                    df = pd.DataFrame(result)
                    all_table_html[table_name] = df.to_html()

            return all_table_html

    except Error as e:
        print(f"Error: {e}")
        return {}


# Function to execute stored procedures
def execute_stored_procedure(sp_name):
    try:
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            
            # Execute the stored procedure
            cursor.callproc(sp_name)
            
            # Fetch and return the result
            result = cursor.fetchall()
            return pd.DataFrame(result).to_html() if result else None

    except Error as e:
        print(f"Error: {e}")
        return None

    # finally:
    #     if conn.is_connected():
    #         cursor.close()
    #         conn.close()
def create_stored_procedures(cursor):
    # Stored Procedure 1: Get data from hpsa_primary_care
    sp1_query = """
        CREATE PROCEDURE if not exists GetPrimaryCareData()
        BEGIN
            SELECT * FROM hpsa_primary_care limit 20;
        END
    """
    cursor.execute(sp1_query)

    # Stored Procedure 2: Get data from hpsa_dental_health
    sp2_query = """
        CREATE PROCEDURE if not exists GetDentalHealthData()
        BEGIN
            SELECT * FROM hpsa_dental_health limit 20;
        END
    """
    cursor.execute(sp2_query)
create_stored_procedures(conn.cursor())


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

    # finally:
    #     if conn.is_connected():
    #         cursor.close()
    #         conn.close()

# Execute queries

# try:
#     conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
#     if conn.is_connected():
#         print('Connected to MySQL database')

#         # Create a cursor
#         cursor = conn.cursor()

#         # # Select all rows from a table
#         # select_query = input(str("select * from ")) #"SELECT * FROM hpsa_mua where hpsa_mua.mua_source_ID > 1000;"
#         # cursor.execute(select_query)

#         # Fetch all rows
#         rows = cursor.fetchall()

#         # Print the rows
#         for row in rows:
#             print(row)

# except Error as e:
#     print(f"Error: {e}")

# finally:
#     # Close the cursor and connection
#     if conn.is_connected():
#         cursor.close()
#         conn.close()
#         print('Connection closed')
@app.route('/functions/function3')
def function3():
    return render_template('functions/function3.html')

# Route to execute GetPrimaryCareData stored procedure
@app.route('/execute_sp1', methods=['POST'])
def execute_sp1():
    sp1_data = execute_stored_procedure('GetPrimaryCareData')
    return render_template('functions/function3.html', sp1_data=sp1_data)

# Route to execute GetDentalHealthData stored procedure
@app.route('/execute_sp2', methods=['POST'])
def execute_sp2():
    sp2_data = execute_stored_procedure('GetDentalHealthData')
    return render_template('functions/function3.html', sp2_data=sp2_data)

@app.route('/functions/function4')
def function4():
    fun4 = execute_queries()
    return render_template('functions/function4.html', func4=fun4)
# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/functions/function1')  # Adjusted route
def function1():
    # Call the function1_logic to get the data
    function1_data = function1_logic()
    return render_template('functions/function1.html', function1_data=function1_data)  # Adjusted template path

# Update the route function to use the new function2_logic
@app.route('/functions/function2')
def function2():
    # Call the function2_logic to get the data
    function2_data = function2_logic()
    return render_template('functions/function2.html', function2_data=function2_data)

if __name__ == '__main__':
    app.run(debug=True)
