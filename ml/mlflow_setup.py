import mlflow
import os
import sys
from pathlib import Path

# Call key values from config.py:
file_path = Path(__file__)
file_dir = os.path.dirname(file_path)
sys.path.append(os.path.dirname(file_dir))
from config import MLFLOW_TRACKING_URI, MLFLOW_ARTIFACT_URI, EXPERIMENT_RAINFALL, EXPERIMENT_TEMPERATURE

if __name__ == "__main__":

    # Set the tracking URI
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    # Experiments set up:
    experiment_name = [EXPERIMENT_RAINFALL, EXPERIMENT_TEMPERATURE]
    for name in experiment_name:
        if mlflow.get_experiment_by_name(name) is None:
            mlflow.create_experiment(name=name, artifact_location = f"{MLFLOW_ARTIFACT_URI}/{name}")
        mlflow.set_experiment(experiment_id = mlflow.get_experiment_by_name(name).experiment_id)

    # Print connection information
    print(f"MLflow Tracking URI: {MLFLOW_TRACKING_URI}")
    print("Active Experiments:")
    print(f"Rainfall - location: {mlflow.get_experiment_by_name(EXPERIMENT_RAINFALL).artifact_location}")
    print(f"Temperature - location: {mlflow.get_experiment_by_name(EXPERIMENT_TEMPERATURE).artifact_location}")