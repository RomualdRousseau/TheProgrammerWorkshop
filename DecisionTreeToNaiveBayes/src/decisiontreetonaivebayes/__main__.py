import csv
import math
import re
from typing import Any

import numpy as np


def tokenizer(data: str, delimiters=r'[\s.,;:!?\'"()\[\]{}<>/\\|@#\$%^&*+=~`-]+') -> list[str]:
    return {token.lower() for token in re.split(delimiters, data) if token}


def to_categorical(vocabulary: list[str], message: str) -> np.ndarray:
    tokens = tokenizer(message)
    vector = [1.0 if token in tokens else 0.0 for token in vocabulary]
    return np.array(vector)


def load_data(path: str) -> tuple[dict[str, Any], list[str]]:
    data = {
        "categories": {"ham": 0, "spam": 0},
        "all": 0,
        "tokens": {},
    }

    def token_append(tokens: dict[str, dict[str, int]], category: str, token: str) -> dict[str, dict[str, int]]:
        stat = tokens.setdefault(
            token,
            {
                "categories": {"ham": 0, "spam": 0},
                "all": 0,
            },
        )
        stat["categories"][category] += 1
        stat["all"] += 1
        return tokens

    with open(path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip header row

        for row in reader:
            category, message = row

            data["categories"][category] += 1
            data["all"] += 1

            for token in tokenizer(message):
                data["tokens"] = token_append(data["tokens"], category, token)

    return data, sorted(data["tokens"].keys())


def fit(data: dict[str, Any], vocabulary: list[str]) -> tuple[np.ndarray, np.ndarray]:
    def p_token_given_category(data, token, category):
        return math.log(data["tokens"][token]["categories"][category] / data["all"] + 1e-6)

    def p_category(data, category):
        return math.log(data["categories"][category] / data["all"] + 1e-6)

    weights = [[p_token_given_category(data, token, category) for category in ["ham", "spam"]] for token in vocabulary]
    biases = [p_category(data, category) for category in ["ham", "spam"]]
    return np.array(weights), np.array(biases)


def predict(input: np.ndarray, weights: np.ndarray, biases: np.ndarray) -> np.ndarray:
    return np.exp(input @ weights + biases)


data, vocabulary = load_data("data/mail_data.csv")
weights, biases = fit(data, vocabulary)

with open("data/mail_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # Skip header row
    for row in reader:
        category, message = row
        output = predict(to_categorical(vocabulary, message), weights, biases)
        if output[0] > output[1]:
            category_hat = "ham"
        else:
            category_hat = "spam"
        if category != category_hat:
            print(f"I think it is {category_hat} but it is {category}: ", message)
