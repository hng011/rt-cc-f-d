import json
import logging
import requests
import os
import pandas as pd
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.gcsio import GcsIO
from sklearn.preprocessing import MinMaxScaler
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")
DATASET_ID = os.getenv("DATASET_ID")
TABLE_ID = os.getenv("TABLE_ID")
NUMBER_FEATURES = os.getenv("NUMBER_FEATURES")

API_URL = os.getenv("API_URL", f"http://localhost:8501/api/prediction/batch")
BQ_SCHEMA = """
    filename:STRING, 
    transaction_id:STRING, 
    timestamp:TIMESTAMP, 
    features:STRING, 
    autencoder_error:FLOAT, 
    status:STRING
"""

class ProcessGCSFile(beam.DoFn):
    def process(self, element):
            try:
                msg = json.loads(element.decode("utf-8"))
                
                if msg.get('kind') != 'storage#object': return

                bucket = msg['bucket']
                full_path_name = msg['name'] # full path name 
                time_created = msg['timeCreated']
                gcs_path = f"gs://{bucket}/{full_path_name}"
                clean_filename = full_path_name.split('/')[-1]
                logging.info(f"[TRIGGER]: created a new file: {gcs_path}")

                gcs = GcsIO()
                if not gcs.exists(gcs_path): return
                with gcs.open(gcs_path, 'r') as f:
                    try:
                        df = pd.read_csv(f)
                    except Exception as e:
                        logging.error(f"[ERROR]: Unable to read data | {e}")
                        return

                cols_to_drop = [col for col in ["Time", "Class"] if col in df.columns]
                if cols_to_drop:
                    df = df.drop(columns=cols_to_drop)

                if "Amount" in df.columns:
                    scaler = MinMaxScaler()                    
                    df['scaled_amount'] = scaler.fit_transform(df['Amount'].values.reshape(-1, 1))
                    df = df.drop(columns=['Amount'])
                    logging.info(f"[INFO]: data preprocessed ({df.shape[1]} features)")
                
                if df.shape[1] != int(NUMBER_FEATURES):
                    logging.error(f"[ERROR]: Ensure the data has {NUMBER_FEATURES} features")
                    return

                batch_features = df.values.tolist()

                if batch_features:
                    logging.info(f"Sending {len(batch_features)} to ({API_URL})...")
                    
                    payload = {"transactions": [{"features": row} for row in batch_features]}
                    
                    try:
                        response = requests.post(API_URL, json=payload, timeout=60)
                        
                        if response.status_code == 200:
                            api_response = response.json()
                            transactions = api_response["transactions"]
                            
                            logging.info(f"{len(transactions)} prediction rows done.")

                            # Generate Output to BigQuery
                            for i, pred in enumerate(transactions):
                                yield {
                                    "filename": clean_filename,
                                    "transaction_id": f"{clean_filename}_row_{i}",
                                    "timestamp": time_created,
                                    "features": json.dumps(batch_features[i]), 
                                    "autoencoder_error": pred["autoencoder_error"],
                                    "status": pred["status"]
                                }
                        else:
                            logging.error(f"[Error]: {response.status_code}")

                    except Exception as e:
                        logging.error(f"[Error]: unable to connect {e}")

            except Exception as e:
                logging.error(f"Pipeline Error: {e}", exc_info=True)


def run():
    options = PipelineOptions(
        streaming=True, 
        project=PROJECT_ID,
        runner='DirectRunner'
    )

    input_subscription = f"projects/{PROJECT_ID}/subscriptions/{SUBSCRIPTION_ID}"
    output_table = f"{PROJECT_ID}:{DATASET_ID}.{TABLE_ID}"

    with beam.Pipeline(options=options) as p:
        (
            p
            | "ReadPubSub" >> beam.io.ReadFromPubSub(subscription=input_subscription)
            | "ProcessFile" >> beam.ParDo(ProcessGCSFile())
            | "WriteToBQ" >> beam.io.WriteToBigQuery(
                output_table,
                schema=BQ_SCHEMA,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
            )
        )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()