# ui_app.py

import streamlit as st
import pandas as pd
import joblib
import easyocr
import spacy
import re
import webbrowser

# Load model and vectorizer
model = joblib.load("random_forest_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Load fake internship dataset (for matching display)
fake_df = pd.read_csv("fake_internship_dataset.csv")
fake_company_list = fake_df['company_name'].str.lower().tolist()

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Function to extract text from image
def extract_text(uploaded_file):
    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        result = reader.readtext(image_bytes, detail=0)
        full_text = " ".join(result)
        return full_text
    return ""

# Function to extract company name using simple regex / logic
def extract_company_name(text):
    # Example regex for a company name-like phrase (improve as needed)
    match = re.search(r"(?:internship|certificate)\s*at\s*([A-Za-z0-9&.\- ]+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    else:
        # fallback: take first line or first 3 words
        return " ".join(text.split()[:3])

# Streamlit UI
st.set_page_config(page_title="InternCheck", page_icon="🔍")
st.title("InternCheck - Internship Scam Detector🔍")


uploaded_file = st.file_uploader("Upload Internship offer letter / Certificate / Screenshot", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Certificate", use_container_width=True)

    with st.spinner("Analyzing document..."):
        extracted_text = extract_text(uploaded_file)
        company_name = extract_company_name(extracted_text)

        # Vectorize text
        X = vectorizer.transform([extracted_text])
        prediction = model.predict(X)[0]

        # Display result clearly
        if prediction == 1:
            st.error("🚩 This internship appears to be a SCAM, please be careful!")
        else:
            st.success("✅ This internship appears to be REAL, Let's gooo!")

        # Extra: show if company matches fake list
        if company_name.lower() in fake_company_list:
            st.warning(f"⚠️ This company **{company_name}** is present in the known scam list!")

        # Google button
        if st.button("🔎 Google this internship"):
            search_query = company_name + " internship reviews"
            google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
            webbrowser.open_new_tab(google_url)





