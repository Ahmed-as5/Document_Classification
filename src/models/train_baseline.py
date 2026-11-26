import sys
import joblib
import pandas as pd

from pathlib import Path

from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression

from sklearn.svm import LinearSVC

from sklearn.metrics import accuracy_score, f1_score


PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(PROJECT_ROOT))


from src.data.merge_datasets import load_dataset

from src.preprocessing.text_preprocessing import preprocess_text


MODELS_DIR = PROJECT_ROOT / 'models'
REPORTS_DIR = PROJECT_ROOT / 'reports'

MODELS_DIR.mkdir(exist_ok=True)
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


models = {

    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        random_state=42
    ),

    "SVM": LinearSVC(
        C=1.0,
        random_state=42,
        max_iter=2000
    )

}


results = {}

pipelines = {}


for name, model in models.items():

    pipeline = Pipeline([

        ('tfidf', TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2)
        )),

        ('classifier', model)

    ])


    pipeline.fit(X_train, y_train)


    predictions = pipeline.predict(X_test)


    accuracy = accuracy_score(y_test, predictions)

    f1 = f1_score(
        y_test,
        predictions,
        average='macro'
    )

    results[name] = {

        'Model': name,

        'Accuracy': accuracy,

        'F1-Score': f1

    }


    pipelines[name] = pipeline


    print(f"\n{name}")

    print("Accuracy:", accuracy)

    print("F1-Score:", f1)


    filename = name.lower().replace(' ', '_')

    joblib.dump(
        pipeline,
        MODELS_DIR / f'{filename}_pipeline.joblib'
    )


best_model_name = max(

    results,

    key=lambda name: results[name]['F1-Score']

)


best_pipeline = pipelines[best_model_name]


joblib.dump(

    best_pipeline,

    MODELS_DIR / 'baseline_model.joblib'

)


tfidf_vectorizer = best_pipeline.named_steps['tfidf']

joblib.dump(

    tfidf_vectorizer,

    MODELS_DIR / 'tfidf_vectorizer.joblib'

)


results_df = pd.DataFrame(results.values())

results_df.to_csv(

    REPORTS_DIR / 'baseline_results.csv',

    index=False

)


print("\nBest Model:", best_model_name)

print("Best Results:", results[best_model_name])

print("\nModels Saved Successfully!")

print("Results Saved Successfully!")