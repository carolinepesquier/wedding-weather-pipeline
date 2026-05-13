from google.cloud import bigquery

client = bigquery.Client(project="wedding-weather-496115")
print("BigQuery connection successful!")
print(f"Project: {client.project}")