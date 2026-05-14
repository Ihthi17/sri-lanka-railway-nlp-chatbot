import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

import joblib

# Load dataset
df = pd.read_csv("dataset.csv")

# Questions
X = df["question"]

# Intent labels
y = df["intent"]

# Convert words to numbers
vectorizer = CountVectorizer()

X_vectors = vectorizer.fit_transform(X)

# Train model
model = MultinomialNB()

model.fit(X_vectors, y)

# Save model
joblib.dump(model, "chatbot_model.pkl")

# Save vectorizer
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model trained successfully ✅")