"""
Financial ML Model Security Audit - Vulnerable Starter Code

Purpose:
This intentionally vulnerable script is used for AI/ML security testing.
It demonstrates common machine learning security issues that should be detected
with Semgrep, Bandit, and manual secure code review.

Vulnerabilities demonstrated:
1. Unsafe pickle deserialization
2. Hardcoded credentials
3. Missing data validation
4. Data poisoning risk
5. Model extraction risk

WARNING:
This file is intentionally insecure for educational and defensive testing only.
Do not use these patterns in production.
"""

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score


# ---------------------------------------------------------------------------
# Vulnerability 1: Hardcoded Credentials
# ---------------------------------------------------------------------------

API_KEY = "sk-1234567890abcdef"
SECRET = "api_key_secret123"
TRADING_API_TOKEN = "token_live_demo_12345"


# ---------------------------------------------------------------------------
# Vulnerability 2: Unsafe Pickle Deserialization
# ---------------------------------------------------------------------------

def load_trading_model(model_path):
    """
    Vulnerable model loading function.

    Risk:
    pickle.load() can execute arbitrary code when loading untrusted files.
    If an attacker replaces the model file, code execution can occur during
    model deserialization.
    """
    with open(model_path, "rb") as model_file:
        model = pickle.load(model_file)

    return model


class MaliciousModel:
    """
    Demo object that executes code when unpickled.

    This simulates what could happen if a malicious model file is loaded
    by a trading system.
    """

    def __reduce__(self):
        command = 'echo "EXPLOIT DEMO: Code executed during pickle model load"'
        return (os.system, (command,))


def create_malicious_model_file():
    """
    Creates a malicious pickle file for demonstration purposes.
    """
    with open("malicious_model.pkl", "wb") as file:
        pickle.dump(MaliciousModel(), file)


# ---------------------------------------------------------------------------
# Vulnerability 3: Missing Data Validation
# ---------------------------------------------------------------------------

def load_trading_data(csv_path):
    """
    Vulnerable data loading function.

    Risk:
    No file validation, schema validation, size validation, or data integrity
    verification is performed before loading the dataset.
    """
    data = pd.read_csv(csv_path)
    return data


# ---------------------------------------------------------------------------
# Vulnerability 4: Data Poisoning Demonstration
# ---------------------------------------------------------------------------

def train_clean_model():
    """
    Trains a baseline model on clean synthetic trading data.
    """
    np.random.seed(42)

    x_clean = np.random.randn(1000, 10)
    y_clean = (x_clean[:, 0] > 0).astype(int)

    model = LogisticRegression(max_iter=1000)
    model.fit(x_clean, y_clean)

    x_test = np.random.randn(200, 10)
    y_test = (x_test[:, 0] > 0).astype(int)

    accuracy = accuracy_score(y_test, model.predict(x_test))

    return model, accuracy, x_clean, y_clean, x_test, y_test


def train_poisoned_model(x_clean, y_clean, x_test, y_test):
    """
    Demonstrates how poisoned data can reduce model integrity.

    Risk:
    Attackers can inject mislabeled data into training pipelines and influence
    model behavior.
    """
    x_poison = np.random.randn(100, 10)
    x_poison[:, 0] = -5

    y_poison = np.ones(100)

    x_poisoned = np.vstack([x_clean, x_poison])
    y_poisoned = np.hstack([y_clean, y_poison])

    poisoned_model = LogisticRegression(max_iter=1000)
    poisoned_model.fit(x_poisoned, y_poisoned)

    poisoned_accuracy = accuracy_score(y_test, poisoned_model.predict(x_test))

    return poisoned_model, poisoned_accuracy


# ---------------------------------------------------------------------------
# Vulnerability 5: Model Extraction Demonstration
# ---------------------------------------------------------------------------

class VulnerableTradingModelAPI:
    """
    Vulnerable ML API that returns full prediction probabilities.

    Risk:
    Returning full probability distributions, combined with no rate limiting,
    can help attackers train a surrogate model and steal proprietary logic.
    """

    def __init__(self):
        x_train = np.random.randn(5000, 20)
        y_train = (x_train[:, 0] + x_train[:, 1] > 0).astype(int)

        self.model = MLPClassifier(
            hidden_layer_sizes=(50, 30),
            max_iter=500,
            random_state=42
        )

        self.model.fit(x_train, y_train)

    def predict(self, input_features):
        """
        Vulnerable prediction endpoint.

        Issue:
        Returns full probability distribution instead of only final class.
        """
        return self.model.predict_proba(input_features)


def simulate_model_extraction_attack():
    """
    Simulates attacker behavior by repeatedly querying the ML API and training
    a surrogate model using the returned predictions.
    """
    api = VulnerableTradingModelAPI()

    x_synthetic = np.random.randn(2000, 20)
    stolen_labels = []

    for sample in x_synthetic:
        probabilities = api.predict(sample.reshape(1, -1))
        predicted_label = 1 if probabilities[0][1] > 0.5 else 0
        stolen_labels.append(predicted_label)

    stolen_labels = np.array(stolen_labels)

    surrogate_model = MLPClassifier(
        hidden_layer_sizes=(50, 30),
        max_iter=500,
        random_state=42
    )

    surrogate_model.fit(x_synthetic, stolen_labels)

    x_test = np.random.randn(500, 20)
    original_predictions = (api.predict(x_test)[:, 1] > 0.5).astype(int)
    surrogate_predictions = surrogate_model.predict(x_test)

    agreement = accuracy_score(original_predictions, surrogate_predictions)

    return agreement


# ---------------------------------------------------------------------------
# Demo Runner
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("Financial ML Model Security Audit - Vulnerable Starter Code")
    print("=" * 70)

    print("\n[1] Hardcoded Credentials")
    print(f"API_KEY detected: {API_KEY}")
    print(f"SECRET detected: {SECRET}")
    print(f"TRADING_API_TOKEN detected: {TRADING_API_TOKEN}")

    print("\n[2] Unsafe Pickle Deserialization")
    print("Creating malicious pickle model file...")
    create_malicious_model_file()

    print("Loading malicious model with pickle.load()...")
    load_trading_model("malicious_model.pkl")

    if os.path.exists("malicious_model.pkl"):
        os.remove("malicious_model.pkl")

    print("\n[3] Missing Data Validation")
    print("Function load_trading_data() uses pd.read_csv() without validation.")

    print("\n[4] Data Poisoning Demonstration")
    clean_model, clean_accuracy, x_clean, y_clean, x_test, y_test = train_clean_model()
    poisoned_model, poisoned_accuracy = train_poisoned_model(
        x_clean,
        y_clean,
        x_test,
        y_test
    )

    print(f"Clean model accuracy: {clean_accuracy:.2%}")
    print(f"Poisoned model accuracy: {poisoned_accuracy:.2%}")
    print(f"Accuracy degradation: {(clean_accuracy - poisoned_accuracy):.2%}")

    print("\n[5] Model Extraction Demonstration")
    agreement = simulate_model_extraction_attack()
    print(f"Surrogate model agreement with original model: {agreement:.2%}")

    print("\nAssessment Notes:")
    print("- Semgrep should detect unsafe pickle usage and hardcoded credentials.")
    print("- Bandit should flag insecure deserialization and unsafe patterns.")
    print("- Manual review should identify data poisoning and model extraction risks.")
    print("- Recommended fixes include SafeTensors, signed models, secrets management,")
    print("  data validation, rate limiting, and reduced prediction output detail.")


if __name__ == "__main__":
    main()
