import sys
import joblib

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(PROJECT_ROOT))


from src.data.merge_datasets import load_dataset

from src.preprocessing.text_preprocessing import preprocess_text


MODELS_DIR = PROJECT_ROOT / 'models'

REPORTS_DIR = PROJECT_ROOT / 'reports'

REPORTS_DIR.mkdir(exist_ok=True)


data = load_dataset()


data['processed_text'] = data['data'].apply(preprocess_text)


X = data['processed_text']

y = data['labels']


X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42,

    stratify=y

)


model_files = {

    "Logistic Regression":
        "logistic_regression_pipeline.joblib",

    "SVM":
        "svm_pipeline.joblib"

}


for name, filename in model_files.items():

    model_path = MODELS_DIR / filename

    if not model_path.exists():

        print(f"{name} model not found!")

        continue


    pipeline = joblib.load(model_path)


    predictions = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)


    f1 = f1_score(
        y_test,
        predictions,
        average='macro'
    )


    print(f"\n{'=' * 50}")

    print(name)

    print(f"{'=' * 50}")

    print("Accuracy:", accuracy)

    print("F1-Score:", f1)


    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions
        )
    )

    cm = confusion_matrix(
        y_test,
        predictions,
        labels=pipeline.classes_
    )


    plt.figure(figsize=(10, 7))


    sns.heatmap(

        cm,

        annot=True,

        fmt='d',

        cmap='Blues',

        xticklabels=pipeline.classes_,

        yticklabels=pipeline.classes_

    )


    plt.title(f'{name} - Confusion Matrix')

    plt.xlabel('Predicted Label')

    plt.ylabel('True Label')

    plt.tight_layout()

    image_name = name.lower().replace(' ', '_')

    plt.savefig(
        REPORTS_DIR / f'{image_name}_confusion_matrix.png',
        dpi=300
    )


    plt.show()