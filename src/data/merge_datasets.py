import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


DATASET_PATH = PROJECT_ROOT / 'data' / 'raw' / 'bbc_data.csv'


def load_dataset():

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    data = pd.read_csv(DATASET_PATH)

    required_columns = {'data', 'labels'}

    if not required_columns.issubset(data.columns):
        raise ValueError(
            "Dataset must contain 'data' and 'labels' columns."
        )

    data = data.drop_duplicates().copy()

    data = data.reset_index(drop=True)

    data = data.dropna(subset=['data', 'labels'])

    return data


if __name__ == "__main__":

    data = load_dataset()

    print("Dataset Loaded Successfully!")

    print("Dataset Shape:", data.shape)

    print("\nCategory Distribution:")

    print(data['labels'].value_counts())