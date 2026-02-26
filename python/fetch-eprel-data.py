import pandas
import requests
import inspect
from pathlib import Path

# Script that gets energydata information from EPREL API. 
# Provide the script a .csv file with product SKU and eprel_id.
# Tell the script what folder acts as output_basepath.
# If getting energydata sheets language variable is required.

# TO USE call function run_script()

# Base URL for readaibility
api_base = "https://eprel.ec.europa.eu/api"

# CSV Path to import as data
input_csv = r"C:\Users\Matias\Desktop\EPREL_API_Projekti\IDMap.csv"

# Path to folder you want to import files to
output_basepath = r"C:\Users\Matias\Desktop\EPREL_API_Projekti\Responses"

# Import the CSV
data = pandas.read_csv(input_csv, sep =";")

# Determine the two columns in .CSV data 
# default: sap_sku (users internal product SKU for convenient file naming) 
# and eprel_id which is the SKU that EPREL database uses and has created

ColumnHeader1 = "sap_sku"
ColumnHeader2 = "eprel_id"

# Choose language for energydata sheets
language = "FI"

def run_script():
    """
    Main function that operates the whole script.
    Call this function to start the script.
    """

    # Global data so that Validate ID function works for later functions
    global data

    while True:
        menu()
        choice = input("Choose an option: ")

        if choice == "0":
            print("Exiting script.")
            break

        elif choice == "1":
            print("Running Validate EPREL IDs")
            data = check_idvalidity(data)

        elif choice == "2":
            print("Running Get basic energy data")
            get_energydata()

        elif choice == "3":
            print("Running Get complete energy data")
            get_complete_energy_data()

        elif choice == "4":
            print("Running Download energy labels")
            get_energylabels()

        elif choice == "5":
            print("Running Download energy data sheets")
            get_energydata_sheets()

        elif choice == "6":
            print("Running everything")
            data = check_idvalidity(data)
            get_energydata()
            get_complete_energy_data()
            get_energylabels()
            get_energydata_sheets()

        else:
            print("Invalid input. Please choose 0-6.")

def menu():
    """
    Prints the script menu
    """
    print("1  - Validate EPREL IDs (creates failed CSV & cleans data variable)")
    print("2  - Get basic energy data (creates CSV with determined variables)")
    print("3  - Get complete energy data (creates CSV with all variables available)")
    print("4  - Download energy labels (downloads files into EnergyLabel folder)")
    print("5  - Download energy data sheets (downloads files into DataSheets folder)")
    print("6  - Run everything")
    print("0  - Exit")

def check_idvalidity(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Validates that the eprel_id column values in data dont lead to error with API call.
    If ID leads to error this removes the ID from the variable data.
    Outputs a .csv file that includes all the removed ID's and Error messages.
    Usage: data = check_idvalidity(data)
    
    :param df: CSV input data
    :type df: pandas.DataFrame
    :return: Validated CSV data, errors removed
    :rtype: DataFrame
    """
    # Empty array for results and failed
    valid_rows = []
    failed_rows = []

    # For progress counter
    i = 1
    function_name = inspect.currentframe().f_code.co_name
    total_rows = len(df)

    for row in df.itertuples(index = False):

        # Progress counter
        print(f"{function_name}: Row processed ({i}/{total_rows})")
        i = i + 1

        # CSV Column name
        eprel_id = getattr(row, ColumnHeader2)

        try:
            # Send API the URL
            requestUrl = f"{api_base}/product/{eprel_id}"
            response = requests.get(requestUrl, timeout=20)
            response.raise_for_status()

            # Append valid_rows if no error
            row_dict = row._asdict()
            valid_rows.append(row_dict)
      
        except Exception as e:
            print(f"{function_name}: Removing invalid EPREL_ID {eprel_id} ({e})")

            # Append failed_rows if error
            row_dict = row._asdict()
            row_dict["ERROR"] = str(e)
            failed_rows.append(row_dict)

    # Save the arrays as data frame
    valid_dataframe = pandas.DataFrame(valid_rows)
    failed_dataframe = pandas.DataFrame(failed_rows)

    # Make a .csv file with failed eprel ids
    if not failed_dataframe.empty:
        failed_path = Path(output_basepath) / "failed_eprel_ids.csv"
        failed_dataframe.to_csv(failed_path, sep = ";", index = False)
        print(f"{function_name}: Failed rows saved to {failed_path}")

    print(f"{function_name}: Done. {len(valid_dataframe)}/{total_rows} rows valid.")
    return valid_dataframe

def get_energydata():
    """
    Calls the API with each eprel_id and makes a .csv of chosen product variables.
    Product variables can be chosen under results.append command, default is
    EnergyClass (example: A) and EnergyRange (example: A-D)
    To know what variables are available use get_complete_energy_data and go through
    the column headers
    Output: get_energydata.csv to output_basepath
    """
    # Empty array for results
    results = []

    # For progress counter
    i = 1
    function_name = inspect.currentframe().f_code.co_name
    total_rows = len(data)

    for row in data.itertuples():

        # Progress counter
        print(f"{function_name}: Row processed ({i}/{total_rows})")
        i = i + 1

        # CSV Column name
        eprel_id = getattr(row, ColumnHeader2)
        sap_sku  = getattr(row, ColumnHeader1)


        try:
            # Send API the URL
            requestUrl = f"{api_base}/product/{eprel_id}"
            response = requests.get(requestUrl, timeout=20)
            response.raise_for_status()
            json_data = response.json()
            
            # Choose what variables to return
            results.append({
                "sap_id": sap_sku,
                "eprel_id": eprel_id,
                "EnergyClass":json_data.get("energyClass"),
                "EnergyClassRange":json_data.get("energyClassRange")
            })
        except Exception as e:
            print(f"WARNING: EPREL_ID{eprel_id} failed ({e})")
            continue

    # Output results as CSV
    output_csv = rf"{output_basepath}\get_energydata_results.csv"
    resultsDataFrame = pandas.DataFrame(results)
    resultsDataFrame.to_csv(output_csv, sep=";", index=False)

def get_complete_energy_data ():
    """
    Calls the API with each eprel_id and makes a .csv of complete product variables.
    Will include all of the variables that the API responds with.
    Practical for researching what variables you want in get_energydata
    Lets say that all of the products dont have same variables, the .csv will just
    create a new column header for each variable. This leads to variables that might
    have only one value under specific column header.
    Output: get_complete_energy_data.csv to output_basepath
    """
    # Empty array for results
    results = []

    # For progress counter
    i = 1
    function_name = inspect.currentframe().f_code.co_name
    total_rows = len(data)

    for row in data.itertuples():

        # Progress counter
        print(f"{function_name}: Row processed ({i}/{total_rows})")
        i = i + 1

        # CSV Column name
        eprel_id = getattr(row, ColumnHeader2)
        sap_sku  = getattr(row, ColumnHeader1)


        try:
            # Send API the URL
            requestUrl = f"{api_base}/product/{eprel_id}"
            response = requests.get(requestUrl, timeout=20)
            response.raise_for_status()
            
            # Store the response as Data Frame
            flat_data = pandas.json_normalize(response.json())

            # Add the column data
            flat_data["eprel_id"] = eprel_id
            flat_data["sap_id"] = sap_sku

            # Store the Data frame in results
            results.append(flat_data)

        except Exception as e:
            print(f"WARNING: EPREL_ID{eprel_id} failed ({e})")
            continue

    # Concatenate all of the dataframes into a single dataframe
    if results:
        resultsDataFrame = pandas.concat(results, ignore_index = True)
    
    # So that the script from crash if results is empty
    else:
        resultsDataFrame = pandas.DataFrame()

    # Output results dataframe as .csv file
    output_csv = rf"{output_basepath}\get_complete_energydata_results.csv"
    resultsDataFrame.to_csv(output_csv, sep=";", index=False)

def get_energylabels():
    """
    Calls the API with each eprel_id and saves energy labels as .png files named with sap_id.png
    Creates folder to output_basepath if EnergyLabels not yet exists.
    Outputs: images as .png file to output_basepath/EnergyLabels
    """
    # For progress counter
    i = 1
    function_name = inspect.currentframe().f_code.co_name
    total_rows = len(data)

    target_dir = Path(output_basepath) / "EnergyLabels"
    target_dir.mkdir(parents=True, exist_ok=True)

    for row in data.itertuples():

        # Progress counter
        print(f"{function_name}: Row processed ({i}/{total_rows})")
        i = i + 1

        # CSV Column name
        eprel_id = getattr(row, ColumnHeader2)
        sap_sku  = getattr(row, ColumnHeader1)


        try:
            # Send API the URL
            requestUrl = f"{api_base}/product/{eprel_id}/labels?noRedirect=false&format=PNG"
            response = requests.get(requestUrl, timeout=20)
            response.raise_for_status()

        except Exception as e:
            # Catch errors
            print(f"WARNING: EPREL_ID: {eprel_id} failed ({e})")
            continue

        # Output response as .png file
        image_path = rf"{target_dir}/{sap_sku}.png"
        with open(image_path, "wb") as file:
            file.write(response.content)

def get_energydata_sheets():
    """
    Calls the API with each eprel_id and saves energydata sheets as .pdf files named with sap_id.pdf.
    Creates folder to output_basepath if EnergyDataSheets not yet exists.
    Outputs: information sheets as .pdf file to output_basepath/EnergyDataSheets
    """
    # For progress counter
    i = 1
    function_name = inspect.currentframe().f_code.co_name
    total_rows = len(data)

    target_dir = Path(output_basepath) / "EnergyDataSheets"
    target_dir.mkdir(parents=True, exist_ok=True)

    for row in data.itertuples():

        # Progress counter
        print(f"{function_name}: Row processed ({i}/{total_rows})")
        i = i + 1

        # CSV Column name
        eprel_id = getattr(row, ColumnHeader2)
        sap_sku  = getattr(row, ColumnHeader1)


        try:
            # Send API the URL
            requestUrl = f"{api_base}/product/{eprel_id}/fiches?noRedirect=false&language={language}"
            response = requests.get(requestUrl, timeout=20)
            response.raise_for_status()

        except Exception as e:
            # Catch errors
            print(f"WARNING: EPREL_ID: {eprel_id} failed ({e})")
            continue

        # Output response as .pdf file
        image_path = rf"{target_dir}/{sap_sku}.pdf"
        with open(image_path, "wb") as file:
            file.write(response.content)

run_script()