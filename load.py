from google.cloud import bigquery

def load_to_bigquery(df, table_id):

    # BigQuery pre-requisites:
    client = bigquery.Client(project = "wedding-weather-496115")

    job_config = bigquery.LoadJobConfig(
        write_disposition = bigquery.WriteDisposition.WRITE_APPEND
        )       

    # Load the DataFrame to BigQuery:
    job = client.load_table_from_dataframe(df, table_id, job_config = job_config)

    # Waits for the job to complete:
    job.result()  

    # Make API request:
    table = client.get_table(table_id)
    print("Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
            )
        )