import os
import requests
import pandas as pd
""""""""""""""""""""""""""""""""""""""""""
def download_data(currencies, start_date, end_date,data_dir=os.getcwd() + '/Data/csv'):
    subdir = f"{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}"
    full_dir = os.path.join(data_dir, subdir)
    os.makedirs(full_dir, exist_ok=True)

    for currency in currencies:
        filename = f"{currency}.csv"
        filepath = os.path.join(full_dir, filename)

        if os.path.exists(filepath):
            print(f"File {filename} already exists, skipping data download.")
            continue

        url = f"https://stooq.com/q/d/l/?s={currency}&d1={start_date.strftime('%Y%m%d')}&d2={end_date.strftime('%Y%m%d')}&i=d"
        response = requests.get(url)

        if response.status_code == 200:
            csv_content = response.content
            with open(filepath, "wb") as csv_file:
                csv_file.write(csv_content)
            print(f"Data for {currency} saved to {filename}.")
        else:
            print(f"Failed to download data for {currency}.")
def create_dataframe_dict(path):
    dictionary = {}

    for filename in os.listdir(path):
        new_name = os.path.splitext(filename)[0]
        new_name = new_name.split('_')[0]

        if filename.endswith(".csv"):
            file_path = os.path.join(path, filename)
            df = pd.read_csv(file_path)
            dictionary[f"{new_name}"] = df

    return dictionary











