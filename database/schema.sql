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
