CREATE TABLE IF NOT EXISTS sales_data (
    id TEXT PRIMARY KEY NOT NULL,
    timestamp DATE NOT NULL,
    amount INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS plant (
    id TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    plz INT NOT NULL,
    region TEXT NOT NULL,
    country TEXT NOT NULL,
    speciality TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS yearly_data (
    id TEXT PRIMARY KEY NOT NULL,
    plant_id TEXT NOT NULL,
    year INT NOT NULL,
    employees INT NOT NULL,
    sales_figures_mio  NUMERIC(6,2) NOT NULL,
    volume_tsd_pieces INT NOT NULL,
    prices_fix_mio NUMERIC(6,2) NOT NULL,
    prices_var_mio  NUMERIC(6,2) NOT NULL,
    product_area TEXT NOT NULL,
    FOREIGN KEY (plant_id) REFERENCES plant(id)
);

CREATE TABLE IF NOT EXISTS customer_information (
    customer_id TEXT PRIMARY KEY NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    plz INT NOT NULL,
    region TEXT NOT NULL,
    branch TEXT NOT NULL,
    employees INT NOT NULL
);

CREATE TABLE IF NOT EXISTS sales_daily_data (
    id TEXT PRIMARY KEY NOT NULL,
    date TEXT NOT NULL,
    product TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    units INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer_information(customer_id)
);

CREATE TABLE IF NOT EXISTS workschedule (
    id TEXT PRIMARY KEY NOT NULL,
    shift_date TEXT NOT NULL,
    section TEXT NOT NULL,
    product TEXT NOT NULL,
    planned_units INT NOT NULL,
    cycle_time_seconds INT NOT NULL,
    shift_type TEXT NOT NULL,
    shift_start TEXT NOT NULL,
    shit_end TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sales_data_product (
    id TEXT PRIMARY KEY NOT NULL,
    timestamp TEXT NOT NUll,
    amount INT NOT NULL,
    product_a INT NOT NULL,
    product_b INT NOT NULL,
    product_c INT NOT NULL
);
    

