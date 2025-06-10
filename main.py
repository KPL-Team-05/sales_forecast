"""https://www.ionos.de/digitalguide/websites/web-entwicklung/sqlite3-python/"""
import sqlite3
import csv
from uuid import uuid4
import pandas as pd


def setup_database():
    """Sets up the database by creating the necessary schema and initial data.

    This function connects to a SQLite database located at 'database/forecast_data.db',
    executes the SQL commands found in 'database/schema.sql' to create the database schema,
    and then executes the SQL commands in 'database/setup.sql' to populate the database with
    initial data.

    Raises:
        sqlite3.Error: If there is an error while executing the SQL commands.
        FileNotFoundError: If the specified .sql files do not exist.
    """
    connection = sqlite3.connect('database/forecast_data.db')
    cursor = connection.cursor()
    with open('database/schema.sql', 'r', encoding='utf-8') as schema_raw, open('database/setup.sql', 'r', encoding='utf-8') as setup_raw:
        schema = schema_raw.read()
        cursor.executescript(schema)
        setup = setup_raw.read()
        cursor.executescript(setup)
    connection.commit()


def insert_csv_into_database():
    """Inserts data from a CSV file into a SQLite database.

    This function connects to a SQLite database and reads sales data from a specified CSV file. 
    For each row in the CSV, it extracts the timestamp and amount, and inserts them into the 
    'sales_data' table in the database, generating a unique identifier for each entry.

    Raises:
        sqlite3.Error: If there is an error connecting to the database or executing the insert statement.
        FileNotFoundError: If the specified CSV file does not exist.
    """
    connection = sqlite3.connect('database/forecast_data.db')
    cursor = connection.cursor()

    with open('data/sales_data_jan2022_to_now.csv', 'r', encoding='utf-8') as file:
        csv_file = csv.reader(file)
        next(csv_file)  # skip the header row
        for line in csv_file:
            timestamp = line[0]
            amount = line[1]
            insert_statement = 'INSERT INTO sales_data VALUES (?, ?, ?)'
            cursor.execute(insert_statement, (str(uuid4()), timestamp, amount))

    with open('data/plant.csv', 'r', encoding='utf-8') as file:
        csv_file = csv.reader(file)
        next(csv_file)  # skip the header row
        for line in csv_file:
            uuid = line[0]
            name = line[1]
            plz = line[2]
            region = line[3]
            country = line[4]
            speciality = line[5]
            insert_statement = 'INSERT INTO plant VALUES (?, ?, ?, ?, ?, ?)'
            cursor.execute(insert_statement, (uuid, name, plz,
                           region, country, speciality))

    with open('data/yearly_data.csv', 'r', encoding='utf-8') as file:
        csv_file = csv.reader(file)
        next(csv_file)  # skip the header row
        for line in csv_file:
            plant_id = line[0]
            year = line[1]
            employees = line[2]
            sales_figures_mio = line[3]
            volume_tsd_pieces = line[4]
            prices_fix_mio = line[5]
            prices_var_mio = line[6]
            product_area = line[7]
            insert_statement = 'INSERT INTO yearly_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cursor.execute(insert_statement, (str(uuid4()), plant_id, year, employees,
                           sales_figures_mio, volume_tsd_pieces, prices_fix_mio, prices_var_mio, product_area))
            
    
    with open('data/customer_information.csv', 'r', encoding='utf-8') as file:
        csv_file = csv.reader(file)
        next(csv_file)
        for line in csv_file:
            customer_id = line[0]
            address = line[1]
            city = line[2]
            plz= line[3]
            region = line[4]
            branch = line[5]
            employees = line[6]
            insert_statement = "INSERT INTO customer_information VALUES (?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(insert_statement, (customer_id, address, city, plz, region, branch, employees))

    with open('data/sales_data_multi_customers_per_day.csv', 'r', encoding='utf-8') as file:
        csv_file = csv.reader(file)
        next(csv_file)
        for line in csv_file:
            date = line[0]
            product = line[1]
            customer_id = line[2]
            units = line[3]
            insert_statement = "INSERT INTO sales_daily_data VALUES (?, ?, ?, ?, ?)"
            cursor.execute(insert_statement, (str(uuid4()), date, product, customer_id, units))

    with open('data/sales_data_with_products.csv', 'r', encoding='utf-8') as file:
        csv_file = csv.reader(file)
        next(csv_file)
        for line in csv_file:
            timestamp = line[0]
            amount = line[1]
            product_a = line[2]
            product_b = line[3]
            product_c = line[4]
            insert_statement = "INSERT INTO sales_data_product VALUES (?, ?, ?, ?, ?, ?)"
            cursor.execute(insert_statement, (str(uuid4()), timestamp, amount, product_a, product_b, product_c))

    with open('data/workschedule.csv', 'r', encoding='utf-8') as file:
        csv_file = csv.reader(file)
        next(csv_file)
        for line in csv_file:
            shift_date = line[0]
            section = line[1]
            product = line[2]
            planned_units = line[3]
            cycle_time_seconds = line[4]
            shift_type = line [5]
            shift_start = line [6]
            shift_end = line [7]
            insert_statement = "INSERT INTO workschedule VALUES (?, ?, ?, ?, ?, ?, ? ,? ,?)"
            cursor.execute(insert_statement, (str(uuid4()), shift_date, section, product, planned_units, cycle_time_seconds, shift_type, shift_start, shift_end))


    connection.commit()


def get_sales_data_from_database() -> pd.DataFrame:
    """Retrieves sales data from the database and returns it as a pandas DataFrame.

    This function connects to a SQLite database, fetches all records from the 
    'sales_data' table, and converts the results into a pandas DataFrame with 
    specified column names.

    Returns:
        pd.DataFrame: A DataFrame containing the sales data with columns 
        ['id', 'timestamp', 'amount'].

    Raises:
        sqlite3.Error: If there is an error connecting to the database or 
        executing the query.
    """
    connection = sqlite3.connect('database/forecast_data.db')
    cursor = connection.cursor()
    sales_data = cursor.execute('SELECT * FROM sales_data').fetchall()
    return pd.DataFrame(sales_data, columns=['id', 'timestamp', 'amount'])


def get_plants_from_database() -> pd.DataFrame:
    """Retrieve plant data from the database.

    This function connects to a SQLite database and retrieves all records from the 
    'plant' table. The retrieved data is then converted into a pandas DataFrame 
    with specified column names.

    Returns:
        pd.DataFrame: A DataFrame containing the plant data with columns 
        ['id', 'name', 'plz', 'region', 'country', 'speciality'].

    Raises:
        sqlite3.Error: If there is an error connecting to the database or executing 
        the SQL query.
    """
    connection = sqlite3.connect('database/forecast_data.db')
    cursor = connection.cursor()
    sales_data = cursor.execute('SELECT * FROM plant').fetchall()
    return pd.DataFrame(sales_data, columns=['id', 'name', 'plz', 'region', 'country', 'speciality'])

def get_customer_informations_from_database() -> pd.DataFrame:
    """Retrieve customer information data from the database.

    This function connects to a SQLite database and retrieves all records from the 
    'customer_information' table. The retrieved data is then converted into a pandas DataFrame 
    with specified column names.

    Returns:
        pd.DataFrame: A DataFrame containing the plant data with columns 
        ['customer_id', 'address', 'city', 'plz', 'region', 'branch', 'employees'].

    Raises:
        sqlite3.Error: If there is an error connecting to the database or executing 
        the SQL query.
    """
    connection = sqlite3.connect('database/forecast_data.db')
    cursor = connection.cursor()
    customer_information = cursor.execute('SELECT * FROM customer_information').fetchall()
    return pd.DataFrame(customer_information, columns=['customer_id', 'address', 'city', 'plz', 'region', 'branch', 'employees'])

def get_sales_daily_data_from_database() -> pd.DataFrame:
    """Retrieve sales daily data from the database.

    This function connects to a SQLite database and retrieves all records from the 
    'sales_daily_data' table. The retrieved data is then converted into a pandas DataFrame 
    with specified column names.

    Returns:
        pd.DataFrame: A DataFrame containing the plant data with columns 
        ['id', 'date', 'product', 'customer_id', 'units'])

    Raises:
        sqlite3.Error: If there is an error connecting to the database or executing 
        the SQL query.
    """
    connection = sqlite3.connect('database/forecast_data.db')
    cursor = connection.cursor()
    sales_daily_data = cursor.execute('SELECT * FROM sales_daily_data').fetchall()
    return pd.DataFrame(sales_daily_data, columns=['id', 'date', 'product', 'customer_id', 'units'])

def get_sales_data_product_from_database() -> pd.DataFrame:
    """Retrieve plant data from the database.

    This function connects to a SQLite database and retrieves all records from the 
    'sales_data_product' table. The retrieved data is then converted into a pandas DataFrame 
    with specified column names.

    Returns:
        pd.DataFrame: A DataFrame containing the plant data with columns 
        ['id', 'timestamp', 'amount', 'product_a', 'product_b', 'product_c'])

    Raises:
        sqlite3.Error: If there is an error connecting to the database or executing 
        the SQL query.
    """
    connection = sqlite3.connect('database/forecast_data.db')
    cursor = connection.cursor()
    sales_data_product = cursor.execute('SELECT * FROM sales_data_product').fetchall()
    return pd.DataFrame(sales_data_product, columns=['id', 'timestamp', 'amount', 'product_a', 'product_b', 'product_c'])


def get_workschedule_from_database() -> pd.DataFrame:
    """Retrieve yearly data from the database.

    This function connects to a SQLite database and retrieves all records from the 
    `workschedule` table. The data is then converted into a pandas DataFrame with 
    specified column names.

    Returns:
        pd.DataFrame: A DataFrame containing the yarly data with columns 
        ['id', 'shift_date', 'section', 'product', 'planned_units', 'cycle_time_seconds', 'shift_type','shift_start', 'shift_end'])

    Raises:
        sqlite3.Error: If there is an error connecting to the database or executing 
        the SQL query.
    """
    connection = sqlite3.connect('database/forecast_data.db')
    cursor = connection.cursor()
    workschedule = cursor.execute('SELECT * FROM workschedule').fetchall()
    return pd.DataFrame(workschedule, columns=['id', 'shift_date', 'section', 'product', 'planned_units', 'cycle_time_seconds', 'shift_type','shift_start', 'shift_end'])

def get_yearly_data_from_database() -> pd.DataFrame:
    """Retrieve yearly data from the database.

    This function connects to a SQLite database and retrieves all records from the 
    `yearly_data` table. The data is then converted into a pandas DataFrame with 
    specified column names.

    Returns:
        pd.DataFrame: A DataFrame containing the yarly data with columns 
        ['id', 'plant_id', 'year', 'employees', 'sales_figures_mio', 'volume_tsd_pieces', 'prices_fix_mio', 'prices_var_mio', 'product_area'].

    Raises:
        sqlite3.Error: If there is an error connecting to the database or executing 
        the SQL query.
    """
    connection = sqlite3.connect('database/forecast_data.db')
    cursor = connection.cursor()
    sales_data = cursor.execute('SELECT * FROM yearly_data').fetchall()
    return pd.DataFrame(sales_data, columns=['id', 'plant_id', 'year', 'employees', 'sales_figures_mio', 'volume_tsd_pieces', 'prices_fix_mio', 'prices_var_mio', 'product_area'])


def main():
    """Main function that orchestrates the workflow of the application.

    This function performs the following tasks:
    1. Sets up the database.
    2. Inserts data from a CSV file into the database.
    3. Retrieves sales data from the database.
    4. Retrieves plant data from the database.
    5. Retrieves yearly data from the database.

    It does not take any parameters and does not return any values.
    """
    setup_database()
    insert_csv_into_database()

    sales_data = get_sales_data_from_database()
    print(sales_data)

    plants = get_plants_from_database()
    print(plants)

    yearly_data = get_yearly_data_from_database()
    print(yearly_data)

    customer_informations = get_customer_informations_from_database()
    print(customer_informations)

    sales_daily_data = get_sales_daily_data_from_database()
    print(sales_daily_data)

    sales_data_product = get_sales_data_product_from_database()
    print(sales_data_product)

    workschedule = get_workschedule_from_database()
    print(workschedule)




main()
