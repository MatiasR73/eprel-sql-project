# eprel-sql-project


Step 1:
Download all EPREL database products as ZIP files from EPREL API and convert them to .xlsx files. Both with one script:
"fetch-eprel-data-as-xlsx.py"

Step 2: 
Create a SQL localhost server using SQL Server Management Studio and SQL Express. Create "eprel" named database inside that server. Connect to it via VS.

Step 3:
Import all fetched .xlsx files into the SQL localhost server using script: 
"import-files-to-sql-server.py"

Step 4:
"create-id-column.sql" to simplify accessing product ID's
"count-of-products-by-organisation.sql" to list all organisations from all tables and count their occurences.
"create-energyclass-table-for-ranking.sql" to make a table of energyclasses and assign point variable to them.
"rank-organisations-by-energyclasspoints" to list organisations from single table and rank them by how high energyclass avg they have.

Step 5:
Create a way to display the results.

