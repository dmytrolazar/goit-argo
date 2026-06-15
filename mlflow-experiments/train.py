import os
from dotenv import load_dotenv
load_dotenv()

import mlflow
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss

# Параметри
learning_rate = 0.01
epochs = 100
experiment_name = "Iris Classification"

# URI трекінгу
mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])

# Отримуємо експеримент за назвою
experiment = mlflow.get_experiment_by_name(experiment_name)
if experiment is None:
    experiment_id = mlflow.create_experiment(experiment_name)
    print(f"✅ Створено експеримент '{experiment_name}' (ID={experiment_id})")
else:
    experiment_id = experiment.experiment_id
    print(f"ℹ️ Використовується існуючий експеримент '{experiment_name}' (ID={experiment_id})")

# 🛠️ Тут важлива відмінність: start_run з name, а не з experiment_id напряму
with mlflow.start_run(experiment_id=experiment_id):
    mlflow.log_param("learning_rate", learning_rate)
    mlflow.log_param("epochs", epochs)

    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    model = LogisticRegression(max_iter=epochs)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)

    acc = accuracy_score(y_test, y_pred)
    loss = log_loss(y_test, y_proba)

    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("loss", loss)

    mlflow.sklearn.log_model(model, "model")

    print("✅ Експеримент завершено. Перевірте результати в MLflow UI.")