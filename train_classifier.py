# train_internship_classifier.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

# 1️⃣ Load combined dataset
df = pd.read_csv(r"C:\Users\shama\OneDrive\Desktop\scam intern detect\combined_internship_dataset.csv")

# 2️⃣ Prepare features and label
# We will use 'job_description' + 'email_domain' combined as feature text
df['combined_text'] = df['job_description'].fillna('') + ' ' + df['email_domain'].fillna('')

X = df['combined_text']
y = df['label']

# 3️⃣ Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 4️⃣ Vectorize text (TF-IDF)
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 5️⃣ Train Logistic Regression
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train_tfidf, y_train)

# 6️⃣ Predict and evaluate Logistic Regression
y_pred_lr = lr_model.predict(X_test_tfidf)

print("\n=== Logistic Regression Results ===")
print("Accuracy:", accuracy_score(y_test, y_pred_lr))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_lr))
print("Classification Report:\n", classification_report(y_test, y_pred_lr))

# 7️⃣ Train Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_tfidf, y_train)

# 8️⃣ Predict and evaluate Random Forest
y_pred_rf = rf_model.predict(X_test_tfidf)

print("\n=== Random Forest Results ===")
print("Accuracy:", accuracy_score(y_test, y_pred_rf))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_rf))
print("Classification Report:\n", classification_report(y_test, y_pred_rf))

# 9️⃣ Save best model → here we save both

# Save vectorizer
with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

# Save Logistic Regression model
with open("logistic_regression_model.pkl", "wb") as f:
    pickle.dump(lr_model, f)

# Save Random Forest model
with open("random_forest_model.pkl", "wb") as f:
    pickle.dump(rf_model, f)

print("\nModels and vectorizer saved! You can now use them in Streamlit app.")
