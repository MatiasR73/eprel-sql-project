import os
import pandas as pd
from sqlalchemy import create_engine

# Folder with your Excel files
EXCEL_FOLDER = r"C:\Users\matia\Desktop\sql eprel project\eprel-sql-project\data"

# Connection string to local SQL Express with trusted connection
engine = create_engine(
    r"mssql+pyodbc://Matu_LP\SQLEXPRESS/eprel?trusted_connection=yes&Encrypt=no&driver=ODBC+Driver+18+for+SQL+Server"
)

# Loop through all Excel files in folder
for file_name in os.listdir(EXCEL_FOLDER):
    if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
        table_name = os.path.splitext(file_name)[0]  # file name without extension
        file_path = os.path.join(EXCEL_FOLDER, file_name)
        print(f"Importing {file_name} into table {table_name}...")

        try:
            df = pd.read_excel(file_path, engine="openpyxl")
            df.to_sql(table_name, con=engine, if_exists="replace", index=False)
            print(f"{file_name} imported successfully!")
        except Exception as e:
            print(f"Error importing {file_name}: {e}")