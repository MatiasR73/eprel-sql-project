import requests
import os
import zipfile
import json
import shutil
import pandas as pd
from pathlib import Path

API_BASE = "https://eprel.ec.europa.eu/api"
API_KEY = "A2CmD1dtuj3sZxLmumwfA9kktezviY4O9LRHyiQl" 

BASE_DATA_PATH = r"C:\Users\Matias\Desktop\sql project\data"
os.makedirs(BASE_DATA_PATH, exist_ok=True)

headers = {
    "x-api-key": API_KEY
}

# List of all product categories to loop through
categories = [
    "lightsources",
]

def process_category(category):
    print(f"\nProcessing: {category}")

    zip_path = os.path.join(BASE_DATA_PATH, f"{category}.zip")
    extract_folder = os.path.join(BASE_DATA_PATH, f"{category}_unzipped")
    excel_path = os.path.join(BASE_DATA_PATH, f"{category}.xlsx")

    # Remove old extraction folder if exists
    if os.path.exists(extract_folder):
        shutil.rmtree(extract_folder)

    # Download ZIP export
    request_url = f"{API_BASE}/exportProducts/{category}"
    response = requests.get(request_url, headers=headers, stream=True, timeout=300)
    response.raise_for_status()

    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(8192):
            f.write(chunk)

    print("ZIP downloaded")

    # Extract ZIP
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    print("ZIP extracted")

    # Load all JSON files
    all_rows = []
    for file in Path(extract_folder).glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_rows.extend(data)

    print(f"Loaded {len(all_rows)} records from {category}")

    # Cleanup
    os.remove(zip_path)
    shutil.rmtree(extract_folder)

    # Normalize and save to Excel
    if all_rows:
        df = pd.json_normalize(all_rows)
        df["category"] = category
        df.to_excel(excel_path, index=False)
        print(f"{category}.xlsx created successfully!")
        return True
    else:
        print(f"No data found for {category}")
        return False

def main():
    for category in categories:
        try:
            process_category(category)
        except Exception as e:
            print(f"Error processing {category}: {e}")

main()
