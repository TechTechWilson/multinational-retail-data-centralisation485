# Milestone 3: Create the database schema

Develop the star-based schema of the database, ensuring that the columns are of the correct data types.

---

<details>
<summary><h4>Prerequisites Content: Task 1</h4></summary>

`1. What is SQL?` `2. SQL Setup` `3. SQL Tools Setup` `4. SQL Commands` `5. SQL Best Practices` `6. SELECT and Sorting` `7. The WHERE Clause` `8. CRUD Creating Tables` `9. CRUD Altering Tables` `10. SQL JOINs` `11. SQL JOIN Types` `12. SQL Common Aggregations`

</details>

<details>
<summary><h3>Task 1: Cast the columns of the `orders_table` to the correct data types.</h3></summary>

Change the data types to correspond to those seen in the table below.
<pre>
+------------------+--------------------+--------------------+
|   orders_table   | current data type  | required data type |
+------------------+--------------------+--------------------+
| date_uuid        | TEXT               | UUID               |
| user_uuid        | TEXT               | UUID               |
| card_number      | TEXT               | VARCHAR(?)         |
| store_code       | TEXT               | VARCHAR(?)         |
| product_code     | TEXT               | VARCHAR(?)         |
| product_quantity | BIGINT             | SMALLINT           |
+------------------+--------------------+--------------------+
</pre>

The `?` in `VARCHAR` should be replaced with an integer representing the maximum length of the values in that column.

</details>

<details>
<summary><h3>Task 2: Cast the columns of the `dim_users` to the correct data types.</h3></summary>

The column required to be changed in the users table are as follows:
<pre>
+----------------+--------------------+--------------------+
| dim_users      | current data type  | required data type |
+----------------+--------------------+--------------------+
| first_name     | TEXT               | VARCHAR(255)       |
| last_name      | TEXT               | VARCHAR(255)       |
| date_of_birth  | TEXT               | DATE               |
| country_code   | TEXT               | VARCHAR(?)         |
| user_uuid      | TEXT               | UUID               |
| join_date      | TEXT               | DATE               |
+----------------+--------------------+--------------------+
</pre>

</details>

<details>
<summary><h3>Task 3: Update the `dim_store_details` table.</h3></summary>

There are two latitude columns in the store details table.
Using SQL, merge one of the columns into the other so you have one `latitude` column.

Then set the data types for each column as shown below:
<pre>
+---------------------+-------------------+------------------------+
| store_details_table | current data type |   required data type   |
+---------------------+-------------------+------------------------+
| longitude           | TEXT              | NUMERIC                |
| locality            | TEXT              | VARCHAR(255)           |
| store_code          | TEXT              | VARCHAR(?)             |
| staff_numbers       | TEXT              | SMALLINT               |
| opening_date        | TEXT              | DATE                   |
| store_type          | TEXT              | VARCHAR(255) NULLABLE  |
| latitude            | TEXT              | NUMERIC                |
| country_code        | TEXT              | VARCHAR(?)             |
| continent           | TEXT              | VARCHAR(255)           |
+---------------------+-------------------+------------------------+
</pre>

There is a row that represents the business's website change the location column values from `N/A` to `NULL`.

</details>

<details>
<summary><h3>Task 4: Make changes to the `dim_products` table for the delivery team.</h3></summary>

You will need to do some work on the `products` table before casting the data types correctly.

The `product_price` column has a `£` character which you need to remove using SQL.

The team that handles the deliveries would like a new human-readable column added for the weight so they can quickly make decisions on delivery weights.

Add a new column `weight_class` which will contain human-readable values based on the weight range of the product.
<pre>
+--------------------------+-------------------+
| weight_class VARCHAR(?)  | weight range(kg)  |
+--------------------------+-------------------+
| Light                    | < 2               |
| Mid_Sized                | >= 2 - < 40       |
| Heavy                    | >= 40 - < 140     |
| Truck_Required           | => 140            |
+----------------------------+-----------------+
</pre>

</details>

<details>
<summary><h3>Task 5: Update the `dim_products` table with the required data types.</h3></summary>

After all the columns are created and cleaned, change the data types of the `products` table.

You will want to rename the `removed` column to `still_available` before changing its data type.

Make the changes to the columns to cast them to the following data types:
<pre>
+-----------------+--------------------+--------------------+
|  dim_products   | current data type  | required data type |
+-----------------+--------------------+--------------------+
| product_price   | TEXT               | NUMERIC            |
| weight          | TEXT               | NUMERIC            |
| EAN             | TEXT               | VARCHAR(?)         |
| product_code    | TEXT               | VARCHAR(?)         |
| date_added      | TEXT               | DATE               |
| uuid            | TEXT               | UUID               |
| still_available | TEXT               | BOOL               |
| weight_class    | TEXT               | VARCHAR(?)         |
+-----------------+--------------------+--------------------+
</pre>

</details>

<details>
<summary><h3>Task 6: Update the `dim_date_times` table.</h3></summary>

Now update the date table with the correct types:
<pre>
+-----------------+-------------------+--------------------+
| dim_date_times  | current data type | required data type |
+-----------------+-------------------+--------------------+
| month           | TEXT              | VARCHAR(?)         |
| year            | TEXT              | VARCHAR(?)         |
| day             | TEXT              | VARCHAR(?)         |
| time_period     | TEXT              | VARCHAR(?)         |
| date_uuid       | TEXT              | UUID               |
+-----------------+-------------------+--------------------+
</pre>

</details>

<details>
<summary><h3>Task 7: Updating the `dim_card_details` table.</h3></summary>

Now we need to update the last table for the card details.

Make the associated changes after finding out what the lengths of each variable should be:
<pre>
+------------------------+-------------------+--------------------+
|    dim_card_details    | current data type | required data type |
+------------------------+-------------------+--------------------+
| card_number            | TEXT              | VARCHAR(?)         |
| expiry_date            | TEXT              | VARCHAR(?)         |
| date_payment_confirmed | TEXT              | DATE               |
+------------------------+-------------------+--------------------+
</pre>

</details>

<details>
<summary><h3>Task 8: Create the primary keys in the dimension tables.</h3></summary>

Now that the tables have the appropriate data types we can begin adding the primary keys to each of the tables prefixed with `dim`.

Each table will serve the `orders_table` which will be the single source of truth for our orders.

Check the column header of the `orders_table` you will see all but one of the columns exist in one of our tables prefixed with `dim`.

We need to update the columns in the `dim` tables with a primary key that matches the same column in the `orders_table`.

Using SQL, update the respective columns as primary key columns.

</details>

<details>
<summary><h3>Task 9: Finalising the star-based schema & adding the foreign keys to the orders table.</h3></summary>

With the primary keys created in the tables prefixed with `dim` we can now create the foreign keys in the `orders_table` to reference the primary keys in the other tables.

Use SQL to create those foreign key constraints that reference the primary keys of the other table.

This makes the star-based database schema complete.

</details>

<details>
<summary><h4>Prerequisites Content: Task 10</h4></summary>

`1. Operating Systems` `2. What is the command line` `3. File Navigation & File Paths` `4. Git and Version Control` `5. Commits and Branches` `6. What is Github?` `7. Github README files`

</details>

<details>
<summary><h3>Task 10: Update the latest code changes to GitHub</h3></summary>

Update your GitHub repository with the latest code changes from your local project. Start by staging your modifications and creating a commit. Then, push the changes to your GitHub repository.

Additionally, document your progress by adding to your GitHub `README` file.
You can refer to the relevant lesson in the prerequisites for this task for more information.

At minimum, your `README` file should contain the following information:
  - Project Title
  - Table of Contents, if the `README` file is long
  - A description of the project: what it does, the aim of the project, and what you learned
  - Installation instructions
  - Usage instructions
  - File structure of the project
  - License information

You don't have to write all of this at once, but make sure to update your `README` file as you go along, so that you don't forget to add anything.

</details>

