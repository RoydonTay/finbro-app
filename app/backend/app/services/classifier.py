# classifier.py
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import os

class Classifier:
    def __init__(self):
        model_dir = "app/models/roberta-base"
        self.model = AutoModelForSequenceClassification.from_pretrained(model_dir, local_files_only=True)
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)

    def preprocess_function(self, examples):
        return self.tokenizer.tokenizer(examples["text"], truncation=True)

    def get_sentiment_label_and_score(self, text: str):
        labels = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
        sentiment_classifier = pipeline(task="text-classification", model=self.model, tokenizer=self.tokenizer, device_map="cpu")
        output = sentiment_classifier(text)
        output[0]["label"] = labels[output[0]["label"]]
        return output