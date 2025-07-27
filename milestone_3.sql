-- Milestone 3: Create the database schema
-- Fill in VARCHAR(XX) with the correct max lengths from your data

-- Task 1: Cast columns of orders_table
ALTER TABLE orders_table
    ALTER COLUMN date_uuid TYPE UUID USING date_uuid::uuid,
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::uuid,
    ALTER COLUMN card_number TYPE VARCHAR(XX),
    ALTER COLUMN store_code TYPE VARCHAR(XX),
    ALTER COLUMN product_code TYPE VARCHAR(XX),
    ALTER COLUMN product_quantity TYPE SMALLINT;

-- Task 2: Cast columns of dim_users
ALTER TABLE dim_users
    ALTER COLUMN first_name TYPE VARCHAR(255),
    ALTER COLUMN last_name TYPE VARCHAR(255),
    ALTER COLUMN date_of_birth TYPE DATE USING date_of_birth::date,
    ALTER COLUMN country_code TYPE VARCHAR(XX),
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::uuid,
    ALTER COLUMN join_date TYPE DATE USING join_date::date;

-- Task 3: Update dim_store_details table
-- Merge latitude columns if needed (example, adjust as necessary)
-- UPDATE dim_store_details SET latitude = COALESCE(latitude, latitude_2);
-- ALTER TABLE dim_store_details DROP COLUMN latitude_2;
ALTER TABLE dim_store_details
    ALTER COLUMN longitude TYPE NUMERIC USING longitude::numeric,
    ALTER COLUMN locality TYPE VARCHAR(255),
    ALTER COLUMN store_code TYPE VARCHAR(XX),
    ALTER COLUMN staff_numbers TYPE SMALLINT USING staff_numbers::smallint,
    ALTER COLUMN opening_date TYPE DATE USING opening_date::date,
    ALTER COLUMN store_type TYPE VARCHAR(255),
    ALTER COLUMN latitude TYPE NUMERIC USING latitude::numeric,
    ALTER COLUMN country_code TYPE VARCHAR(XX),
    ALTER COLUMN continent TYPE VARCHAR(255);
-- Set N/A to NULL in location
UPDATE dim_store_details SET location = NULL WHERE location = 'N/A';

-- Task 4: Clean dim_products table
UPDATE dim_products SET product_price = REPLACE(product_price, '£', '');
ALTER TABLE dim_products ADD COLUMN weight_class VARCHAR(XX);
UPDATE dim_products
SET weight_class = CASE
    WHEN weight::numeric < 2 THEN 'Light'
    WHEN weight::numeric >= 2 AND weight::numeric < 40 THEN 'Mid_Sized'
    WHEN weight::numeric >= 40 AND weight::numeric < 140 THEN 'Heavy'
    WHEN weight::numeric >= 140 THEN 'Truck_Required'
END;

-- Task 5: Update dim_products data types
ALTER TABLE dim_products RENAME COLUMN removed TO still_available;
ALTER TABLE dim_products
    ALTER COLUMN product_price TYPE NUMERIC USING product_price::numeric,
    ALTER COLUMN weight TYPE NUMERIC USING weight::numeric,
    ALTER COLUMN EAN TYPE VARCHAR(XX),
    ALTER COLUMN product_code TYPE VARCHAR(XX),
    ALTER COLUMN date_added TYPE DATE USING date_added::date,
    ALTER COLUMN uuid TYPE UUID USING uuid::uuid,
    ALTER COLUMN still_available TYPE BOOL USING (still_available = 'True'),
    ALTER COLUMN weight_class TYPE VARCHAR(XX);

-- Task 6: Update dim_date_times table
ALTER TABLE dim_date_times
    ALTER COLUMN month TYPE VARCHAR(XX),
    ALTER COLUMN year TYPE VARCHAR(XX),
    ALTER COLUMN day TYPE VARCHAR(XX),
    ALTER COLUMN time_period TYPE VARCHAR(XX),
    ALTER COLUMN date_uuid TYPE UUID USING date_uuid::uuid;

-- Task 7: Update dim_card_details table
ALTER TABLE dim_card_details
    ALTER COLUMN card_number TYPE VARCHAR(XX),
    ALTER COLUMN expiry_date TYPE VARCHAR(XX),
    ALTER COLUMN date_payment_confirmed TYPE DATE USING date_payment_confirmed::date;

-- Task 8: Add primary keys to dim tables
ALTER TABLE dim_users ADD PRIMARY KEY (user_uuid);
ALTER TABLE dim_store_details ADD PRIMARY KEY (store_code);
ALTER TABLE dim_products ADD PRIMARY KEY (product_code);
ALTER TABLE dim_date_times ADD PRIMARY KEY (date_uuid);
ALTER TABLE dim_card_details ADD PRIMARY KEY (card_number);

-- Task 9: Add foreign keys to orders_table
ALTER TABLE orders_table
    ADD CONSTRAINT fk_user FOREIGN KEY (user_uuid) REFERENCES dim_users(user_uuid),
    ADD CONSTRAINT fk_store FOREIGN KEY (store_code) REFERENCES dim_store_details(store_code),
    ADD CONSTRAINT fk_product FOREIGN KEY (product_code) REFERENCES dim_products(product_code),
    ADD CONSTRAINT fk_date FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid),
    ADD CONSTRAINT fk_card FOREIGN KEY (card_number) REFERENCES dim_card_details(card_number); 