import os
import sys
import csv
import subprocess
from urllib.parse import quote
import pandas as pd
import requests

GS_TOKEN = os.environ['GS_TOKEN']
csv_file_path = r'C:\\Repo\\Python\\GearsetAPI\\Reporting\\ChangeFailureRate\\DeploymentPipelines.csv'

API_URL = "https://api.gearset.com/public/reporting/change-failure-rate/"
HEADERS = {
    'accept': 'application/json',
    'Authorization': f'token {GS_TOKEN}',
    'api-version': '1'
}

def read_csv(file_path):
    # Read a CSV file and return a DataFrame.
    return pd.read_csv(file_path)

def extract_unique_ids(data_frame, column_name):
    # Extract unique IDs from a specific column in a DataFrame.
    return data_frame[column_name].unique()

def get_response(unique_id, start, end):
    # Send a GET request to the API and return the response.
    url = f"{API_URL}{unique_id}?StartDate={quote(start)}&EndDate={quote(end)}"
    response = requests.get(url, headers=HEADERS)
    
    # Check the HTTP status code.
    if response.status_code > 200:
        print(f"HTTP Status Code: {response.status_code}, Unique ID: {unique_id}")
        
    return response.json()

def write_to_csv(deployments):
    # Write deployments data to a CSV file.
    if deployments:
        headers = deployments[0].keys()
        with open('deployments.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for deployment in deployments:
                writer.writerow(deployment)

def call_env_api(unique_ids, start, end):
    # Call the API for each unique ID and write the data to a CSV file.
    for unique_id in unique_ids:
        data = get_response(unique_id, start, end)
        deployments = data.get('Events', [])
        write_to_csv(deployments)

# Hard coded date ranges
start_datetime = "2024-01-01T00:00:00.000Z"
end_datetime = "2024-02-29T23:59:59.000Z"

# Read data from CSV file
df = read_csv(csv_file_path)

# Extracting unique Pipeline IDs and Environment IDs
unique_pipeline_ids = extract_unique_ids(df, 'Pipeline ID')
unique_environment_ids = extract_unique_ids(df, 'Environment ID')

# API is call is built, executed, and outputted here
call_env_api(unique_environment_ids, start_datetime, end_datetime)

# Open the CSV file in Excel
subprocess.Popen(['C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE', 'deployments.csv'])