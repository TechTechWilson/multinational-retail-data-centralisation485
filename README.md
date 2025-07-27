# Multinational Retail Data Centralisation

## Project Description

This project aims to centralise a multinational retail company's sales data into a single, accessible PostgreSQL database. The workflow includes extracting and cleaning data from various sources (databases, APIs, S3 buckets), transforming it to ensure consistency and quality, and loading it into a star-based schema. The final database enables efficient querying and business intelligence, supporting data-driven decision-making across the company.

**Key objectives:**
1. Extract and clean sales, product, store, user, card, and date data from multiple sources.
2. Store raw and cleaned data in separate PostgreSQL databases for traceability.
3. Design and implement a star-based schema with correct data types, primary keys, and foreign keys.
4. Enable advanced SQL queries for business insights and reporting.

---

## Table of Contents
- [Project Description](#project-description)
- [Installation Instructions](#installation-instructions)

- [Usage Instructions](#usage-instructions)
- [File Structure](#file-structure)
- [License](#license)

---

## Installation Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/WasheeWashee/multinational-retail-data-centralisation211.git
   cd multinational-retail-data-centralisation211
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or, if using conda:
   ```bash
   conda env create -f environment.yml
   conda activate mrdc
   ```
3. Set up your PostgreSQL databases (`sales_data_raw` and `sales_data_cleaned`) using the provided `.tar` or `.sql` files.
4. Create your own YAML credentials files (`db_creds_raw.yaml`, `db_creds_cleaned.yaml`) in the project root, with the following format:
   ```yaml
   RDS_HOST: your_host
   RDS_PORT: your_port
   RDS_DATABASE: your_database
   RDS_USER: your_username
   RDS_PASSWORD: your_password
   ```

---

## Usage Instructions

1. **Run the ETL pipeline:**
   ```bash
   python main.py
   ```
   This will extract, clean, and upload data to the cleaned database.

2. **Schema migration:**
   - After running the ETL, update your database schema by running the SQL in `milestone_3.sql` against your `sales_data_cleaned` database.

3. **Querying the data:**
   - Use the queries in `milestone_4.sql` to generate business insights and reports.

**Note:** Ensure your AWS credentials and API keys are set up as required for S3 and API extraction.

---

## File Structure

- `main.py` — Orchestrates the ETL pipeline.
- `database_utils.py` — Contains the `DatabaseConnector` class for DB operations.
- `data_extraction.py` — Contains the `DataExtractor` class for extracting data from various sources.
- `data_cleaning.py` — Contains the `DataCleaning` class for cleaning and transforming data.
- `milestone_3.sql` — SQL DDL for creating and updating the star-based schema.
- `milestone_4.sql` — SQL queries for business intelligence and reporting.
- `requirements.txt` — Python dependencies.
- `environment.yml` — Conda environment specification (optional).
- `db_creds_raw.yaml`, `db_creds_cleaned.yaml` — Database credentials (not tracked in git).
- `LICENCE.txt` — License information.
- `README.md` — Project documentation (this file).

---

## License

This project is licensed under the MIT License. See the `LICENCE.txt` file for details.

---

## Acknowledgements

- Inspired by the [WasheeWashee/multinational-retail-data-centralisation211](https://github.com/WasheeWashee/multinational-retail-data-centralisation211) project.
- Data and requirements provided as part of a data engineering specialisation program.

